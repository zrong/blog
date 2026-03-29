# 技术参考

## 模块结构

```
scripts/imggen/
├── __init__.py     # 包初始化
├── cli.py          # CLI 入口（typer）
├── config.py       # 配置加载
└── provider.py     # Provider 实现
```

## config.py

复用 rspeak 的 `_find_project_root()` 模式，从项目根 `agent_config.toml` 的 `[image-generation]` 命名空间加载配置。

关键函数：
- `load_config()` → 加载完整配置文件
- `_get_imggen_config()` → 提取 `[image-generation]` 子字典
- `list_providers()` → 返回所有 provider 概要信息
- `get_provider_config(provider)` → 获取指定 provider 配置，支持默认/首个回退

## provider.py

扁平分派设计，按 provider 的 `type` 字段分派到不同 API 实现。

### OpenAI 兼容实现

**获取模型**：
- `GET {base_url}/models`
- Header: `Authorization: Bearer {api_key}`
- 返回模型 ID 列表

**生成图片（Images API）**：
- `POST {base_url}/images/generations`
- Body: `{"model": "...", "prompt": "...", "size": "1024x1024", "n": 1}`
- 用于标准图片生成模型（DALL-E、Flux 等）

**生成图片（Chat Completions API）**：
- `POST {base_url}/chat/completions`
- Body: `{"model": "...", "messages": [{"role": "user", "content": [{"type": "text", "text": "..."}, {"type": "image_url", "image_url": {"url": "..."}}]}]}`
- 用于聊天生图模型（GPT-Image-1、Sora Image 等）
- 模型名称匹配规则：包含 `gpt-image`、`sora` 等关键词的模型自动走此路径

**响应处理**：
- 优先使用 `b64_json` 字段（base64 解码保存）
- 回退使用 `url` 字段（下载图片数据）

### Gemini 兼容实现

**获取模型**：
- `GET {base_url}/models`
- Header: `x-goog-api-key: {api_key}`

**生成图片**：
- `POST {base_url}/models/{model}:generateContent`
- Header: `x-goog-api-key: {api_key}`
- Body:
```json
{
  "contents": [{"parts": [{"text": "prompt"}]}],
  "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
}
```
- 响应：从 `candidates[0].content.parts[]` 提取 `inlineData.data`（base64 图片）

## CLI 命令（cli.py）

使用 typer 框架，三个子命令：

- `list`：列出已配置的 provider
- `models`：从 API 获取可用模型列表（可选 `-p` 指定 provider）
- `generate`：生成图片，参数包括 prompt、provider、model、size、output、n
