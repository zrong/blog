#!/usr/bin/env python3
#==================================
# Migrate changeyan's comments to isso
# We convert the old comments to generic.json for isso migrate function.
# 
# isso: https://posativ.org/isso/
# changeyan: https://changyan.kuaizhan.com/
#
# author: zrong
#
# 2019-08-28 init
# 2019-08-29 use generic.json
#==================================

from pathlib import Path
import json
import sys
from datetime import datetime

"""
generic.json
[
    {
        "comments": [
            {"email": "", "remote_addr": "0.0.0.0", "website": "http://www.tigerspice.com", "created": "2005-02-24 04:03:37", "author": "texas holdem", "id": 0, "text": "Great men can't be ruled. by free online poker"}
        ],
        "id": "/posts/0001/",
        "title": "Test+post"
    },
    {
        "comments": [
            {"email": "105421439@87750645.com", "remote_addr": "0.0.0.0", "website": "", "created": "2005-05-08 06:50:26", "author": "Richard Crinshaw", "id": 0, "text": "Ja-make-a me crazzy mon :)\n"}
        ],
        "id": "/posts/0007/",
        "title": "Nat+%26+Miguel"
    }
]
"""

def export_generic(jsonfile, csvdir):
    jf = Path(jsonfile)
    cd = Path(csvdir)
    if not jf.is_absolute() or not cd.is_dir():
        raise ValueError('Path must be absolute!')
    
    jd = json.loads(jf.read_text('utf-8'))

    # threads row ['id', 'uri', 'title'])
    # comments row ['tid', 'id', 'parent', 'created', 'modified', 'mode', 'remote_addr', 'text', 'author', 'email', 'website', 'likes', 'dislikes', 'voters', 'notification']

    all_generic = {}

    for comment in jd['comments']:
        tid = comment['topicSourceId']

        if not tid:
            continue

        title = comment['topicTitle'].split('|')[0].strip()
        email = comment.get('referUserId', None)
        website = comment.get('userProfileUrl', None)
        remote_addr = comment['ip']
        author = comment.get('nickname', None)

        if email:
            # referUserId perhaps is a integer
            try:
                int(email)
                email = None
            except Exception as e:
                # a@b.com#name
                email = email.split('#')[0]

        thread_item = all_generic.get(tid)
        if not thread_item:
            thread_item = {
                'id': str(tid),
                'title': title,
                'comments': [],
            }
            all_generic[tid] = thread_item

        comment_item = {
            "email": email,
            "remote_addr": remote_addr,
            "website": website,
            "created": comment['ctime'],
            "author": author,
            "id": len(thread_item['comments']),
            "text": comment['content'],
            'parent': None,
            # Save old_id and reply_id to calculate "parent"
            'old_id': comment['id'],
            'reply_id': comment['replyId'] or None,
        }
        thread_item['comments'].append(comment_item)

    generic_list = list(all_generic.values())

    # Unfortunately, generic migrate has a bug for "parent", so I must ignore follows.
    """
    for thread in generic_list:
        parents = {}
        for comment in thread['comments']:
            reply_id = comment['reply_id']
            if reply_id:
                for c2 in thread['comments']:
                    if int(reply_id) == int(c2['old_id']):
                        comment['parent'] = c2['id']
                        break
    """

    for thread in generic_list:
        for comment in thread['comments']:
            del comment['reply_id']
            del comment['old_id']

    generic_file = Path(cd.joinpath('generic.json'))
    generic_file.write_text(json.dumps(generic_list, ensure_ascii=False))


if __name__ == '__main__':
    export_generic(sys.argv[1], sys.argv[2])

