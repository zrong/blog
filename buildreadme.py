#!/usr/bin/env python3

import os

def _write_list(adir, rf):
    rf.write('# '+adir+'\n\n')
    is_post = adir == 'post'
    names = []
    for afile in os.listdir(adir):
        if afile.endswith('.md'):
            name = afile.split('.')[0]
            if is_post:
                names.append(int(name))
            else:
                names.append(name)
    if is_post:
        names = sorted(names)
    for name in names:
        _write_a_file(adir, str(name), rf)
    rf.write('\n')

def _write_a_file(adir, name, rf):
    with open(os.path.join(adir, str(name)+'.md'), 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('Title:'):
                rf.write('1. [%s](http://zengrong.net/%s.htm)\n'%(
                            line[6:].strip(), name))
                break

def _write_readme():
    with open('README.md', 'w', encoding='utf-8', newline='\n') as f:
        f.write("[zrong's blog](http://zengrong.net) 中的所有文章\n")
        f.write('==========\n\n')
        f.write("----------\n\n")
        _write_list('page', f)
        _write_list('post', f)

def _rewrite_title():
    for afile in os.listdir('post'):
        if afile.endswith('.md'):
            content = None
            fpath = os.path.join('post', afile)
            with open(fpath, 'r', encoding='utf-8', newline='\n') as f:
                for line in f:
                    if line.startswith('Title:') and line.find('[转]') > -1:
                        f.seek(0)
                        content = True
                        break
                if content:
                     content = f.read().replace('[转]', '【转】')
            if content:
                with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(content)

if __name__ == "__main__":
    _write_readme()
    #_rewrite_title()
