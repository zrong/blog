import os
import platform
import shutil
import argparse
from zrong.base import DictBase, slog, write_by_templ, list_dir

class BlogError(Exception):
    pass

class Conf(DictBase):

    def init(self, workDir, confFile):
        self.site = DictBase(
        {
            'user': 'user',
            'password': 'password',
            'url': 'http://you-wordpress-blog/xmlrpc.php',
        })
        self.directory = DictBase(
        {
            'work': workDir,
            'draft': 'draft',
            'post': 'post',
            'page': 'page',
        })
        self.files = DictBase(
        {
            'ext': '.md',
            'draftfmt': 'draft_%s',
        })
        self.save_to_file(confFile)

    def get_draft(self, name):
        draftname = (self.files.draftfmt % str(name))+self.files.ext
        draftfile = self.get_path(self.directory.draft, draftname)
        return draftname, draftfile

    def get_new_draft(self, name=None):
        draftnames = list(list_dir(self.get_path(self.directory.draft)))
        draftname, draftfile = None, None
        if name:
            draftname, draftfile = self.get_draft(name)
            if draftname in driftnames:
                raise BlogError('The draft file "%s" is already existence!')
        else:
            name = 1
            draftname, draftfile = self.get_draft(name)
            while os.path.exists(draftfile):
                name += 1
                draftname, draftfile = self.get_draft(name)
        return draftname, draftfile

    def get_post(self, name):
        return self.get_path(self.directory.post, name+self.files.ext)

    def get_page(self, name):
        return self.get_path(self.directory.page, name+self.files.ext)

    def get_path(self, name, *path):
        workdir = os.path.join(self.directory.work, name)
        if path:

            return os.path.abspath(os.path.join(
                workdir, *path))
        return workdir

def checkFTPConf(ftpConf):
    if not ftpConf \
    or not ftpConf.server \
    or not ftpConf.user \
    or not ftpConf.password:
        raise BlogError('ftpConf MUST contains following values:'
                'server,user,password !')

def check_args(argv=None):
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
        choices=['new', 'pub', 'update', 'del', 'show'], 
        default='show',
        help='Action for wordpress.')
    pp.add_argument('-t', '--type', type=str,
        choices=['post', 'page', 'option', 'tax', 'term'],
        default='option',
        help='Action for wordpress.')
    pp.add_argument('-q', '--query', nargs='*',
        help='The options for query.')
    pp.add_argument('-n', '--number', type=int,
        default=10,
        help='The amount for GetPosts.')
    pp.add_argument('-o', '--orderby',
        choices=['post_modified', 'post_id'],
        default='post_id',
        help='To sort the result-set by one column.')
    pp.add_argument('-d', '--order',
        choices=['ASC', 'DESC'],
        default='DESC',
        help='To sort the records in a descending or a ascending order.')

    args = parser.parse_args(args=argv)
    if args.sub_name:
        return args, subParsers.choices[args.sub_name]
    parser.print_help()
    return None, None
