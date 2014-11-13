import os
import re
import xmlrpc
import markdown
from wordpress_xmlrpc import (
        Client, WordPressPost, WordPressPage, 
        WordPressTaxonomy, WordPressTerm)
from wordpress_xmlrpc.methods.posts import (
        GetPosts, NewPost, GetPost, EditPost)
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods.options import GetOptions
from wordpress_xmlrpc.methods.taxonomies import (
        GetTaxonomies, GetTaxonomy, GetTerms, GetTerm)
from zrong.base import slog, read_file, DictBase


conf = None
args = None
wp = None

def _wpcall(method):
    global wp
    if not wp:
        wp = Client(conf.site.url, conf.site.user, conf.site.password)
    try:
        results = wp.call(method)
    except xmlrpc.client.Fault as e:
        slog.error(e)
        return None
    return results

def _get_postid(as_list=False):
    if not args.query:
        return None
    if as_list:
        postids = []
        for postid in args.query:
            match = re.match(r'^(\d+)-(\d+)$', postid)
            if match:
                a = int(match.group(1))
                b = int(match.group(2))
                for i in range(a,b+1):
                    postids.append(str(i))
            else:
                postids.append(postid)
        return postids
    return args.query[0]

def _get_class():
    if args.type == 'post':
        return WordPressPost
    if args.type == 'page':
        return WordPressPage
    return None

def _print_result(result):
    if isinstance(result, WordPressTerm):
        slog.info('id=%s, group=%s, '
                'taxnomy_id=%s, name=%s, slug=%s, '
                'parent=%s, count=%d', 
                result.id, result.group, 
                result.taxonomy_id, result.name, result.slug,
                result.parent, result.count)
    elif isinstance(result, WordPressPost):
        slog.info('id=%s, date_modified=%s, '
                'slug=%s, title=%s', 
                result.id, str(result.date_modified), 
                result.slug, result.title)
    else:
        print(result)

def _print_results(results):
    if isinstance(results, list):
        for result in results:
            _print_result(result)
    else:
        _print_result(results)

def _wp_check_draft(postid):
    if not postid:
        slog.warning('Please provide a post id!')
        return False

    draftname, draftfile = conf.get_draft(postid)
    if not os.path.exist(draftfile):
        slog.error('The draft file "%s" is inexistance!'%draftfile)
        return False

    return draftfile

def _wp_pub():
    dfile = _wp_check_draft(_get_postid())
    if dfile:
        txt = read_file(dfile)
        print('wp_pub', txt)

def _wp_new():
    try:
        draftname, draftfile = conf.get_new_draft(_get_postid())
    except BlogError as e:
        slog.error(e)
        return

def _wp_update():
    postids = _get_postid(as_list=True)
    if not postids:
        slog.warning('Please provide a post id!')
        return

    if args.type not in ('post', 'page'):
        return

    def _update_a_post(postid):
        pfile = conf.get_post(postid)
        if not os.path.exists(pfile):
            slog.error('The post file "%s" is inexistance!'%pfile)
            return
        txt = read_file(pfile)
        md = markdown.Markdown(extensions=['markdown.extensions.meta'])
        html = md.convert(txt)
        post = _wpcall(GetPost(postid, result_class=_get_class()))
        if not post:
            return
        meta = md.Meta
        post.title = meta['title'][0]
        post.slug = meta['nicename'][0]
        post.content = html
        modified = meta.get('modified')
        if modified:
            post.date_modified = modified[0]

        succ = _wpcall(EditPost(postid, post))
        if succ == None:
            return
        if succ:
            slog.info('Update %s successfully!'%postid)
        else:
            slog.info('Update %s fail!'%postid)

    for postid in postids:
        _update_a_post(postid)

def _wp_del():
    pass

def _wp_show():
    method = None
    if args.type == 'post' or args.type == 'page':

        field = {'post_type':'page'} \
            if args.type == 'page' else {}
        field['number'] = args.number
        field['orderby'] = args.orderby
        field['order'] = args.order

        resultclass = WordPressPage \
            if args.type == 'page' else WordPressPost

        if args.query:
            method = GetPost(_get_postid(), result_class=resultclass)
        else:
            method = GetPosts(field, result_class=resultclass)

    elif args.type == 'option':
        method = GetOptions([])
    elif args.type == 'tax':
        method = GetTaxonomies()
    elif args.type == 'term':
        method = GetTerms(args.query[0])

    if not method:
        return

    results = _wpcall(method)
    if not results:
        return

    _print_results(results)

def build(gconf, gargs, parser=None):
    global conf
    global args
    conf = gconf
    args = gargs
    print(args)

    noAnyArgs = True
    if args.user:
        conf.site.user = args.user
    if args.password:
        conf.site.password = args.password
    if args.site:
        if args.site.rfind('xmlrpc.php')>0:
            conf.site.url = args.site
        else:
            removeslash = args.site.rfind('/')
            if removeslash == len(args.site)-1:
                removeslash = args.site[0:removeslash]
            else:
                removeslash = args.site
            conf.site.url = '%s/xmlrpc.php'%removeslash
    if args.action:
        eval('_wp_'+args.action)()
        noAnyArgs = False

    if noAnyArgs and parser:
        parser.print_help()

