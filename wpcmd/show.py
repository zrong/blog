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

        if self.args.query:
            return GetPost(_get_postid(), result_class=WordPressPage)
        return GetPosts(field, result_class=WordPressPage)

    def _show_post(self):
        field = {}
        field['number'] = self.args.number
        field['orderby'] = self.args.orderby
        field['order'] = self.args.order

        if self.args.query:
            return GetPost(_get_postid())
        return GetPosts(field)

    def go(self):
        print(self.args)
        method = None
        if self.args.type == 'post':
            method = self._show_post()
        elif self.args.type == 'page':
            method = self._show_page()
        elif self.args.type == 'draft':
            for adir, aname, afile in self.conf.get_mdfiles('draft'):
                slog.info(afile)
        elif self.args.type == 'option':
            method = GetOptions([])
        elif self.args.type == 'tax':
            method = GetTaxonomies()
        elif self.args.type == 'term':
            terms = self.get_terms_from_wp(self.args.query)
            if terms:
                self.print_results(terms)
            else:
                slog.warning('No term %s!'%str(self.args.query))

        if not method:
            return

        results = self.wpcall(method)
        if not results:
            slog.warning('No results for showing.')
            return

        self.print_results(results)


def build(gconf, gargs, parser=None):
    action = ShowAction(gconf, gargs, parser)
    action.build()
