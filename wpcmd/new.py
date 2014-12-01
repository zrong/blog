from wpcmd.base import Action

class NewAction(Action):

    def _new_article(self):
        postid = self.get_postid()
        if not postid:
            slog.warning('Please provide a post id!')
            return
        afile, aname = self.conf.get_draft(postid)
        html, meta = self.get_article_content(afile)

        # Update all taxonomy befor new a article.
        self.get_terms_from_wp(['category'])
        self.get_terms_from_wp(['post_tag'])

        if meta.posttype == 'page':
            post = WordPressPage()
        else:
            post = WordPressPost()

        post.content= html
        post.title = meta.title
        post.slug = meta.nicename
        post.date = meta.date
        post.user = meta.author
        post.date_modified = meta.modified
        post.post_status = meta.poststatus
        post.terms = self.get_terms_from_meta(meta.category, meta.tags)
        if not post.terms:
            slog.warning('Please provide some terms.')
            return
        postid = _wpcall(NewPost(post))

        if postid:
            write_by_templ(afile, afile, {'POSTID':postid, 'SLUG':postid})
        else:
            return

        newfile, newname = None, None
        if meta.posttype == 'page':
            newfile, newname = self.conf.get_article(post.nicename, meta.posttype)
        else:
            newfile, newname = self.conf.get_article(postid, meta.posttype)

        slog.info('Move "%s" to "%s".'%(afile, newfile))
        shutil.move(afile, newfile)

    def _new_term(self):
        if not self.args.query or len(self.args.query)<2:
            slog.error('Provide 2 arguments at least please.')
            return
        term = _get_terms_from_wp(self.args.query, force=True)
        if term:
            slog.error('The term "%s" has been in wordpress.'%self.args.query[1])
            return
        taxname = self.args.query[0]
        slug = self.args.query[1]
        name = self.args.query[2] if len(self.args.query)>2 else slug
        term = WordPressTerm()
        term.slug = slug
        term.name = name
        term.taxonomy = taxname
        if len(self.args.query)>3:
            term.description = self.args.query[3]
        termid = _wpcall(NewTerm(term))
        if not termid:
            return
        term = _wpcall(GetTerm(taxname, termid))
        if not term:
            return
        slog.info('The term %s(%s) has created.'%(name, termid))
        self.conf.save_term(term, taxname)
        self.conf.save_to_file()
        slog.info('The term %s has saved.'%name)

    def go(self):
        print(self.args)
        if self.args.type == 'draft':
            self._new_article()
        elif self.args.type == 'term':
            self._new_term()


def build(gconf, gargs, parser=None):
    action = NewAction(gconf, gargs, parser)
    action.build()

