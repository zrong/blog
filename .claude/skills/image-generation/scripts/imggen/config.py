"""配置文件加载

配置查找策略（按优先级）：
1. 当前工作目录（CWD）/agent_config.toml
2. Skill 目录（SKILL_DIR）/agent_config.toml
3. 向上查找 .git 所在目录/agent_config.toml

这样无论 skill 安装在项目内还是全局都能找到配置。
"""

from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


def _find_config() -> tuple[Path, Path]:
    """查找配置文件和 skill 目录

    Returns:
        (config_path, skill_dir)
    """
    skill_dir = Path(__file__).resolve().parent.parent.parent

    # 候选配置路径（优先级从高到低）
    candidates = [
        Path.cwd() / "agent_config.toml",
        skill_dir / "agent_config.toml",
    ]

    # 向上查找 .git 目录
    for parent in Path.cwd().parents:
        if (parent / ".git").exists():
            candidates.append(parent / "agent_config.toml")
            break

    for candidate in candidates:
        if candidate.exists():
            return candidate, skill_dir

    raise FileNotFoundError(
        f"未找到 agent_config.toml\n"
        f"搜索了: {', '.join(str(c) for c in candidates)}\n"
        f"请复制 {skill_dir / 'agent_config.example.toml'} 为 agent_config.toml 并填入实际值"
    )


CONFIG_PATH, SKILL_DIR = _find_config()
CONFIG_EXAMPLE_PATH = SKILL_DIR / "agent_config.example.toml"


def load_config(path: Path = CONFIG_PATH) -> dict:
    """加载配置文件"""
    if not path.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {path}\n"
            f"请复制 {CONFIG_EXAMPLE_PATH} 为 agent_config.toml 并填入实际值"
        )
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _get_imggen_config(config: dict | None = None) -> dict:
    """提取 [image-generation] 子字典"""
    config = config or load_config()
    return config.get("image-generation", {})


def list_providers(config: dict | None = None) -> list[dict]:
    """列出所有已配置的 provider 及其端点

    Returns:
        [{"key": "apiyi", "name": "API易", "is_default": True,
          "endpoints": [{"type": "openai", "base_url": "...", "default_model": "..."}]}, ...]
    """
    imggen = _get_imggen_config(config)
    providers = imggen.get("providers", {})
    default = imggen.get("default_provider", "")
    result = []
    for k, v in providers.items():
        endpoints = _parse_endpoints(v)
        result.append({
            "key": k,
            "name": v.get("name", k),
            "is_default": k == default,
            "endpoints": endpoints,
        })
    return result


def get_endpoint_config(
    provider: str | None = None,
    endpoint: str | None = None,
    config: dict | None = None,
) -> dict:
    """获取指定 provider + endpoint 的扁平配置（供 provider.py 使用）

    Args:
        provider: provider key，None 时使用 default_provider 或首个
        endpoint: endpoint type（如 "openai"、"gemini"），None 时使用首个端点
        config: 配置字典，None 时自动加载

    Returns:
        {"type", "name", "base_url", "api_key", "default_model", "provider_key"}
    """
    imggen = _get_imggen_config(config)
    providers = imggen.get("providers", {})
    if not providers:
        raise ValueError("未配置任何 provider，请在 agent_config.toml 中添加 [image-generation.providers.xxx]")

    if provider:
        if provider not in providers:
            available = ", ".join(providers.keys())
            raise ValueError(f"Provider '{provider}' 不存在，可用: {available}")
        key = provider
    else:
        key = imggen.get("default_provider", "")
        if not key or key not in providers:
            key = next(iter(providers))

    p = providers[key]
    endpoints = _parse_endpoints(p)

    if not endpoints:
        raise ValueError(f"Provider '{key}' 没有配置任何 endpoint")

    ep = None
    if endpoint:
        ep = next((e for e in endpoints if e["type"] == endpoint), None)
        if not ep:
            available = ", ".join(e["type"] for e in endpoints)
            raise ValueError(f"Endpoint '{endpoint}' 不存在于 provider '{key}'，可用: {available}")
    else:
        ep = endpoints[0]

    return {
        "provider_key": key,
        "type": ep["type"],
        "name": p.get("name", key),
        "base_url": ep["base_url"].rstrip("/"),
        "api_key": p.get("api_key", ""),
        "default_model": ep.get("default_model", ""),
    }


def _parse_endpoints(provider_dict: dict) -> list[dict]:
    """从 provider 配置中解析端点列表

    支持两种格式：
    1. endpoints 子键（推荐）：endpoints.openai / endpoints.gemini
    2. 扁平格式（向后兼容）：直接在 provider 下有 type/base_url
    """
    eps = provider_dict.get("endpoints")
    if eps:
        return [
            {
                "type": k,
                "base_url": v.get("base_url", ""),
                "default_model": v.get("default_model", ""),
            }
            for k, v in eps.items()
        ]
    # 扁平格式兼容
    if "base_url" in provider_dict:
        return [{
            "type": provider_dict.get("type", "openai"),
            "base_url": provider_dict["base_url"],
            "default_model": provider_dict.get("default_model", ""),
        }]
    return []
