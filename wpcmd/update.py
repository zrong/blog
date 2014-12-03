import re
from wpcmd.base import Action
from zrong.base import slog
from wordpress_xmlrpc import (WordPressPost, WordPressPage)
from wordpress_xmlrpc.methods.posts import (GetPost, EditPost)
from wordpress_xmlrpc.methods.taxonomies import (GetTerm, EditTerm)

class UpdateAction(Action):

    def _update_a_draft(self):
        postid = self.get_postid()
        if not postid:
            slog.warning('Please provide a post id!')
            return
        afile, aname = self.conf.get_draft(postid)
        html, meta, images = self.get_article_content(afile)

        if meta.poststatus == 'draft':
            slog.warning('The post status of draft "%s" is "draft", '
                'please modify it to "publish".'%postid)
            return

        # Update all taxonomy before create a new article.
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

    def _update_articles(self):
        postids = self.get_postid(as_list=True)
        if not postids:
            slog.warning('Please provide a post id!')
            return

        # Update all taxonomy before create a new article.
        self.get_terms_from_wp(['category'])
        self.get_terms_from_wp(['post_tag'])

        for postid in postids:
            self._update_a_article(postid)

    def _update_a_article(self, postid):
        afile, aname = self.conf.get_article(postid, self.args.type)
        html, meta, images = self.get_article_content(afile)

        if not html:
            return
        resultclass = WordPressPost
        if self.args.type == 'page':
            postid = meta.postid
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
        typ = 'post_tag' if self.args.type == 'tag' else self.args.type
        q = self.args.query 
        term = None
        query = [typ]
        if q and len(q) > 1:
            query.append(q[0])
            term = self.get_terms_from_wp(query, force=True)
            if not term:
                slog.error('The term %s is not existend.'%str(self.args.query))
                return
            term = self.wpcall(GetTerm(typ, term.id))
            if term:
                term.slug = q[0]
                term.name = q[1]
                if len(q)>2:
                    term.description = q[2]
                # post_get can not support parent.
                if term.taxonomy == 'post_tag':
                    term.parent = None
                issucc = self.wpcall(EditTerm(term.id, term))
                if issucc:
                    self.conf.save_term(term, typ)
                    self.conf.save_to_file()
                    slog.info('The term %s(%s) has saved.'%(term.slug, term.id))
                else:
                    slog.info('The term %s(%s) saves unsuccessfully.'%(term.slug,
                        term.id))
            else:
                slog.info('Can not get term "%s".'%typ)
        else:
            term = self.get_terms_from_wp(query, force=True)
            if term:
                slog.info('Update terms done.')
            else:
                slog.warning('No terms.')

    def go(self):
        print(self.args)
        if self.args.type == 'draft':
            self._update_a_draft()
        elif self.args.type in ('post', 'page'):
            self._update_articles()
        elif self.args.type in ('tag', 'category'):
            self._update_term()


def build(gconf, gargs, parser=None):
    action = UpdateAction(gconf, gargs, parser)
    action.build()
