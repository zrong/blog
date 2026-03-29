"""Provider 实现：按 type 字段分派到 OpenAI/Gemini API"""

import base64
import re

import httpx

# 聊天生图模型关键词（走 chat/completions 而非 images/generations）
_CHAT_IMAGE_MODELS = re.compile(r"gpt-image|sora", re.IGNORECASE)


def fetch_models(provider_config: dict) -> list[str]:
    """从 API 获取可用模型列表"""
    ptype = provider_config["type"]
    if ptype == "openai":
        return _fetch_openai_models(provider_config)
    elif ptype == "gemini":
        return _fetch_gemini_models(provider_config)
    else:
        raise ValueError(f"不支持的 provider type: {ptype}")


def generate_image(
    prompt: str,
    provider_config: dict,
    model: str | None = None,
    size: str = "1024x1024",
    output: str | None = None,
    n: int = 1,
) -> list[str]:
    """生成图片，返回保存的文件路径列表"""
    model = model or provider_config.get("default_model", "")
    if not model:
        raise ValueError("未指定模型，请通过 -m 参数或配置 default_model")

    ptype = provider_config["type"]
    if ptype == "openai":
        results = _generate_openai(prompt, provider_config, model, size, n)
    elif ptype == "gemini":
        results = _generate_gemini(prompt, provider_config, model, n)
    else:
        raise ValueError(f"不支持的 provider type: {ptype}")

    # 保存文件
    saved = []
    for i, data in enumerate(results):
        path = output if len(results) == 1 else _suffix_output(output, i)
        if path is None:
            path = f"generated_{i}.png"
        with open(path, "wb") as f:
            f.write(data)
        saved.append(path)
    return saved


# ── OpenAI 兼容 ──────────────────────────────────────────


def _fetch_openai_models(cfg: dict) -> list[str]:
    url = f"{cfg['base_url']}/models"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}
    with httpx.Client(timeout=30) as client:
        resp = client.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    models = data.get("data", [])
    return sorted(m["id"] for m in models)


def _generate_openai(prompt: str, cfg: dict, model: str, size: str, n: int) -> list[bytes]:
    if _CHAT_IMAGE_MODELS.search(model):
        return _generate_openai_chat(prompt, cfg, model, n)
    return _generate_openai_images(prompt, cfg, model, size, n)


def _generate_openai_images(prompt: str, cfg: dict, model: str, size: str, n: int) -> list[bytes]:
    url = f"{cfg['base_url']}/images/generations"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}
    body = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "n": n,
        "response_format": "b64_json",
    }
    with httpx.Client(timeout=120) as client:
        resp = client.post(url, headers=headers, json=body)
        resp.raise_for_status()
        data = resp.json()
        return [_extract_b64_or_url(img, client) for img in data.get("data", [])]


def _generate_openai_chat(prompt: str, cfg: dict, model: str, n: int) -> list[bytes]:
    url = f"{cfg['base_url']}/chat/completions"
    headers = {"Authorization": f"Bearer {cfg['api_key']}"}
    results = []
    with httpx.Client(timeout=120) as client:
        for _ in range(n):
            body = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
            }
            resp = client.post(url, headers=headers, json=body)
            resp.raise_for_status()
            data = resp.json()
            # 从响应中提取图片
            choices = data.get("choices", [])
            if not choices:
                raise ValueError("Chat completions 响应中没有 choices")
            message = choices[0].get("message", {})
            content = message.get("content", "")
            # content 可能是字符串或列表
            if isinstance(content, list):
                for part in content:
                    if isinstance(part, dict):
                        img_url = part.get("image_url", {}).get("url") or part.get("image_url", {}).get(
                            "url", ""
                        )
                        # 处理 gpt-image-1 格式：part.type == "image_url" 或 part 有 inline_data
                        if part.get("type") == "image_url":
                            img_url = part.get("image_url", {}).get("url", "")
                        elif "inline_data" in part:
                            b64 = part["inline_data"].get("data", "")
                            results.append(base64.b64decode(b64))
                            continue
                        if img_url:
                            if img_url.startswith("data:"):
                                b64 = img_url.split(",", 1)[1]
                                results.append(base64.b64decode(b64))
                            else:
                                img_resp = client.get(img_url)
                                img_resp.raise_for_status()
                                results.append(img_resp.content)
            elif isinstance(content, str):
                # 某些代理可能直接返回 base64 或 URL 在文本中
                raise ValueError(f"模型返回了文本而非图片内容: {content[:200]}")
    return results


def _extract_b64_or_url(img_data: dict, client: httpx.Client) -> bytes:
    """从 images/generations 响应提取图片数据"""
    if "b64_json" in img_data:
        return base64.b64decode(img_data["b64_json"])
    url = img_data.get("url", "")
    if url:
        resp = client.get(url)
        resp.raise_for_status()
        return resp.content
    raise ValueError("响应中没有 b64_json 也没有 url")


# ── Gemini 兼容 ──────────────────────────────────────────


def _fetch_gemini_models(cfg: dict) -> list[str]:
    url = f"{cfg['base_url']}/models"
    headers = {"x-goog-api-key": cfg["api_key"]}
    with httpx.Client(timeout=30) as client:
        resp = client.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    models = data.get("models", [])
    return sorted(m.get("name", "") for m in models)


def _generate_gemini(prompt: str, cfg: dict, model: str, n: int) -> list[bytes]:
    url = f"{cfg['base_url']}/models/{model}:generateContent"
    headers = {"x-goog-api-key": cfg["api_key"]}
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }
    results = []
    with httpx.Client(timeout=120) as client:
        for _ in range(n):
            resp = client.post(url, headers=headers, json=body)
            resp.raise_for_status()
            data = resp.json()
            candidates = data.get("candidates", [])
            if not candidates:
                raise ValueError("Gemini 响应中没有 candidates")
            parts = candidates[0].get("content", {}).get("parts", [])
            for part in parts:
                inline = part.get("inlineData") or part.get("inline_data")
                if inline and "data" in inline:
                    results.append(base64.b64decode(inline["data"]))
                    break
            else:
                raise ValueError("Gemini 响应中没有图片数据")
    return results


# ── 辅助 ──────────────────────────────────────────────────


def _suffix_output(output: str | None, index: int) -> str:
    """为多张图片生成带序号的文件名"""
    if output is None:
        return f"generated_{index}.png"
    stem = output.rsplit(".", 1)[0] if "." in output else output
    ext = output.rsplit(".", 1)[1] if "." in output else "png"
    return f"{stem}_{index}.{ext}"
