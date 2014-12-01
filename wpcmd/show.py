from wpcmd.base import Action

class ShowAction(Action):

    def _wp_show(self):
        method = None
        if self.args.type == 'post':
            method = _wp_show_post()
        elif self.args.type == 'page':
            method = _wp_show_page()
        elif self.args.type == 'draft':
            for adir, aname, afile in self.conf.get_mdfiles('draft'):
                slog.info(afile)
        elif self.args.type == 'option':
            method = GetOptions([])
        elif self.args.type == 'tax':
            method = GetTaxonomies()
        elif self.args.type == 'term':
            terms = _get_terms_from_wp(self.args.query)
            if terms:
                _print_results(terms)
            else:
                slog.warning('No term %s!'%str(self.args.query))

        if not method:
            return

        results = self.wpcall(method)
        if not results:
            slog.warning('No results for showing.')
            return

        _print_results(results)

    def _wp_show_page(self):
        field = {'post_type':'page'}
        field['number'] = self.args.number
        field['orderby'] = self.args.orderby
        field['order'] = self.args.order

        if self.args.query:
            return GetPost(_get_postid(), result_class=WordPressPage)
        return GetPosts(field, result_class=WordPressPage)

    def _wp_show_post(self):
        field = {}
        field['number'] = self.args.number
        field['orderby'] = self.args.orderby
        field['order'] = self.args.order

        if self.args.query:
            return GetPost(_get_postid())
        return GetPosts(field)

def build(gconf, gargs, parser=None):
    action = ShowAction(gconf, gargs, parser)
    action.build()
