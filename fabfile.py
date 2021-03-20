# -*- coding: utf-8 -*-

import logging
import sys
from fabric import task, Connection
from invoke.exceptions import Exit


logger = logging.Logger('fabric', level=logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


class Tmux(object):
    """Tmux helper for fabric 2"""
    def __init__(self, runner, session_name='default'):
        self.session_name = session_name
        self.run_cmd = runner.run

        self.create_session()

    def create_session(self):
        test = self.run_cmd('tmux has-session -t %s' % self.session_name, warn=True)

        if test.failed:
            self.run_cmd('tmux new-session -d -s %s' % self.session_name)

        self.run_cmd(
            'tmux set-option -t %s -g allow-rename off' % self.session_name)

    def recreate(self):
        self.kill_session()
        self.create_session()

    def kill_session(self):
        self.run_cmd('tmux kill-session -t %s' % self.session_name)

    def command(self, command, pane=0):
        self.run_cmd('tmux send-keys -t %s:%s "%s" ENTER' % (
            self.session_name, pane, command))

    def new_window(self, name):
        self.run_cmd('tmux new-window -t %s -n %s' % (self.session_name, name))

    def find_window(self, name):
        test = self.run_cmd('tmux list-windows -t %s | grep \'%s\'' % (self.session_name, name), warn=True)

        return test.ok

    def rename_window(self, new_name, old_name=None):
        if old_name is None:
            self.run_cmd('tmux rename-window %s' % new_name)
        else:
            self.run_cmd('tmux rename-window -t %s %s' % (old_name, new_name))

    def wait_for(self, signal_name):
        self.run_cmd('tmux wait-for %s' % signal_name)

    def run_singleton(self, command, orig_name, wait=True):
        run_name = "run/%s" % orig_name
        done_name = "done/%s" % orig_name

        # If the program is running we wait to be finished.
        if self.find_window(run_name):
            self.wait_for(run_name)

        # If the program is not running we create a window with done_name
        if not self.find_window(done_name):
            self.new_window(done_name)

        self.rename_window(run_name, done_name)

        # Check that we can execute the commands in the correct window
        assert self.find_window(run_name)

        rename_window_cmd = 'tmux rename-window -t %s %s' % (
            run_name, done_name)
        signal_cmd = 'tmux wait-for -S %s' % run_name

        expanded_command = '%s ; %s ; %s' % (
            command, rename_window_cmd, signal_cmd)
        self.command(expanded_command, run_name)

        if wait:
            self.wait_for(run_name)


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
    git_dir = '$HOME/blog'
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
