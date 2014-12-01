from wpcmd.base import Action
from zrong.base import slog

class UpdateAction(Action):

    def _update_article(self):
        postids = self.get_postid(as_list=True)
        if not postids:
            slog.warning('Please provide a post id!')
            return

        # Update all taxonomy
        self.get_terms_from_wp(['category'])
        self.get_terms_from_wp(['post_tag'])

        for postid in postids:
            _update_a_article(postid)

    def _update_a_article(self, postid):
        afile, aname = self.conf.get_article(postid, self.args.type)
        html, meta = self.get_article_content(afile)
        if not html:
            return
        resultclass = WordPressPost
        if self.args.type == 'page':
            postid = meta.postid
            resultclass = WordPressPage
        elif self.args.type == 'draft':
            postid = meta.postid
            if meta.post_type == 'page':
                resultclass = WordPressPage

        post = self.wpcall(GetPost(postid, result_class=resultclass))
        if not post:
            slog.warning('No post "%s"!'%postid)
            return
        slog.info('Old article:')
        self.print_results(post)
        post.title = meta.title
        post.user = meta.author
        post.slug = meta.nicename
        post.date = meta.date
        post.content = html
        post.post_status = meta.poststatus
        if meta.modified:
            post.date_modified = meta.modified

        terms = self.get_terms_from_meta(meta.category, meta.tags)
        if terms:
            post.terms = terms
        elif self.args.type == 'post':
            slog.warning('Please provide some terms.')
            return

        succ = self.wpcall(EditPost(postid, post))
        if succ == None:
            return
        if succ:
            slog.info('Update %s successfully!'%postid)
        else:
            slog.info('Update %s fail!'%postid)

    def _update_term(self):
        term = self.get_terms_from_wp(self.args.query, force=True)
        if len(self.args.query) > 2:
            if not term:
                slog.error('The term %s is not existend.'%str(self.args.query))
                return
            taxname = self.args.query[0]
            term = self.wpcall(GetTerm(taxname, term.id))
            if term:
                term.slug = self.args.query[1]
                term.name = self.args.query[2]
                if len(self.args.query)>3:
                    term.description = self.args.query[3]
                # post_get can not support parent.
                if term.taxonomy == 'post_tag':
                    term.parent = None
                issucc = self.wpcall(EditTerm(term.id, term))
                if issucc:
                    self.conf.save_term(term, taxname)
                    self.conf.save_to_file()
                    slog.info('The term %s(%s) has saved.'%(term.slug, term.id))
                else:
                    slog.info('The term %s(%s) saves unsuccessfully.'%(term.slug,
                        term.id))
            else:
                slog.info('Can not get term "%s".'%self.args.query[1])
        else:
            if term:
                slog.info('Update terms done.')
            else:
                slog.warning('No terms.')

    def go(self):
        print(self.args)
        if self.conf.is_article(self.args.type):
            self._update_article()
        elif self.args.type == 'term':
            self._update_term()


def build(gconf, gargs, parser=None):
    action = UpdateAction(gconf, gargs, parser)
    action.build()
