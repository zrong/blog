"""rspeak CLI - 博客写作与发布工具

用法：
    uv run rspeak deploy blog        # Hugo 构建 + rsync 部署
    uv run rspeak deploy wechat -p N # 发布到微信公众号
    uv run rspeak deploy zhihu -p N  # 转为知乎格式
    uv run rspeak sync -p N          # Hugo ↔ Joplin 同步
    uv run rspeak review -p N        # 文章校对
"""

import re
import subprocess

import typer

app = typer.Typer(
    name="rspeak",
    help="博客写作与发布工具：校对、Hugo/Joplin 同步、多平台部署",
    no_args_is_help=True,
)

deploy_app = typer.Typer(
    name="deploy",
    help="部署博客到各平台",
    no_args_is_help=True,
)
app.add_typer(deploy_app, name="deploy")


# ---- deploy 子命令 ----


@deploy_app.command("blog")
def deploy_blog(
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="仅模拟运行，不实际传输"),
):
    """Hugo 构建并 rsync 部署到远程服务器"""
    from .deploy import deploy_blog as _deploy_blog

    typer.echo("开始部署博客...")
    try:
        result = _deploy_blog(dry_run=dry_run)
        typer.echo(f"Hugo 构建完成: {result['build_dir']}")
        if dry_run:
            typer.echo("[模拟运行] rsync 输出:")
        else:
            typer.echo("rsync 同步完成:")
        typer.echo(result["rsync_result"].stdout)
    except FileNotFoundError as e:
        typer.echo(f"错误: {e}", err=True)
        raise typer.Exit(1)
    except subprocess.CalledProcessError as e:
        typer.echo(f"命令执行失败: {' '.join(str(c) for c in e.cmd)}", err=True)
        if e.output:
            typer.echo(e.output, err=True)
        if e.stderr:
            typer.echo(e.stderr, err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"部署失败: {e}", err=True)
        raise typer.Exit(1)


