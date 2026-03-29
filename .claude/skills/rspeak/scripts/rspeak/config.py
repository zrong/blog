"""配置文件加载

配置文件路径：项目根目录/agent_config.toml
从 skill 目录下的 agent_config.example.toml 复制并填入实际值。
所有 rspeak 配置收纳在 [rspeak] 命名空间下。
"""

from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


# 定位项目根（向上查找 .git）
def _find_project_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / ".git").exists():
            return parent
    raise FileNotFoundError("无法定位项目根目录（未找到 .git）")


PROJECT_ROOT = _find_project_root()
CONFIG_PATH = PROJECT_ROOT / "agent_config.toml"
SKILL_DIR = Path(__file__).resolve().parent.parent.parent  # rspeak/ -> scripts/ -> skill 目录
CONFIG_EXAMPLE_PATH = SKILL_DIR / "agent_config.example.toml"


def load_config(path: Path = CONFIG_PATH) -> dict:
    """加载配置文件

    Args:
        path: 配置文件路径，默认为项目根目录/agent_config.toml

    Returns:
        配置字典
    """
    if not path.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {path}\n"
            f"请复制 {CONFIG_EXAMPLE_PATH} 为 {CONFIG_PATH} 并填入实际值"
        )
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _get_rspeak_config(config: dict | None = None) -> dict:
    """提取 [rspeak] 子字典"""
    config = config or load_config()
    return config.get("rspeak", {})


def get_blog_path(config: dict | None = None) -> Path:
    """获取博客项目绝对路径"""
    rspeak = _get_rspeak_config(config)
    return Path(rspeak.get("blog_path", str(PROJECT_ROOT)))


def get_joplin_config(config: dict | None = None) -> dict:
    """获取 Joplin 配置"""
    return _get_rspeak_config(config).get("joplin", {})


def get_wechat_config(config: dict | None = None, account: str | None = None) -> dict:
    """获取微信公众号配置

    支持两种格式：
    1. 旧格式（单账号）：[rspeak.wechat] appid = ... appsecret = ...
    2. 新格式（多账号）：[rspeak.wechat.accounts.main] appid = ... appsecret = ...

    Args:
        config: 配置字典，None 时自动加载
        account: 账号名称，None 使用 default_account 或旧格式

    Returns:
        {"appid", "appsecret", "account_name", "name", ...}
    """
    wechat = _get_rspeak_config(config).get("wechat", {})

    # 新格式：存在 accounts 子键
    if "accounts" in wechat:
        account_name = account or wechat.get("default_account", "")
        accounts = wechat["accounts"]
        if not account_name:
            account_name = next(iter(accounts))
        if account_name not in accounts:
            available = ", ".join(accounts.keys())
            raise ValueError(f"微信账号 '{account_name}' 不存在，可用: {available}")
        acc = accounts[account_name]
        return {
            "appid": acc["appid"],
            "appsecret": acc["appsecret"],
            "access_token": acc.get("access_token", ""),
            "account_name": account_name,
            "name": acc.get("name", account_name),
        }

    # 旧格式兼容
    return {
        "appid": wechat.get("appid", ""),
        "appsecret": wechat.get("appsecret", ""),
        "access_token": wechat.get("access_token", ""),
        "account_name": "default",
        "name": "默认账号",
    }


def list_wechat_accounts(config: dict | None = None) -> list[dict]:
    """列出所有配置的微信公众号账号

    Returns:
        [{"key": "main", "name": "主账号", "appid": "wx..."}, ...]
    """
    wechat = _get_rspeak_config(config).get("wechat", {})
    if "accounts" not in wechat:
        if wechat.get("appid"):
            return [{"key": "default", "name": "默认账号", "appid": wechat["appid"]}]
        return []
    return [
        {"key": k, "name": v.get("name", k), "appid": v.get("appid", "")}
        for k, v in wechat["accounts"].items()
    ]


def get_hugo_config(config: dict | None = None) -> dict:
    """获取 Hugo 配置"""
    return _get_rspeak_config(config).get("hugo", {})


def get_deploy_config(config: dict | None = None) -> dict:
    """获取部署配置"""
    return _get_rspeak_config(config).get("deploy", {})
