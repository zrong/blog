import os
import re
import mimetypes
from xmlrpc.client import Binary
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from zrong.base import DictBase, slog, read_file, write_file, write_by_templ
from wpcmd.base import Action
from wordpress_xmlrpc import (WordPressPost, WordPressPage)
from wordpress_xmlrpc.methods.posts import (GetPost, EditPost, NewPost)
from wordpress_xmlrpc.methods.media import (UploadFile)
from wordpress_xmlrpc.methods.taxonomies import (GetTerm, EditTerm)

class UpdateAction(Action):

    def _get_article_metadata(self, meta):
        adict = DictBase()
        adict.title = meta['title'][0]
        adict.postid = meta['postid'][0]
        adict.nicename = meta['nicename'][0]
        adict.slug = meta['slug'][0]
        adict.date = self.get_datetime(meta['date'][0])
        adict.author = meta['author'][0]
        tags = meta.get('tags')
        if tags:
            adict.tags = [tag.strip() for tag in tags[0].split(',')]
        category = meta.get('category')
        if category:
            adict.category = [cat.strip() for cat in category[0].split(',')]
        modified = meta.get('modified')
        if modified:
            adict.modified = self.get_datetime(modified[0])
        posttype = meta.get('posttype')
        if posttype:
            adict.posttype = posttype[0]
        else:
            adict.posttype = 'post'
        poststatus = meta.get('poststatus')
        if poststatus:
            adict.poststatus = poststatus[0]
        else:
            adict.poststatus = 'publish'
        attachments = meta.get('attachments')
        if attachments:
            adict.attachments = [att.strip() for att in attachments[0].split(',')]
        return adict

    def _get_article_content(self, afile, istxt=False):
        txt = None
        if istxt:
            txt = afile
        else:
            if not os.path.exists(afile):
                slog.error('The file "%s" is inexistance!'%afile)
                return None, None
            txt = read_file(afile)
            md = markdown.Markdown(extensions=[
                'markdown.extensions.meta',
                'markdown.extensions.tables',
                CodeHiliteExtension(linenums=False, guess_lang=False),
                ])

        html = md.convert(txt)
        meta = md.Meta

        adict = self._get_article_metadata(meta)
        return html,adict,txt,self._get_images(txt)

    def _get_images(self, txt):
        return re.findall(u'image/\d{4}/\d{2}/.*', txt, re.M)

    def _update_a_draft(self):
        postid = self.get_postid()
        if not postid:
            slog.warning('Please provide a post id!')
            return
        afile, aname = self.conf.get_draft(postid)
        html, meta, txt, images = self._get_article_content(afile)

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
        postid = self.wpcall(NewPost(post))

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
        html, meta, txt, medias = self._get_article_content(afile)
        if medias and not meta.attachments:
            txt = self._update_medias(medias, txt)
            write_file(afile, txt)
            html, meta, txt, medias = self._get_article_content(txt, True)
            if medias:
                slog.error('Medias in the article is maybe wrong!')
                return

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

    def _update_medias(self, medias, txt):
        slog.info('Ready for upload some medias to WordPress.')
        attach_ids = []
        for media in medias:
            bits = None
            with open(self.conf.get_path(media), 'rb') as m:
                    bits = Binary(m.read()).data
            amedia = {}
            amedia['name'] = os.path.split(media)[1]
            amedia['type'] = mimetypes.guess_type(media)[0]
            amedia['bits'] = bits
            upd = self.wpcall(UploadFile(amedia))
            txt = txt.replace(media, upd['url'])
            attach_ids.append(upd['id'])
        # Add attachments to the TOF.
        txt = 'Attachments: %s\n%s'%s(','.join(attach_ids), txt)
        return txt

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
        #print(self.args)
        if self.args.type == 'draft':
            self._update_a_draft()
        elif self.args.type in ('post', 'page'):
            self._update_articles()
        elif self.args.type in ('tag', 'category'):
            self._update_term()


def build(gconf, gargs, parser=None):
    action = UpdateAction(gconf, gargs, parser)
    action.build()