@deploy_app.command("wechat")
def deploy_wechat(
    postid: int = typer.Option(..., "--postid", "-p", help="Hugo 文章 ID"),
):
    """将 Hugo 文章发布到微信公众号（创建草稿）"""
    from .deploy import deploy_wechat as _deploy_wechat

    typer.echo(f"正在将文章 {postid} 发布到微信公众号...")
    try:
        result = _deploy_wechat(postid)
        typer.echo("草稿创建成功！")
        typer.echo(f"标题: {result['article'].title}")
        typer.echo(f"草稿 media_id: {result['media_id']}")
        typer.echo("请登录微信公众号后台确认并发布草稿。")
    except FileNotFoundError:
        typer.echo(f"错误: 找不到文章 {postid}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"发布失败: {e}", err=True)
        raise typer.Exit(1)


@deploy_app.command("zhihu")
def deploy_zhihu(
    postid: int = typer.Option(..., "--postid", "-p", help="Hugo 文章 ID"),
):
    """将 Hugo 文章转为知乎格式（输出到终端供复制）"""
    from .deploy import deploy_zhihu as _deploy_zhihu

    try:
        text = _deploy_zhihu(postid)
        typer.echo(text)
    except FileNotFoundError:
        typer.echo(f"错误: 找不到文章 {postid}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"转换失败: {e}", err=True)
        raise typer.Exit(1)


@deploy_app.command("xiaohongshu")
def deploy_xiaohongshu():
    """小红书发布（待实现）"""
    typer.echo("小红书发布功能尚未实现，敬请期待。")
    raise typer.Exit(0)


# ---- sync 子命令 ----


@app.command("sync")
def sync(
    postid: int = typer.Option(None, "--postid", "-p", help="Hugo 文章 ID"),
    title: str = typer.Option(None, "--title", "-t", help="文章标题关键词"),
    slug: str = typer.Option(None, "--slug", "-s", help="URL slug（Joplin→Hugo 时需要）"),
):
    """Hugo 与 Joplin 之间双向同步文章"""
    if postid is None and title is None:
        typer.echo("错误: 必须提供 --postid 或 --title 之一", err=True)
        raise typer.Exit(1)

    from .config import load_config, get_joplin_config, get_hugo_config, get_deploy_config
    from .deploy import resolve_blog_root
    from .joplin import JoplinClient
    from .converter import sync_article

    config = load_config()
    joplin_conf = get_joplin_config(config)
    hugo_conf = get_hugo_config(config)
    deploy_conf = get_deploy_config(config)

    blog_root = resolve_blog_root(deploy_conf)
    content_dir = blog_root / hugo_conf.get("content_dir", "content")
    static_dir = blog_root / "static"
    notebook_path = joplin_conf.get("notebook_path", "Thought/Writing/Blog")

    with JoplinClient(
        token=joplin_conf["token"],
        base_url=joplin_conf.get("base_url", "http://localhost:41184"),
    ) as client:
        if not client.ping():
            typer.echo("错误: Joplin 服务不可用，请确认 Joplin 已启动且 Web Clipper 已开启", err=True)
            raise typer.Exit(1)

        try:
            result = sync_article(
                client=client,
                content_dir=content_dir,
                static_dir=static_dir,
                title=title,
                postid=postid,
                notebook_path=notebook_path,
                slug=slug,
            )
        except ValueError as e:
            typer.echo(f"错误: {e}", err=True)
            raise typer.Exit(1)

    action = result["action"]
    action_labels = {
        "hugo_to_joplin": "Hugo → Joplin 同步完成",
        "joplin_to_hugo": "Joplin → Hugo 同步完成",
        "already_synced": "双方内容已同步，无需操作",
        "not_found": "未找到匹配的文章",
    }
    typer.echo(action_labels.get(action, f"操作: {action}"))

    if result.get("post"):
        typer.echo(f"Hugo 文章: {result['post'].title} (postid={result['post'].postid})")
    if result.get("note"):
        typer.echo(f"Joplin 笔记: {result['note'].title} (id={result['note'].id})")


# ---- review 子命令 ----


@app.command("review")
def review(
    postid: int = typer.Option(..., "--postid", "-p", help="Hugo 文章 ID"),
):
    """校对 Hugo 文章（输出发现的问题）"""
    from .config import load_config, get_hugo_config, get_deploy_config
    from .deploy import resolve_blog_root
    from .hugo import parse_post

    config = load_config()
    hugo_conf = get_hugo_config(config)
    deploy_conf = get_deploy_config(config)

    blog_root = resolve_blog_root(deploy_conf)
    content_dir = blog_root / hugo_conf.get("content_dir", "content")

    post_file = content_dir / "post" / f"{postid}.md"
    if not post_file.exists():
        typer.echo(f"错误: 找不到文章 {postid}", err=True)
        raise typer.Exit(1)

    post = parse_post(post_file)
    typer.echo(f"校对文章: {post.title} (postid={post.postid})")
    typer.echo("=" * 60)

    issues = _check_article(post.body)

    if not issues:
        typer.echo("未发现问题，文章格式规范。")
    else:
        typer.echo(f"发现 {len(issues)} 处问题:\n")
        for i, issue in enumerate(issues, 1):
            typer.echo(f"  {i}. [{issue['category']}] 第 {issue['line']} 行")
            typer.echo(f"     {issue['description']}")
            if issue.get("suggestion"):
                typer.echo(f"     建议: {issue['suggestion']}")
            typer.echo()


def _check_article(body: str) -> list[dict]:
    """基础文章校对检查

    检查项：中英文之间缺少空格、中文标点与英文标点混用、多余空行
    """
    issues = []
    lines = body.split("\n")
    in_code_block = False

    for line_num, line in enumerate(lines, 1):
        # 跳过代码块内容
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # 中文后紧跟英文字母
        for match in re.finditer(r'([\u4e00-\u9fff])([A-Za-z])', line):
            # 跳过行内代码
            before = line[:match.start()]
            if before.count('`') % 2 == 1:
                continue
            issues.append({
                "category": "中英文混排",
                "line": line_num,
                "description": f"中文与英文之间缺少空格: ...{match.group()}...",
                "suggestion": f"{match.group(1)} {match.group(2)}",
            })

        # 英文后紧跟中文
        for match in re.finditer(r'([A-Za-z])([\u4e00-\u9fff])', line):
            before = line[:match.start()]
            if before.count('`') % 2 == 1:
                continue
            issues.append({
                "category": "中英文混排",
                "line": line_num,
                "description": f"英文与中文之间缺少空格: ...{match.group()}...",
                "suggestion": f"{match.group(1)} {match.group(2)}",
            })

        # 中文句子末尾使用英文句号
        if re.search(r'[\u4e00-\u9fff]\.(\s|$)', line):
            issues.append({
                "category": "标点符号",
                "line": line_num,
                "description": "中文句子末尾使用了英文句号",
                "suggestion": "使用中文句号「。」",
            })

        # 中文之间使用英文逗号
        if re.search(r'[\u4e00-\u9fff],[\u4e00-\u9fff]', line):
            issues.append({
                "category": "标点符号",
                "line": line_num,
                "description": "中文句子中使用了英文逗号",
                "suggestion": "使用中文逗号「，」",
            })

    # 多余空行检查
    consecutive_empty = 0
    for line_num, line in enumerate(lines, 1):
        if line.strip() == "":
            consecutive_empty += 1
            if consecutive_empty >= 3:
                issues.append({
                    "category": "格式",
                    "line": line_num,
                    "description": "连续多个空行",
                    "suggestion": "最多保留一个空行",
                })
        else:
            consecutive_empty = 0

    return issues
