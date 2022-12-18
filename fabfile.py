# -*- coding: utf-8 -*-

import logging
import sys
from fabric import task, Connection
from invoke.exceptions import Exit
from pyape.builder.fabric import Tmux
from pyape.config import GlobalConfig
import tomli


logger = logging.Logger('fabric', level=logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


@task
def test_tmux(c):
    t = Tmux('session', runner=c)
    t.run_singleton('sleep 10', 'sleeping')


SITE_WEBROOT = '/srv/www/blog.zengrong.net'
GIT_URI = 'git@github.com:zrong/blog.git'


@task
def deploy_sync(c, nopull=False):
    """ 使用 fabric 的远程调用功能同步执行部署，命令行会一直等待执行结束
    :param nopull: 默认会执行 git pull，若提供此参数则不执行
    """
    if not isinstance(c, Connection):
        raise Exit('Use -H to provide a host!')
    logger.warning('conn: %s', c)
    git_dir = '$HOME/blog.git'
    hugo_cache_dir = f'{git_dir}/hugo_cache'
    cmd = f'test -e {git_dir}'
    logger.warning(cmd)
    r = c.run(cmd, warn=True)
    if r.ok:
        hugo_cmd = f'cd {git_dir} && hugo --cacheDir {hugo_cache_dir} -d {SITE_WEBROOT}'
        if nopull:
            cmd = hugo_cmd 
        else:
            cmd_list = [
                f'git -C {git_dir} reset --hard',
                f'git -C {git_dir} pull origin master',
                f'git -C {git_dir} submodule update',
                hugo_cmd
            ]
            cmd = ' && '.join(cmd_list)
        logger.warning(cmd)
        r = c.run(cmd, warn=True)
    else:
        cmd = f'git clone --recursive {GIT_URI} $HOME/blog'
        logger.warning(cmd)
        r = c.run(cmd, warn=True)


@task
def deploy_tmux(c):
    """ 调用 tmux 异步执行部署，命令行会立即返回
    """
    if not isinstance(c, Connection):
        raise Exit('Use -H to provide a host!')
    logger.warning('conn: %s', c)
    git_dir = '$HOME/blog'
    hugo_cache_dir = '{0}/hugo_cache'.format(git_dir)
    r = c.run('test -e ' + git_dir, warn=True)
    logger.warning('r: %s', r.command)
    t = Tmux(c, 'blog')
    if r.ok:
        cmd_list = [
            'git -C {0} reset --hard'.format(git_dir),
            'git -C {0} pull origin master'.format(git_dir),
            'git -C {0} submodule update'.format(git_dir),
            'cd {0}'.format(git_dir),
            'hugo --cacheDir {0} -d {1}'.format(hugo_cache_dir, SITE_WEBROOT)
        ]
        t.run_singleton(' && '.join(cmd_list), 'hugo', wait=False)
    else:
        t.run_singleton('git clone --recursive {0} $HOME/blog'.format(GIT_URI), 'git', wait=False)


from pathlib import Path
import re
FIRST_IMG = re.compile(r'\/uploads\/20\d{2}\/\d{2}\/\w+\.(jpg|png)')


def _fill_thumb_line(f):
    linenum = 0
    lines = f.readlines()
    insert_linenum = 0
    thumb_image = None
    for line in lines:
        logger.info(f'readline {linenum}: {line}')
        if line.startswith('thumbnail'):
            logger.info(f'包含 thumbnali， 跳过')
            break
        elif line.startswith('+++'):
            # 如果已经找到这里，代表，没有 thumbnail，记录待插入的行
            if linenum > 1:
                insert_linenum = linenum
        else:
            matchobj = FIRST_IMG.search(line)
            if matchobj is not None:
                logger.info(matchobj)
                thumb_image = matchobj.group(0)
                break
        linenum += 1
    if insert_linenum > 0 and thumb_image is not None:
        lines.insert(insert_linenum, f'thumbnail = "{thumb_image}"\n')
        return lines
    return None


@task
def fix_thumbnail(c):
    """ 查询每篇文章中是否有图像文件，若有则将其作为文章的 thumbnail 
    """
    all_md_files = list(Path(__file__).parent.joinpath('content/post/').glob('*.md'))
    # 排序，最新文件在前
    all_md_files.sort(key=lambda path: int(path.name[:-3]), reverse=True)
    # 处理 这么数量的文件
    consume = 900
    # 从第几个文件开始
    i = 0
    end = i + consume
    if end > len(all_md_files):
        end = len(all_md_files)
    while i < end:
        f = all_md_files[i]
        logger.info('=' * 14 + f'\n处理文件{i}: {f.name}')

        f = open(all_md_files[i])
        new_lines = _fill_thumb_line(f)
        f.close()

        if new_lines:
            f = open(all_md_files[i], 'w')
            f.writelines(new_lines)
            f.close()
        i += 1


@task
def build_stark_config(c):
    """ 构建 stark 需要的配置文件。
    由于 stark 生成的索引文件高达 350M+，放弃使用 stark。
    """
    gconf = GlobalConfig(Path(__file__).parent)
    stark_input_files = []
    for d in (gconf.getdir('content/post'), gconf.getdir('content/page')):
        flist = list(d.glob('*.md'))
        is_post = d.name == 'post'
        # 对于 post 根据编号来排序
        if is_post:
            flist.sort(key=lambda f: int(f.name.split('.')[0]))
        for f in flist:
            s = f.read_text()
            # 找到 +++ 的开头和结尾
            first = s.find('+++')
            end = s.find('+++', 3)

            front_matter_s = s[first+3: end]
            front_matter = tomli.loads(front_matter_s)
            # print(front_matter['slug'], front_matter['title'], front_matter['postid'])
            stark_input_files.append({
                'path': f'{d.name}/{f.name}',
                'url': f'post/{front_matter["slug"]}/' if is_post else f'{front_matter["slug"]}/',
                'title': front_matter['title'],
                'filetype': "Markdown",
            })
    stark_input = {
        'base_directory': 'content',
        'url_prefix': 'https://blog.zengrong.net/',
        'files': stark_input_files,
        'stemming': 'None',
    }
    gconf.write('stark_conf.toml', {'input': stark_input})

