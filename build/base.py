import os
import platform
import shutil
import argparse
from zrong.base import DictBase,slog,writeByTempl

class BlogError(Exception):
    pass

class Conf(DictBase):

    def init(self, workDir, confFile):
        self.work_dir = workDir
        self.readFromFile(confFile)

    def get_dir(self, name, *path):
        adir = self.work_dir
        if path:
            return os.path.abspath(os.path.join(adir, *path))
        return adir

def checkFTPConf(ftpConf):
    if not ftpConf \
    or not ftpConf.server \
    or not ftpConf.user \
    or not ftpConf.password:
        raise BlogError('ftpConf MUST contains following values:'
                'server,user,password !')

def checkArgs(argv=None):
    parser = argparse.ArgumentParser()
    subParsers = parser.add_subparsers(dest='sub_name', help='sub-commands')

    pw = subParsers.add_parser('write', 
        help='Write *.md files.')
    pw.add_argument('-a', '--all', action='store_true', 
        help='Perform all of actions.')
    pw.add_argument('-r', '--readme', action='store_true', 
        help='Build README.md.')
    pw.add_argument('-u', '--url', action='store_true', 
        help='Rewrite url.')
    pw.add_argument('-t', '--title', action='store_true', 
        help='Rewrite title.')
    pw.add_argument('-c', '--category', action='store_true', 
        help='Rewrite category.')
    pw.add_argument('-d', '--dirname', type=str, default='post',
        choices = ['post', 'page', 'draft', 'all'],
        help='Rewrite articles by type. The value is [post|page|draft|all].')

    parserRes = subParsers.add_parser('res', 
        help='Process resources.')
    parserRes.add_argument('-f', '--force', action='store_true', 
        help='Remove directory before process.')
    parserRes.add_argument('-a', '--all', action='store_true', 
        help='Process all resources.')
    parserRes.add_argument('-l', '--plst', type=str, nargs='*',
        help='Process picture plist files.')
    parserRes.add_argument('-d', '--pdir', type=str, nargs='*',
        help='Process picture dir files.')
    parserRes.add_argument('-r', '--arm', type=str, nargs='*',
        help='Process armature files.')
    parserRes.add_argument('-n', '--fnt', type=str, nargs='*',
        help='Process font files.')
    parserRes.add_argument('-p', '--par', type=str, nargs='*',
        help='Process particle files.')
    parserRes.add_argument('-s', '--snd', type=str, nargs='*',
        help='Process sound files.')
    parserRes.add_argument('-i', '--ani', type=str, nargs='*',
        help='Process animation files.')
    parserRes.add_argument('--lang', type=str, 
            default='zh_cn', choices=['zh_cn'],
        help='Process specified language.')
    parserRes.add_argument('--density', type=str, 
            default='sd', choices=['sd'],
        help='Process specified density.')
    parserRes.add_argument('--vendor', type=str, 
            default='team1201', choices=['team1201'],
        help='Process specified vendor.')

    args = parser.parse_args(args=argv)
    if args.sub_name:
        return args, subParsers.choices[args.sub_name]
    parser.print_help()
    return None, None
