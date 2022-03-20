title: Qiitaの記事とJupyter notebokとの相互変換
tags: Qiita Python Jupyter
url: https://qiita.com/SaitoTsutomu/items/168400d2e3ea44a70022
created_at: 2016-05-15 13:53:02+09:00
updated_at: 2017-09-10 18:40:31+09:00
body:

# はじめに
Qiitaの記事をJupyterで見たいとき、コピペでもいいですが、一括して変換できるようにプログラムを作ってみました。

## Jupyter notebookからMarkdownへ
- まずは、Jupyter notebookからMarkdownへ変換してみましょう。
- Jupyterの"File"メニューの"Download as"からもできますが、Pythonでやってみます。
- 以下のコードを"make_md.py"とし、下記のようにすると、結果を画面に表示します。
    - python make_md.py "ファイル名"
- "raw"の場合、preタグで囲んでいます。
- "code"の場合、"py3"にしています。

```py3:make_md.py
import sys, yaml
if len(sys.argv) < 2:
    exit()

try:
    with open(sys.argv[1], encoding='utf-8') as f:
        ls = yaml.load(f)['cells']
except:
    exit()

for dc in ls:
    typ = dc['cell_type']
    src = ''.join(dc['source'])
    if not src: continue
    if typ == 'markdown':
        print('%s'%src)
    elif typ == 'raw':
        print('<pre>\n%s\n</pre>'%src)
    elif typ == 'code':
        print('\n```py3:python3\n%s\n```'%src)
```
## MarkdownからJupyterへ
- 以下のコードを"make_ipynb.py"とし、下記のようにすると、Jupyterのファイルを作成します。
    - python make_ipynb.py "URL"

```py3:make_ipynb.py
import sys, urllib.request
from itertools import takewhile
if len(sys.argv) < 2:
    exit()
try:
    s = urllib.request.urlopen(sys.argv[1]+'.md').read().decode().rstrip()
    ss = s.replace('\\', '\\\\').replace('\t', '\\t').replace('"', '\\"').split('\n')
except:
    exit()
fn = ss[0]
ss[0] = '# ' + ss[0]

def parse_str(ss):
    tt = list(takewhile(lambda s: not s.startswith('```'), ss))
    ss = ss[len(tt):]
    cell_type = 'raw' if len(tt) == 0 else 'markdown'
    if cell_type == 'raw':
        nm = ss[0][(ss[0]+':').index(':')+1:]
        tg = ss[0][3:len(ss[0])-len(nm)].rstrip(':')
        ss = ss[1:]
        if tg.startswith('py') or tg == 'bash':
            cell_type = 'code'
        tt = list(takewhile(lambda s: not s.startswith('```'), ss))
        ss = ss[len(tt):]
        if cell_type == 'code':
            tt = list(takewhile(lambda s: not s.startswith('>>>'), tt))
        if ss:
            ss = ss[1:]
        tt = ([('%%' if tg == 'bash' else '# ') + tg] if tg else []) + tt
    return cell_type, tt, ss
cdin = '   "execution_count": null,\n   "outputs": [],\n   '

rr = []
while ss:
    cell_type, tt, ss = parse_str(ss)
    s = '\\n",\n    "'.join(tt)
    if s:
        rr.append("""\
   "cell_type": "%s",
   "metadata": {},
%s   "source": [
    "%s"
   ]
"""%(cell_type, '' if cell_type != 'code' else cdin, '\\n",\n    "'.join(tt)))

with open(fn+'.ipynb', 'w') as fp:
    fp.write("""\
{
 "cells": [
  {
""")
    fp.write('  },\n  {\n'.join(rr))
    fp.write("""\
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.5.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}\n""")
```

# 追記
- SaitoTsutimuのPythonの記事直近20を自動で表示するようにしました。
    - https://hub.docker.com/r/tsutomu7/qiita-jupyter/
        - ポータルのflaskのポートを5000にしています。
        - サブのJupyterのポートは8888にしています。
            - Kitematicのときは、8888に戻してください。
- 一時的にArukasで公開しました。
    - https://qiita-jupyter.arukascloud.io/

以上

