import os
import re
import markdown
import shutil
from zrong.base import read_file, slog, list_dir
from wpcmd.base import Action

class WriteAction(Action):

    def _write_list(self, adir, rf):
        rf.write('# '+adir+'\n\n')
        is_post = adir == 'post'
        names = []
        for adir, name, fpath in self.conf.get_mdfiles(adir):
            if is_post:
                names.append(int(name))
            else:
                names.append(name)
        if is_post:
            names = sorted(names)
        for name in names:
            self._write_a_file(adir, str(name), rf)
        rf.write('\n')

    def _write_a_file(self, adir, name, rf):
        with open(os.path.join(adir, str(name)+'.md'), 'r', encoding='utf-8') as f:
            fmt = '1. %s \[**%s**\] [%s](http://zengrong.net/post/%s.htm)\n'
            time = None
            title = None
            for line in f:
                if line.startswith('Title:'):
                    title = line[6:].strip()
                elif line.startswith('Date:'):
                    time = line[6:16]
                    break
            if time and title:
                title = title.replace('_', r'\_')
                rf.write(fmt%(time, name, title, name))


    def _write_readme(self):
        with open('README.md', 'w', encoding='utf-8', newline='\n') as f:
            f.write("[zrong's blog](http://zengrong.net) 中的所有文章\n")
            f.write('==========\n\n')
            f.write("----------\n\n")
            self._write_list('page', f)
            self._write_list('post', f)

    def _rewrite_url(self, dirname):
        """
        Get wrong URL form articles, then convert them to a correct pattern.
        """

        url = re.compile(r'\]\(/\?p=(\d+)\)', re.S)
        for adir, name, fpath in self.conf.get_mdfiles(dirname):
            content = None
            fpath = os.path.join(adir, afile)
            with open(fpath, 'r', encoding='utf-8', newline='\n') as f:
                content = f.read()
                matchs = url.findall(content)
                if len(matchs) > 0:
                    print(afile, matchs)
                    for num in matchs:
                        content = content.replace('](/?p=%s'% num,
                                '](http://zengrong.net/post/%s.htm'%num)
                else:
                    content = None
            if content:
                with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(content)
                    print(fpath)

    def _rewrite_category(self):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.meta',
            ])
        num = 0
        for adir,name,fpath in self.conf.get_mdfiles('post'):
            md.convert(read_file(fpath))
            cats = [cat.strip() for cat in md.Meta['category'][0].split(',')]
            if len(cats)>1:
                print(name, cats)
                num = num + 1
        print(num)

    def _write_analytic(self):
        if args.name:
            match = re.match(r'^(\d*)-(\d*)$', args.name)
            a,b = None,None
            if match:
                if match.group(1):
                    a = int(match.group(1))
                if match.group(2):
                    b = int(match.group(2))
                dirlist = []
                for f in list_dir(conf.get_path(args.dirname)):
                    if not f.endswith('.md'):
                        continue
                    fname = int(f.split('.')[0])
                    if a != None:
                        if fname < a:
                            continue
                    if b != None:
                        if fname > b:
                            continue
                    dirlist.append(fname)
                abc = sorted(dirlist)
                slog.info('\n'.join([str(item) for item in sorted(dirlist)]))

    # rewrite Action._update_site_config
    def _update_site_config(self):
        pass

    def build(self):
        print(self.args)
        noAnyArgs = True
        if self.args.readme:
            self._write_readme()
            noAnyArgs = False
        if self.args.category:
            self._rewrite_category()
            noAnyArgs = False
        if self.args.analytic:
            _write_analytic()
            noAnyArgs = False

        if noAnyArgs and self.parser:
            self.parser.print_help()

def build(gconf, gargs, parser=None):
    action = WriteAction(gconf, gargs, parser)
    action.build()
