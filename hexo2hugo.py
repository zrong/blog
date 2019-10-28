#!/usr/bin/env python3
#==================================
# move zorng's hexo blog to hugo
#
# 2019-06-11 init
# 2019-06-20 build flash content
#==================================

from pathlib import Path
import os
import re
import yaml
import toml
from datetime import datetime, timezone, timedelta

pwddir = Path(__file__).parent.resolve()

hexo_source = pwddir.parent.joinpath('blog/source/')
hexo_posts = pwddir.parent.joinpath('blog/source/_posts')
hugo_posts = pwddir.joinpath('content/post')
hugo_articles = pwddir.joinpath('content/article')


def replace_body_flash(body_text):
    """ dispose the {% flash %} xxx {% endflash %} 
    in multiline
    """
    re_flash = re.compile(r'{% flash %\}(.*?)\{% endflash %\}', re.DOTALL)
    match_list = re_flash.finditer(body_text)
    repl_list = []
    for matchobj in match_list:
        flash_params = matchobj.group(1).strip()
        # print('flash_params', flash_params)
        lines = flash_params.split('\n')
        flash_pobj = {}
        for line in lines:
            # print('line', line)
            line_list = line.strip().split(':')
            key = line_list[0].strip()
            value = line_list[1].strip()
            if key == 'useexpressinstall' or key == 'menu' or key == 'fversion':
                value = value.replace("'", '').replace('"', '')
            elif key == 'width' or key == 'height':
                value = value.replace("'", '').replace('"', '')
                value = int(value)
            else:
                value = str(value)
            flash_pobj[key] = value
        new_param_line = ['{0}="{1}"'.format(k, v) for k, v in flash_pobj.items()]
        repl_list.append('{{{{< flash {0} >}}}}'.format(' '.join(new_param_line)))
    # print(repl_list)
    for repl in repl_list:
        body_text = re_flash.sub(repl, body_text, 1)
        # print('flash_params ', flash_params)
        # print('flash_pobj ', flash_pobj)
    # print(body_text)
    return body_text


def replace_body_download(body_text):
    """ dispose the
    {% download %}
    id:
        - 1
        - 2
    {% enddownload %} 
    in multiline
    """
    re_flash = re.compile(r'{% download %\}(.*?)\{% enddownload %\}', re.DOTALL)
    match_list = re_flash.finditer(body_text)
    repl_list = []
    for matchobj in match_list:
        dl_params = matchobj.group(1).strip()
        lines = dl_params.split('\n')
        dl_ids = []
        for line in lines:
            print('line', line)
            if line.startswith('id'):
                continue
            lead = line.find('-')
            if lead == -1:
                continue
            value = line[lead+1:].strip().replace("'", '').replace('"', '')
            dl_ids.append(value)
        repl_list.append('{{{{< download {0} >}}}}'.format(' '.join(dl_ids)))
    # print(repl_list)
    for repl in repl_list:
        # print(body_text)
        body_text = re_flash.sub(repl, body_text, 1)
    return body_text


def replace_body_label(body_text):
    """ dispose the shortcode
    {% label 'text' info/danger/warning/success %}
    """
    re_label = re.compile(r'\{% label +\'(.*?)\' +(\w+) +%\}')
    match_list = re_label.finditer(body_text)
    repl_list = []
    for matchobj in match_list:
        label_name = matchobj.group(1)
        label_color = matchobj.group(2)
        repl_list.append('{{{{< label {0} {1} >}}}}'.format(label_name, label_color))
    for repl in repl_list:
        # print(body_text)
        body_text = re_label.sub(repl, body_text, 1)
    return body_text


def replace_body_alert(body_text):
    re_alert = re.compile(r'\{% alert +(\w+) +%\}(.*?)\{% endalert %\}', re.DOTALL)
    match_list = re_alert.finditer(body_text)
    repl_list = []
    for matchobj in match_list:
        alert_color = matchobj.group(1)
        alert_text = matchobj.group(2).strip()
        repl_list.append('{{{{% alert {0} %}}}}\n{1}\n{{{{% /alert %}}}}'.format(alert_color, alert_text))
    for repl in repl_list:
        body_text = re_alert.sub(repl, body_text, 1)
    return body_text


