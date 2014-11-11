import os
import xmlrpc
from zrong.base import slog, read_file
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import (
        GetPosts, NewPost, GetPost)
from wordpress_xmlrpc.methods.users import GetUserInfo


conf = None
args = None
wp = None

def _wpcall(method):
    global wp
    if not wp:
        wp = Client(conf.site.url, conf.site.user, conf.site.password)
    return wp.call(method)

def _wp_publish():
    try:
        post = _wpcall(GetPost(2199))
    except xmlrpc.client.Fault as e:
        print(e)
        return
    #cli = _wpcall(GetUserInfo())
    print(post.title)
    print(post.post_status)
    print(post.post_type)
    print(post.custom_fields)
    print(post.excerpt)
    print(post.content)
    print(post.slug)
    print(post.sticky)
    print(hasattr(post, 'enclosure'))

    posts = _wpcall(GetPosts({'number':1}))
    for post in posts:
        print('='*10)
        print(post.content)
        print(post.custom_fields)



def _wp_check_draft(postid):
    if not postid:
        slog.warning('Please provide a post id!')
        return False

    draftname, draftfile = conf.get_draft(args.postid)
    if not os.path.exist(draftfile):
        slog.error('The draft file "%s" is inexistance!'%draftfile)
        return False

    return draftfile

def _wp_pub():
    dfile = _wp_check_draft(args.postid)
    if dfile:
        txt = read_file(dfile)
        print('wp_pub', txt)

def _wp_new():
    postid = args.postid
    try:
        draftname, draftfile = conf.get_new_draft(args.postid)
    except BlogError as e:
        slog.error(e)
        return

def _wp_update():
    if not args.postid:
        slog.warning('Please provide a post id!')
        return

    pfile = conf.get_post(args.postid)
    if not os.path.exists(pfile):
        slog.error('The post file "%s" is inexistance!'%pfile)
        return
    txt = read_file(pfile)

def _wp_del():
    pass

def build(gconf, gargs, parser=None):
    global conf
    global args
    conf = gconf
    args = gargs

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

