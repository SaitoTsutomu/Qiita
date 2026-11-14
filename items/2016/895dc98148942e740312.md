title: pythonパッケージの依存関係をgraphvizで可視化
tags: Python Graphviz Docker
url: https://qiita.com/SaitoTsutomu/items/895dc98148942e740312
created_at: 2016-03-09 13:53:16+09:00
updated_at: 2016-03-09 22:38:13+09:00
body:

# <i class='fa fa-map'/> やりたいこと
pythonパッケージの依存関係を簡単に見たいとします。
ここでは、graphvizで可視化する方法を説明します。
Ubuntu15.10で確認していますが、たぶん、windowsでもできます。

# <i class='fa fa-map'/> インストール

前提: [Anaconda](https://www.continuum.io/downloads)をインストール済みとします。

graphvizのインストールは、以下の通りです。condaでgraphviz本体を、pipでラッパーをインストールします。また、libltdl7というライブラリも必要でした。

```bash:bash
conda install -y graphviz
pip install graphviz
apt-get install -y libltdl7
```

パッケージの依存関係は、pipdeptreeを使います。インストールは以下の通り。

```bash:bash
pip install pipdeptree
```

# <i class='fa fa-map'/> 実行

以下のようにして python-dep.pngを作成できます。
左からインストールしていけば よいように、並んでいます。

```py3:python
import graphviz
from subprocess import run, DEVNULL, PIPE
ss = run(['pipdeptree'], stdout=DEVNULL, stderr=PIPE, 
         universal_newlines=True).stderr.rstrip().split('\n')
ss = [s[2:].lower().split()[:3] for s in ss if s[0] in ' *']
g = graphviz.Digraph(format='png', filename='python-dep', engine='dot')            
g.edges([(s[2], s[0][:s[0].index('=')]) for s in ss])
g.attr('graph', rankdir='LR')
g.render()
```

![image](https://qiita-image-store.s3.amazonaws.com/0/13955/79e3dd36-d508-25a6-dbac-957ced665d7f.png)


# <i class='fa fa-map'/> Dockerでお試し

上記の一連の[docker](https://hub.docker.com/r/tsutomu7/python-dep/builds/)([Dockerfile](https://github.com/Tsutomu-KKE/python-dep/blob/master/Dockerfile))を用意しました。下記のようにして、python-dep.pngを作成できます。

```bash:bash
docker run -it --rm -v $PWD:/tmp -w /tmp \
    tsutomu7/python-dep python /root/python-dep.py
```


参考
[Graphvizとdot言語でグラフを描く方法のまとめ](http://qiita.com/rubytomato@github/items/51779135bc4b77c8c20d)
[pip関連ツールでPythonのパッケージ管理を楽にする](http://qiita.com/kk6/items/90bc704c9d2a9edc580e)
[Python にインストールしたパッケージをグラフにしてみた](http://qiita.com/kitsuyui/items/0e72af781ac1a7e3e948) ... 記事を書いた後、見つけました。

以上

