from pprint import pprint
import os
import time
import json

def count_frames(p='source.tex'):
    with open(p) as f:
        d = f.read().strip()

    cf = d.count('\\begin{frame}')
    return cf

def read_struct(t):
    tl = t.split('\n')
    print(tl[0])
    if tl[0].find('{') != -1:
        st = [[tl[0][tl[0].find('{')+1:tl[0].find('}')], tl[0][tl[0].find('[')+1:tl[0].find(']')]]] if '[' in tl[0] else [tl[0][tl[0].find('{')+1:tl[0].find('}')]]
        print(st)
        st.append(read_struct('\n'.join(tl[1:-1])))
    else:
        if tl[0][0] == '\\':
            idf = t[0].split(' ')[0]
            st = [idf] + [i.split()[1:] for i in tl]

    return st

def struct2text(st):
    doc = ""

    if '\\'==st[0][0]:
        if '\\'==st[0]:
            doc+='\n'.join(st[1:])+'\n'
        else:
            doc+='\n'.join(f'{st[0]} {j}' for j in st[1:])+'\n'
    else:
        doc+='\\begin{%s}\n'%st[0] if type(st[0])==str else '\\begin{%s}[%s]\n'%(st[0][0],st[0][1])
        for i in st[1:]:
            doc+=struct2text(i)
        doc+='\\end{%s}\n'%st[0] if type(st[0])==str else '\\end{%s}\n'%st[0][0]

    return doc

def start(aspectratio='169',font='Montserrat',theme='Nord',title="Title",subtitle="Subtitle",author="",date="\\today"):
    # main config
    doc = "\\documentclass[aspectratio=%s]{beamer}\n\\usepackage{fontspec}\n\\setmainfont{%s}\n\\usetheme{%s}\n\n"% (aspectratio,font,theme)
    # title
    doc += "\\title{%s}\n\\subtitle{%s}\n" % (title, subtitle)
    if author != "": doc+="\\author{%s}\n" % author
    doc += "\\date{%s}\n\n" % date

    return doc

def save(st, path):
    with open(path, 'w') as f:
        json.dump(st, f)

def load(path):
    with open(path, 'rb') as f:
        st = json.load(f)
    return st
