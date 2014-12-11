import shutil
import datetime
from zrong.base import slog, write_by_templ
from wpcmd.base import Action,BlogError
from wordpress_xmlrpc import (WordPressTerm)
from wordpress_xmlrpc.methods.taxonomies import (NewTerm,GetTerm)

class NewAction(Action):

    def _new_draft(self):
        name = None
        if self.args.query:
            name = self.args.query[0]
        try:
            dfile, dname = self.conf.get_new_draft(name)
        except BlogError as e:
            slog.critical(e)
            return
        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        subdict = {
                'TITLE':'',
                'DATE':dt,
                'MODIFIED':dt,
                'AUTHOR':self.conf.site.user,
                'NICENAME':'',
                'CATEGORY':'technology',
                'TAG':'',
                'POSTTYPE':self.args.type,
                'POSTSTATUS':'draft',
                }
        write_by_templ(self.conf.get_path('templates', 'article.md'), 
                dfile,
                subdict,
                True)
        slog.info('The draft file "%s" has created.'%dfile)

    def _new_term(self):
        if not self.args.query or len(self.args.query)<1:
            slog.error('Provide 1 arguments at least please.')
            return
        query = self.get_term_query()
        print('query:', query)
        term = self.get_terms_from_wp(query, force=True)
        print(term)
        if term:
            slog.error('The term "%s" has been in wordpress.'%self.args.query[0])
            return
        taxname = query[0]
        slug = self.args.query[0]
        name = self.args.query[1] if len(self.args.query)>1 else slug
        term = WordPressTerm()
        term.slug = slug
        term.name = name
        term.taxonomy = taxname
        if len(self.args.query)>2:
            term.description = self.args.query[2]
        termid = self.wpcall(NewTerm(term))
        if not termid:
            return
        term = self.wpcall(GetTerm(taxname, termid))
        if not term:
            return
        slog.info('The term %s(%s) has created.'%(name, termid))
        self.conf.save_term(term, taxname)
        self.conf.save_to_file()
        slog.info('The term %s has saved.'%name)

    def go(self):
        print(self.args)
        if self.args.type in ('post','page'):
            self._new_draft()
        elif self.args.type in ('category', 'tag'):
            self._new_term()


def build(gconf, gargs, parser=None):
    action = NewAction(gconf, gargs, parser)
    action.build()

