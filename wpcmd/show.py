from zrong.base import slog
from wpcmd.base import Action
from wordpress_xmlrpc import (WordPressPost, WordPressPage)
from wordpress_xmlrpc.methods.posts import (GetPosts, GetPost)
from wordpress_xmlrpc.methods.options import GetOptions
from wordpress_xmlrpc.methods.taxonomies import (GetTaxonomies)
from wordpress_xmlrpc.methods.media import (GetMediaLibrary, GetMediaItem)

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
        query = self.get_term_query()
        info = str(query)
        terms = self.get_terms_from_wp(query)
        if terms:
            self.print_results(terms)
        else:
            slog.warning('No term %s!'%info)

    def _show_medialib(self):
        field = {}
        field['number'] = self.args.number
        extra = self.get_dict_from_query(self.args.query)
        if extra:
            for k,v in extra.items():
                field[k] = v
        print(field)
        results = self.wpcall(GetMediaLibrary(field))
        if results:
            self.print_results(results)
        else:
            slog.warning('No results for showing.')

    def _show_mediaitem(self):
        if not self.args.query or len(self.args.query) == 0:
            slog.error('Please provide a attachment_id!')
            return
        result = self.wpcall(GetMediaItem(self.args.query[0]))
        if result:
            self.print_result(result)
        else:
            slog.warning('No results for showing.')

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
        elif self.args.type == 'medialib':
            self._show_medialib()
        elif self.args.type == 'mediaitem':
            self._show_mediaitem()


def build(gconf, gargs, parser=None):
    action = ShowAction(gconf, gargs, parser)
    action.build()