def replace_bodies(body_text):
    body_text = replace_body_flash(body_text)
    body_text = replace_body_download(body_text)
    body_text = replace_body_alert(body_text)
    body_text = replace_body_label(body_text)
    return body_text


def read_content(f):
    front_matter = []
    body = []
    with f.open() as pf:
        fm = True
        line = pf.readline()
        while line:
            if line.startswith('---'):
                if len(front_matter) == 0:
                    line = pf.readline()
                    continue
                else:
                    fm = False
            else:
                if fm:
                    front_matter.append(line)
                else:
                    body.append(line)
            line = pf.readline()
    body_text = replace_bodies(''.join(body))
    return {
        'front_matter': yaml.load(''.join(front_matter), Loader=yaml.SafeLoader),
        'body': body_text
    }


def mege_content(p, type_):
    ofm = p['front_matter']
    datefmt = '%Y-%m-%d %H:%M:%S'
    tzinfo = timezone(timedelta(hours=8))
    dt = ofm['date']
    if isinstance(dt, str):
        dt = datetime.strptime(ofm['date'], datefmt)
    dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=tzinfo)
    upt = ofm.get('updated')
    if isinstance(upt, str):
        upt = datetime.strptime(upt, datefmt)
    tags = ofm.get('tags')
    nicename = ofm.get('nicename')
    postid = ofm.get('postid')
    slug = str(nicename) if nicename else str(postid)
    categories = ofm.get('categories')
    toc = p.get('toc', False)
    aliases = None
    url = None

    if type_ == 'post':
        aliases = ['/post/{0}.html'.format(postid)]
    if type_ == 'article':
        url = '/{0}/'.format(slug)

    nfm = {
        'title': ofm['title'],
        'postid': int(postid),
        'date': dt,
        'isCJKLanguage': True,
        'toc': toc,
        'type': type_,
        'slug': slug,
    }

    if aliases:
        nfm['aliases'] = aliases
    if url:
        nfm['url'] = url

    # use singular, not plural
    # so write follows in config.toml of hugo project
    """
    [taxonomies]
        category = "category"
        tag = "tag"
    """
    if categories is not None:
        # nfm['categories'] = [categories]
        nfm['category'] = [categories]
    if tags is not None:
        # use singular, not plural
        # nfm['tag'] = tags
        nfm['tag'] = tags

    if upt is not None:
        upt = datetime(upt.year, upt.month, upt.day, upt.hour, upt.minute, upt.second, tzinfo=tzinfo)
        nfm['lastmod'] = upt
    if ofm.get('attachments'):
        nfm['attachments'] = ofm['attachments']
    
    front_matter_toml = toml.dumps(nfm)
    return '+++\n%s+++\n\n%s' % (front_matter_toml, p['body'])
    

def build_post(p):
    """ build a post 
    """
    f = hexo_posts.joinpath(p)
    post_data = read_content(f)
    s = mege_content(post_data, 'post')
    hugef = hugo_posts.joinpath(p)
    hugef.write_text(s, encoding='utf8')


def build_posts():
    """ build all posts in hexo/source/_posts
    """
    i = 0
    error_posts = []
    for p in os.listdir(hexo_posts):
        if not p.endswith('.md'):
            continue
        print('perform ', i, p)
        try:
            build_post(p)
        except Exception as e:
            error_posts.append({'name': p, 'error': e})
            print('%s error %s' %(p, e))
            continue
        i += 1
    print(len(error_posts))


def build_pages():
    i = 0
    error_pages = []
    for p in os.listdir(hexo_source):
        if p.startswith('.') or p.startswith('_') or p in ('search', 'uploads', 'tag', 'category', 'link'):
            continue
        page_file = hexo_source.joinpath(p, 'index.md')
        page_data = read_content(page_file)
        print('perform ', i, page_file)
        try:
            s = mege_content(page_data, 'article')
            hugef = hugo_articles.joinpath(p+'.md')
            hugef.write_text(s, encoding='utf8')
        except Exception as e:
            error_pages.append({'name': p, 'error': e})
            print('%s error %s' %(p, e))
            continue
        i += 1
    print(len(error_pages))


if __name__ == '__main__':
    # build_post('2631.md')
    build_posts()
    build_pages()