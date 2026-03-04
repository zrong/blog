"""配置文件加载

配置文件路径：tools/rspeak/config.toml
从 config.example.toml 复制并填入实际值。
"""

from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


# 配置文件在项目根目录（tools/rspeak/），而非 Python 包目录（tools/rspeak/rspeak/）
CONFIG_DIR = Path(__file__).parent.parent
CONFIG_PATH = CONFIG_DIR / "config.toml"
CONFIG_EXAMPLE_PATH = CONFIG_DIR / "config.example.toml"


def load_config(path: Path = CONFIG_PATH) -> dict:
    """加载配置文件

    Args:
        path: 配置文件路径，默认为 tools/rspeak/config.toml

    Returns:
        配置字典
    """
    if not path.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {path}\n"
            f"请复制 {CONFIG_EXAMPLE_PATH} 为 {CONFIG_PATH} 并填入实际值"
        )
    return tomllib.loads(path.read_text(encoding="utf-8"))


def get_joplin_config(config: dict | None = None) -> dict:
    """获取 Joplin 配置"""
    config = config or load_config()
    return config.get("joplin", {})


def get_wechat_config(config: dict | None = None, account: str | None = None) -> dict:
    """获取微信公众号配置

    支持两种格式：
    1. 旧格式（单账号）：[wechat] appid = ... appsecret = ...
    2. 新格式（多账号）：[wechat.accounts.main] appid = ... appsecret = ...

    Args:
        config: 配置字典，None 时自动加载
        account: 账号名称，None 使用 default_account 或旧格式

    Returns:
        {"appid", "appsecret", "account_name", "name", ...}
    """
    config = config or load_config()
    wechat = config.get("wechat", {})

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
    config = config or load_config()
    wechat = config.get("wechat", {})
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
    config = config or load_config()
    return config.get("hugo", {})


def get_deploy_config(config: dict | None = None) -> dict:
    """获取部署配置"""
    config = config or load_config()
    return config.get("deploy", {})
