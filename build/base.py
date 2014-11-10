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

    pp = subParsers.add_parser('wp', 
        help='Publish blog to wordpress.')
    pp.add_argument('-u', '--user', type=str, 
        help='Login username.')
    pp.add_argument('-p', '--password', type=str, 
        help='Login password.')
    pp.add_argument('-s', '--site', type=str, 
        help='Site url.')
    pp.add_argument('-c', '--action', type=str,
        choices=['pub'], 
        help='Action for wordpress.')

    args = parser.parse_args(args=argv)
    if args.sub_name:
        return args, subParsers.choices[args.sub_name]
    parser.print_help()
    return None, None
