# -*- coding: utf-8 -*-
import requests
import json
import time
import os
import re
from typing import Optional, Dict, Any
from flask import Flask, request, jsonify

# 从环境变量读取配置
MINIMAX_API_KEY = os.getenv('MINIMAX_API_KEY')
SERVER_PORT = int(os.getenv('SERVER_PORT', '5000'))
MAX_TEXT_LENGTH = int(os.getenv('MAX_TEXT_LENGTH', '2000'))

if not MINIMAX_API_KEY:
    raise ValueError("请设置 MINIMAX_API_KEY 环境变量")

class MinimaxToOpenAIAdapter:
    def __init__(self, minimax_api_key: str, max_text_length: int = 2000):
        self.minimax_api_key = minimax_api_key
        self.max_text_length = max_text_length
        self.minimax_base_url = "https://api.minimaxi.chat"
    
    def text_to_speech(self, text: str, voice_id: str, model: str = "speech-2.6-hd", response_format: str = "mp3") -> Optional[Dict[str, Any]]:
        # 清理文本中的特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff，。！？；：""''""""—–（）【】《》]', '', text)
        
        headers = {
            "Authorization": f"Bearer {self.minimax_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": text,
            "model": model,
            "voice_setting": {
                "voice_id": voice_id,
                "speed": 1.0,
                "vol": 1.0
            },
            "response_format": response_format,
            "stream": False
        }
        
        url = f"{self.minimax_base_url}/v1/t2a_v2"
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.encoding = 'utf-8'
            json_response = response.json()
            
            base_resp = json_response.get("base_resp", {})
            if base_resp.get("status_code") != 0:
                error_msg = base_resp.get("status_msg", "未知错误")
                return {
                    "error": {
                        "message": f"MiniMax TTS错误: {error_msg}",
                        "type": "api_error",
                        "code": "minimax_tts_error"
                    }
                }
            
            if "data" in json_response and "audio" in json_response["data"]:
                audio_hex = json_response["data"]["audio"]
                audio_data = bytes.fromhex(audio_hex)
                
                return {
                    "audio_data": audio_data,
                    "model": model,
                    "voice_id": voice_id,
                    "usage": {
                        "prompt_tokens": len(text),
                        "completion_tokens": 0,
                        "total_tokens": len(text)
                    }
                }
            else:
                return {
                    "error": {
                        "message": "API响应中缺少音频数据",
                        "type": "api_error",
                        "code": "missing_audio_data"
                    }
                }
        
        except Exception as e:
            return {
                "error": {
                    "message": f"TTS处理错误: {str(e)}",
                    "type": "processing_error", 
                    "code": "tts_processing_error"
                }
            }

app = Flask(__name__)
adapter = MinimaxToOpenAIAdapter(MINIMAX_API_KEY, MAX_TEXT_LENGTH)

@app.route('/v1/audio/speech', methods=['POST'])
def handle_text_to_speech():
    if not request.is_json:
        return jsonify({"error": {"message": "请求必须是JSON格式", "type": "invalid_request"}}), 400
        
    data = request.get_json()
    if not data or 'input' not in data:
        return jsonify({"error": {"message": "缺少输入文本", "type": "invalid_request"}}), 400
    
    text = data['input']
    voice_id = data.get('voice')
    response_format = data.get('response_format', 'mp3')
    
    if not voice_id:
        return jsonify({"error": {"message": "缺少voice参数", "type": "invalid_request"}}), 400
    
    if not text.strip():
        return jsonify({"error": {"message": "输入文本不能为空", "type": "invalid_request"}}), 400
    
    result = adapter.text_to_speech(text, voice_id, response_format=response_format)
    
    if "error" in result:
        return jsonify(result), 500
    
    from flask import Response
    mimetype = 'audio/wav' if response_format == 'wav' else 'audio/mpeg'
    return Response(result["audio_data"], mimetype=mimetype)

@app.route('/audio/speech', methods=['POST'])
def handle_text_to_speech_compat():
    return handle_text_to_speech()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "服务运行正常"})

if __name__ == '__main__':
    print("=== MiniMax TTS适配器启动 ===")
    print(f"服务地址: http://0.0.0.0:{SERVER_PORT}")
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=False)
