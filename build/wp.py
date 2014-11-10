import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo


conf = None
args = None


def _wp_publish():
    print(conf)
    wp = Client(conf.site, conf.user, conf.password)
    #wp.call(GetPosts())
    cli = wp.call(GetUserInfo())
    print(type(cli))

def build(gconf, gargs, parser=None):
    global conf
    global args
    conf = gconf
    args = gargs

    noAnyArgs = True
    if args.user:
        conf.user = args.user
    if args.password:
        conf.passwrod = args.password
    if args.site:
        if args.site.rfind('xmlrpc.php')>0:
            conf.site = args.site
        else:
            removeslash = args.site.rfind('/')
            if removeslash == len(args.site)-1:
                removeslash = args.site[0:removeslash]
            else:
                removeslash = args.site
            conf.site = '%s/xmlrpc.php'%removeslash
    if args.action:
        _wp_publish()
        noAnyArgs = False

    if noAnyArgs and parser:
        parser.print_help()

