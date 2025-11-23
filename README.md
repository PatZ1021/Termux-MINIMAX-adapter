```markdown
# MiniMax to OpenAI TTS Adapter

一个将MiniMax语音合成API转换为OpenAI兼容格式的适配器，专为OMate等支持OpenAI协议的应用设计。

## 🎯 功能特性

- ✅ 将MiniMax TTS API转换为OpenAI兼容格式
- ✅ 支持多AI伴侣不同音色
- ✅ 自动清理特殊字符，避免编码错误
- ✅ 支持MP3和WAV音频格式
- ✅ 轻量级，易于部署

## 🚀 快速开始

### 环境要求

- Python 3.6+
- Flask
- Requests

### 安装依赖

```bash
pip install flask requests
```

### 配置环境变量

```bash
# 设置MiniMax API密钥
export MINIMAX_API_KEY="你的MiniMax_API密钥"

# 可选配置
export SERVER_PORT=5000
export MAX_TEXT_LENGTH=2000
```

### 运行服务

```bash
python minimax_adapter_final.py
```

## 📱 OMate配置

在OMate中添加自定义语音服务：

```
基础URL: http://127.0.0.1:5000  # 或你的服务器IP
Voice ID: 你的MiniMax音色ID
```

### 获取音色ID

访问[MiniMax开放平台](https://api.minimaxi.chat/document/tts)查看可用音色列表。

## 🔧 API端点

### 文本转语音 (OpenAI兼容)
- `POST /v1/audio/speech`
- `POST /audio/speech` (兼容端点)

### 健康检查
- `GET /health`

## 🛠️ 开发说明

### 请求格式
```json
{
  "input": "要转换的文本",
  "voice": "音色ID",
  "response_format": "mp3"
}
```

### 响应格式
返回二进制音频数据，兼容OpenAI TTS API规范。

## 📦 部署到Termux

### 一键启动命令
在Termux的`~/.bashrc`中添加：
```bash
alias minimaxyy='cd ~/minimax-adapter && python minimax_adapter_final.py'
```

然后只需输入：
```bash
minimaxyy
```

## 🐛 故障排除

### 常见问题
1. **编码错误**: 确保API密钥不包含中文字符
2. **认证失败**: 检查API密钥是否正确
3. **音色不存在**: 验证Voice ID是否有效

### 日志查看
服务运行时会显示请求处理状态，便于调试。

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！
```

## 🎯 GitHub仓库建议结构

```
minimax-openai-adapter/
├── minimax_adapter_final.py  # 主程序
├── README.md                 # 说明文档
└── requirements.txt          # 依赖列表
```
