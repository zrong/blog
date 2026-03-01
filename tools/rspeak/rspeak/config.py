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


def get_wechat_config(config: dict | None = None) -> dict:
    """获取微信公众号配置"""
    config = config or load_config()
    return config.get("wechat", {})


def get_hugo_config(config: dict | None = None) -> dict:
    """获取 Hugo 配置"""
    config = config or load_config()
    return config.get("hugo", {})


def get_deploy_config(config: dict | None = None) -> dict:
    """获取部署配置"""
    config = config or load_config()
    return config.get("deploy", {})
