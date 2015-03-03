import os
import re
import mimetypes
import shutil
from string import Template
from xmlrpc.client import Binary
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import (FencedCodeExtension,
        FencedBlockPreprocessor)
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
                return None, None, None, None
            txt = read_file(afile)

        FencedBlockPreprocessor.FENCED_BLOCK_RE = re.compile(r'''
(?P<fence>^(?:~{3,}|`{3,}))[ ]*         # Opening ``` or ~~~
# Optional {, lang="lang" or lang
(\{?\.?(?:lang=")?(?P<lang>[a-zA-Z0-9_+-]*)"?)?[ ]*
# Optional highlight lines, single- or double-quote-delimited
(hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot))?[ ]*
}?[ ]*\n                                # Optional closing }
(?P<code>.*?)(?<=\n)
(?P=fence)[ ]*$''', re.MULTILINE | re.DOTALL | re.VERBOSE)
        fencedcode = FencedCodeExtension()
        codehilite = CodeHiliteExtension(linenums=False, guess_lang=False)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.meta',
            'markdown.extensions.tables',
            fencedcode,
            codehilite,
            ])

        html = md.convert(txt)
        meta = md.Meta

        adict = self._get_article_metadata(meta)
        return html,adict,txt,self._get_medias(txt)

    def _get_and_update_article_content(self, afile, istxt=False):
        html, meta, txt, medias = self._get_article_content(afile)
        if not html:
            return  None, None, None, None
        attach = 0
        if not meta.attachments:
            attach = 1
        elif meta.attachments[0] == '$ATTACHMENTS':
            attach = 2
        elif len(meta.attachments)>0:
            attach = 3

        if medias and attach>0:
            txt,attachids = self._update_medias(medias, txt)
            idstxt = ','.join(attachids)
            if attach == 1:
                # Add attachments to the TOF.
                txt = 'Attachments: %s\n%s'%(idstxt, txt)
                slog.info('Fill attachments: %s.'%idstxt)
            elif attach == 2:
                txt = Template(txt).safe_substitute(ATTACHMENTS=idstxt)
                slog.info('Fill attachments: %s.'%idstxt)
            elif attach == 3:
                slog.info('Add new attachments: %s.'%idstxt)
                meta.attachments += attachids
                txt = re.sub(r'^Attachments: .*$', 
                        'Attachments: '+ ','.join(meta.attachments),
                        txt, 0, re.M)

            write_file(afile, txt)
            html, meta, txt, medias = self._get_article_content(txt, True)
            if medias:
                slog.error('Medias in the article is maybe wrong!')
                return None, None, None, None
        return html, meta, txt, medias

    def _get_medias(self, txt):
        return [(item, item.split('/')[-1]) for item in \
                re.findall(u'%s/draft/[\w\.\-]*'%self.conf.directory.media, txt, re.M)]

    def _update_a_draft(self):
        postid = self.get_postid()
        if not postid:
            slog.warning('Please provide a post id!')
            return
        afile, aname = self.conf.get_draft(postid)
        html, meta, txt, medias = self._get_and_update_article_content(afile)
        if not html:
            return
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
            post.terms = self.get_terms_from_meta(meta.category, meta.tags)
            if not post.terms:
                slog.warning('Please provide some terms.')
                return

        post.content= html
        post.title = meta.title
        post.slug = meta.nicename
        post.date = meta.date
        post.user = meta.author
        post.date_modified = meta.modified
        post.post_status = meta.poststatus
        postid = self.wpcall(NewPost(post))

        if postid:
            write_by_templ(afile, afile, {'POSTID':postid, 'SLUG':postid}, True)
        else:
            return

        newfile, newname = None, None
        if meta.posttype == 'page':
            newfile, newname = self.conf.get_article(meta.nicename, meta.posttype)
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
            self._update_an_article(postid)

    def _update_an_article(self, postid):
        afile, aname = self.conf.get_article(postid, self.args.type)
        html, meta, txt, medias = self._get_and_update_article_content(afile)
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
        urlre = re.compile(r'wp-content/.*/(\d{4}/\d{2}/).*')
        for path, name in medias:
            bits = None
            mediafile = self.conf.get_path(path)
            print(mediafile)
            with open(mediafile, 'rb') as m:
                bits = Binary(m.read()).data
            amedia = {}
            amedia['name'] = name
            amedia['type'] = mimetypes.guess_type(path)[0]
            amedia['bits'] = bits
            upd = self.wpcall(UploadFile(amedia))
            txt = txt.replace(path, upd['url'])
            match = urlre.search(upd['url'])
            targetdir = self.conf.get_media(match.group(1))
            if not os.path.exists(targetdir):
                os.makedirs(targetdir)
            attach_ids.append(upd['id'])
            shutil.move(mediafile, os.path.join(targetdir, name))
        return txt, attach_ids

    def _update_term(self):
        q = self.args.query 
        term = None
        query = self.get_term_query()
        typ = query[0]
        if q and len(q) > 1:
            term = self.get_terms_from_wp(query, force=True)
            if not term:
                slog.error('The term %s is not existend.'%str(q))
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
