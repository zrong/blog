from zrong.base import slog
from wpcmd.base import Action
from wordpress_xmlrpc import (WordPressPost, WordPressPage)
from wordpress_xmlrpc.methods.posts import (GetPosts, GetPost)
from wordpress_xmlrpc.methods.options import GetOptions
from wordpress_xmlrpc.methods.taxonomies import (GetTaxonomies)

class ShowAction(Action):

    def _show_page(self):
        field = {'post_type':'page'}
        field['number'] = self.args.number
        field['orderby'] = self.args.orderby
        field['order'] = self.args.order

        method = None
        if self.args.query:
            method = GetPost(_get_postid(), result_class=WordPressPage)
        else:
            method =  GetPosts(field, result_class=WordPressPage)
        results = self.wpcall(method)
        if results:
            self.print_results(results)
        else:
            slog.warning('No results for showing.')

    def _show_post(self):
        field = {}
        field['number'] = self.args.number
        field['orderby'] = self.args.orderby
        field['order'] = self.args.order

        method = None
        if self.args.query:
            method = GetPost(_get_postid())
        else:
            method = GetPosts(field)
        results = self.wpcall(method)
        if results:
            self.print_results(results)
        else:
            slog.warning('No results for showing.')

    def _show_options(self):
        results = self.wpcall(GetOptions([]))
        if results:
            self.print_results(results)
        else:
            slog.warning('No results for showing.')

    def _show_tax(self):
        results = self.wpcall(GetTaxonomies())
        if results:
            self.print_results(results)
        else:
            slog.warning('No results for showing.')

    def _show_term(self):
        typ = self.args.type
        q = self.args.query
        if typ == 'tag':
            typ = 'post_tag'
        info = None
        if typ == 'term':
            terms = self.get_terms_from_wp(q)
            info = str(self.args.query)
        else:
            query = [typ]
            if q and len(q)>0:
                query.append(q[0])
            terms = self.get_terms_from_wp(query)
            info = str(query)
        if terms:
            self.print_results(terms)
        else:
            slog.warning('No term %s!'%info)

    def go(self):
        print(self.args)
        if self.args.type == 'post':
            self._show_post()
        elif self.args.type == 'page':
            self._show_page()
        elif self.args.type == 'draft':
            for adir, aname, afile in self.conf.get_mdfiles('draft'):
                slog.info(afile)
        elif self.args.type == 'option':
            self._show_options()
        elif self.args.type == 'tax':
            self._show_tax()
        elif self.args.type in ('term', 'category', 'tag'):
            self._show_term()


def build(gconf, gargs, parser=None):
    action = ShowAction(gconf, gargs, parser)
    action.build()
