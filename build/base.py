import os
import platform
import shutil
import argparse
from zrong.base import DictBase, list_dir
from wordpress_xmlrpc import (WordPressTerm)

class BlogError(Exception):
    pass

class Conf(DictBase):

    ARTICLE_TYPES = ('post', 'page', 'draft')

    def save_to_file(self):
        super().save_to_file(self.conffile)

    def init(self, workDir, confFile):
        self.confile = confFile
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
        self.save_to_file()

    def save_terms(self, terms, taxname):
        termdict = DictBase()
        for term in terms:
            self.save_term(term, taxname, termdict)
        self[taxname] = termdict
        self.save_to_file()

    def save_term(self, term, taxname, termdict=None):
        if termdict == None:
            termdict = self[taxname]
        termdict[term.slug] = DictBase({
            'id':term.id,
            'group':term.group,
            'taxonomy':term.taxonomy,
            'taxonomy_id':term.taxonomy_id,
            'name':term.name,
            'slug':term.slug,
            'description':term.description,
            'parent':term.parent,
            'count':term.count,
                })

    def get_term(self, taxname, slug):
        if not self[taxname]:
            return None
        if not self[taxname][slug]:
            return None
        termdict = self[taxname][slug]
        term = WordPressTerm()
        term.id = termdict['id']
        term.group = termdict['group']
        term.taxonomy = termdict['taxonomy']
        term.taxonomy_id = termdict['taxonomy_id']
        term.name = termdict['name']
        term.slug = termdict['slug']
        term.description = termdict['description']
        term.parent = termdict['parent']
        term.count = termdict['count']
        return term

    def is_article(self, posttype):
        return posttype in Conf.ARTICLE_TYPES

    def get_draft(self, name):
        """
        There are two kind of draft file in draft directory.
        One has published to wordpress and in draft status;
        One has beed not published to wordpress yet.
        """
        draftname = (self.files.draftfmt % str(name))+self.files.ext
        return self.get_path(self.directory.draft, draftname), draftname

    def get_new_draft(self, name=None):
        draftnames = list(list_dir(self.get_path(self.directory.draft)))
        draftfile, draftname = None, None
        if name:
            draftfile, draftname = self.get_draft(name)
            if draftname in draftnames:
                raise BlogError('The draft file "%s" is already existence!')
        else:
            name = 1
            draftfile, draftname = self.get_draft(name)
            while os.path.exists(draftfile):
                name += 1
                draftfile, draftname = self.get_draft(name)
        return draftfile, draftname

    def get_article(self, name, posttype):
        postname = name+self.files.ext
        if self.is_article(posttype):
            return self.get_path(self.directory[posttype], postname), postname
        return None, None

    def get_path(self, name, *path):
        workdir = os.path.join(self.directory.work, name)
        if path:
            return os.path.abspath(os.path.join(workdir, *path))
        return workdir

    def get_mdfiles(self, posttype):
        for afile in os.listdir(self.get_path(posttype)):
            if afile.endswith('.md'):
                name = afile.split('.')[0]
                yield (posttype, name, os.path.join(posttype, afile))


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
    pw.add_argument('-r', '--readme', action='store_true', 
        help='Build README.md.')
    pw.add_argument('-u', '--url', action='store_true', 
        help='Rewrite url.')
    pw.add_argument('-c', '--category', action='store_true', 
        help='Rewrite category.')
    pw.add_argument('-d', '--dirname', type=str, default='post',
        choices = ['post', 'page', 'draft', 'all'],
        help='Rewrite articles by type. The value is [post|page|draft|all].')
    pw.add_argument('-n', '--new', action='store_true',
        help='Create a new blog article in draft.')
    pw.add_argument('-a', '--analytic', action='store_true',
        help='Analytic the articles.')
    pw.add_argument('--name', type=str,
        help='Provide a article name.')

    pp = subParsers.add_parser('wp', 
        help='Publish blog to wordpress.')
    pp.add_argument('-u', '--user', type=str, 
        help='Login username.')
    pp.add_argument('-p', '--password', type=str, 
        help='Login password.')
    pp.add_argument('-s', '--site', type=str, 
        help='Site url.')
    pp.add_argument('-c', '--action', type=str,
        choices=['new', 'update', 'del', 'show'], 
        default='show',
        help='Action for wordpress.')
    pp.add_argument('-t', '--type', type=str,
        choices=['post', 'page', 'draft', 'option', 'tax', 'term'],
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
