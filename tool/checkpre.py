import os

workdir = os.path.abspath(os.path.join("post"))
haspre = {}

def check_file(f):
    global haspre
    if not f.endswith('.md'):
        return
    with open(f, 'r', encoding='utf-8') as fo:
        for line in fo:
            if line.startswith('<pre'):
                haspre[f] = True
                return

for f in os.listdir(workdir):
    check_file(os.path.join(workdir, f))

print(haspre.keys())
with open(os.path.join(workdir, '../haspre.log'), 'w', encoding='utf-8') as fo:
    print(fo)
    for k in haspre.keys():
        print(k)
        fo.write(k+"\n")
