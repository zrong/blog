"""CLI 入口"""

from __future__ import annotations

import sys
from typing import Optional

import typer


def _lazy_provider():
    from imggen import provider

    return provider


app = typer.Typer(name="imggen", help="AI 图片生成工具")


@app.command("list")
def list_providers():
    """列出已配置的 provider 及端点"""
    try:
        from imggen.config import list_providers as _list

        providers = _list()
        if not providers:
            typer.echo("未配置任何 provider")
            return
        for p in providers:
            default = " (默认)" if p["is_default"] else ""
            typer.echo(f"  {p['key']}: {p['name']}{default}")
            for ep in p["endpoints"]:
                model = f"model={ep['default_model']}" if ep.get("default_model") else ""
                typer.echo(f"    [{ep['type']}] {ep['base_url']} {model}")
    except Exception as e:
        typer.echo(f"错误: {e}", err=True)
        sys.exit(1)


@app.command("models")
def models(
    provider: Optional[str] = typer.Option(None, "-p", "--provider", help="Provider 名称"),
    endpoint: Optional[str] = typer.Option(None, "-e", "--endpoint", help="Endpoint 类型 (openai/gemini)"),
):
    """从 API 获取可用模型列表"""
    try:
        from imggen.config import get_endpoint_config

        cfg = get_endpoint_config(provider, endpoint)
        typer.echo(f"Provider: {cfg['name']} ({cfg['provider_key']})")
        typer.echo(f"Endpoint: {cfg['type']} ({cfg['base_url']})")
        typer.echo("获取模型列表...")
        prov = _lazy_provider()
        model_list = prov.fetch_models(cfg)
        typer.echo(f"共 {len(model_list)} 个模型：")
        for m in model_list:
            typer.echo(f"  {m}")
    except Exception as e:
        typer.echo(f"错误: {e}", err=True)
        sys.exit(1)


@app.command("generate")
def generate(
    prompt: str = typer.Argument(..., help="图片描述"),
    provider: Optional[str] = typer.Option(None, "-p", "--provider", help="Provider 名称"),
    endpoint: Optional[str] = typer.Option(None, "-e", "--endpoint", help="Endpoint 类型 (openai/gemini)"),
    model: Optional[str] = typer.Option(None, "-m", "--model", help="模型名称"),
    size: str = typer.Option("1024x1024", "-s", "--size", help="图片尺寸 (如 1024x1024)"),
    output: Optional[str] = typer.Option(None, "-o", "--output", help="输出文件路径"),
    n: int = typer.Option(1, "-n", "--n", help="生成数量"),
):
    """生成图片"""
    try:
        from imggen.config import get_endpoint_config

        cfg = get_endpoint_config(provider, endpoint)
        model_name = model or cfg.get("default_model", "")
        typer.echo(f"Provider: {cfg['name']} ({cfg['provider_key']})")
        typer.echo(f"Endpoint: {cfg['type']} ({cfg['base_url']})")
        typer.echo(f"模型: {model_name}")
        typer.echo(f"尺寸: {size}")
        typer.echo(f"Prompt: {prompt}")
        typer.echo("生成中...")
        prov = _lazy_provider()
        saved = prov.generate_image(
            prompt=prompt,
            provider_config=cfg,
            model=model_name,
            size=size,
            output=output,
            n=n,
        )
        typer.echo("生成完成！保存到：")
        for path in saved:
            typer.echo(f"  {path}")
    except Exception as e:
        typer.echo(f"错误: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    app()
