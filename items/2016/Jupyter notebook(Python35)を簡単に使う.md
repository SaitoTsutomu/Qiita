title: Jupyter notebook(Python3.5)を簡単に使う
tags: Python Docker 最適化 Jupyter 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/bacc8143472238c3c6d8
created_at: 2016-04-15 12:02:02+09:00
updated_at: 2016-04-17 17:49:56+09:00
body:

# <i class='fa fa-download' /> はじめに
データ分析などの科学技術計算でJupyter notebook(Python)は、スタンダードといえるでしょう。
ここでは、dockerを使って、簡単に始める方法を説明します。

# <i class='fa fa-download' /> DockerToolboxのインストール

DockerToolboxのサイト(下記)からインストーラーをダウンロードして実行してください。
https://www.docker.com/products/docker-toolbox

インストールは、難しくないですが、必要であれば、[参考リンク](#-%E5%8F%82%E8%80%83%E3%83%AA%E3%83%B3%E3%82%AF)を参照してください。

Linuxの場合は、下記のようにして dockerをインストールできます。

```bash:bash
wget -qO- https://get.docker.com/ | sh
```

# <i class='fa fa-download' /> Jupyterの起動
## Linuxで実行する場合
下記のようにしてください[^1]。

[^1]: ユーザID、グループIDともに1000にしています。異なる場合は、[Dockerfile](https://github.com/Tsutomu-KKE/alpine-python/blob/master/jupyter/Dockerfile)を修正して、自前で"docker build"してください。

```bash:bash
mkdir jupyter
docker run -it -d -p 8888:8888 -v $PWD/jupyter:/home/jupyter \
  --name jupyter tsutomu7/alpine-python:jupyter
firefox localhost:8888
```

コンテナを終了して削除する場合は、次のようにしてください。

```bash:bash
docker rm -f jupyter
```

## WindowsやMacで実行する場合

DockerToolboxをインストールすると、Kitematicというツールがインストールされます。
Kitematicを起動してください。初回の起動では、DockerHubのログイン画面が表示されますが、スキップしてください。

Kitematicが起動したら、下記のように、検索ボックスに"tsutomu7/alpine-python"と入力してください。下に検索結果が出ますので、右下の"○○○"をクリックしてください。
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/e346afc9-6021-cfc4-8c86-1a21cc497769.png)

下記のように"SELECTED TAG"をクリックしてください。
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/b5102070-7a86-f65e-6918-136613d3edd6.png)

"jupyter"をクリックしてください。
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/6c88930e-0ceb-b8df-403d-74530e91b173.png)

"×"を押して、戻ってください。
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/6d080844-5a62-247f-086b-3a5cd2275202.png)

"CREATE"を押してください。
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/c24e2230-f8cc-2998-90fa-52e0aa1bf302.png)

ダウンロードがはじまり、しばらくすると下記のようにコンテナが起動します。

- **”VOLUMES”の下**をクリックして、”Enable"すると、後述の実行結果をホスト(WindowsやMac)に残せます。
- **"WEB PREVIEW"の下**をクリックするとブラウザが開いて Jupyterを使うことができます。
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/a94ff2d2-977d-2742-458a-388abb6e6be2.png)

# <i class='fa fa-download' /> やってみる

![image](https://qiita-image-store.s3.amazonaws.com/0/13955/fc8c539f-4e61-9903-74b2-d8456bf0373f.png)

## グラフ
セルに下記を入力して、Shiftキーを押しながらEnterキーを押して実行してみましょう。

```py3:jupyter
%matplotlib inline
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'IPAexGothic'
plt.plot([2,1,3], label='サンプル')
plt.legend();
```
このようにmatplotlibでグラフを書くことができて、日本語も扱えます。
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/284a639e-ac9e-019d-edde-694bbc119b58.png)

## 最適化
セルに下記を入力して、実行してみましょう。
[組合せ最適化問題を解い](http://qiita.com/Tsutomu-KKE@github/items/bfbf4c185ed7004b5721)て[数独を解く](http://qiita.com/Tsutomu-KKE@github/items/4f919f453aae95b3834b)こともできます。

```py3:jupyter
import pandas as pd, numpy as np
from more_itertools import grouper
from pulp import *

prob = """\
..6.....1
.7..6..5.
8..1.32..
..5.4.8..
.4.7.2.9.
..8.1.7..
..12.5..3
.6..7..8.
2.....4..
"""
r = range(9)
m = LpProblem() # 数理モデル
a = pd.DataFrame([(i, j, k, LpVariable('x%d%d%d'%(i,j,k), cat=LpBinary))
                  for i in r for j in r for k in r],
                 columns=['縦', '横', '数', 'x']) # (定式化1)
for i in r:
    for j in r:
        m += lpSum(a[(a.縦 == i) & (a.横 == j)].x) == 1 # (定式化2)
        m += lpSum(a[(a.縦 == i) & (a.数 == j)].x) == 1 # (定式化3)
        m += lpSum(a[(a.横 == i) & (a.数 == j)].x) == 1 # (定式化4)
for i in range(0, 9, 3):
    for j in range(0, 9, 3):
        for k in r:
            m += lpSum(a[(a.縦 >= i) & (a.縦 < i+3) & # (定式化5)
                         (a.横 >= j) & (a.横 < j+3) & (a.数 == k)].x) == 1
for i, s in enumerate(prob.split('\n')):
    for j, c in enumerate(s):
        if c.isdigit():
            k = int(c)-1 # (定式化6)
            m += lpSum(a[(a.縦 == i) & (a.横 == j) & (a.数 == k)].x) == 1
m.solve() # ソルバーで求解
f = a.x.apply(lambda v: value(v) == 1) # 選ばれた数字
print(np.array(list(grouper(9, a.数[f] + 1))))
```

```text:結果
[[5 3 6 8 2 7 9 4 1]
 [1 7 2 9 6 4 3 5 8]
 [8 9 4 1 5 3 2 6 7]
 [7 1 5 3 4 9 8 2 6]
 [6 4 3 7 8 2 1 9 5]
 [9 2 8 5 1 6 7 3 4]
 [4 8 1 2 9 5 6 7 3]
 [3 6 9 4 7 1 5 8 2]
 [2 5 7 6 3 8 4 1 9]]
```

# <i class='fa fa-download' /> Jupyter Projectとの比較

Jupyter notebookには、[Jupyter Project](https://jupyter.org/)のイメージ([jupyter/notebook](https://hub.docker.com/r/jupyter/notebook/))もありますが、今回、紹介したものは、下記のメリットがあります。

|特徴|紹介したもの|Jupyter Project|
|:--|:--|:--|
|新しい|Python 3.5.1|Python 3.4.3|
|サイズが小さい|658.5 MB|863.1 MB|
|インストール済みパッケージ数が多い|69|38|

## tsutomu7/alpine-python:jupyter のインストール済みパッケージ
package|ver|package|ver|package|ver|package|ver
:--|--:|:--|--:|:--|--:|:--|--:
blist|1.3.6|bokeh|0.11.1|chest|0.2.3|cloudpickle|0.1.1
conda|4.0.5|conda-env|2.4.5|cycler|0.10.0|dask|0.8.2
decorator|4.0.9|entrypoints|0.2|flask|0.10.1|fontconfig|2.11.1
freetype|2.5.5|heapdict|1.0.0|ipykernel|4.3.1|ipython|4.1.2
ipython-genutils|0.1.0|ipython_genutils|0.1.0|ipywidgets|4.1.1|itsdangerous|0.24
jinja2|2.8|jsonschema|2.4.0|jupyter|1.0.0|jupyter-client|4.2.2
jupyter-console|4.1.1|jupyter-core|4.1.0|jupyter_client|4.2.2|jupyter_console|4.1.1
jupyter_core|4.1.0|libgfortran|3.0|libpng|1.6.17|libsodium|1.0.3
libxml2|2.9.2|locket|0.2.0|markdown|2.6.6|markupsafe|0.23
matplotlib|1.5.1|mistune|0.7.2|more-itertools|2.2|mpmath|0.19
nbconvert|4.2.0|nbformat|4.0.1|ncurses|5.9|networkx|1.11
nomkl|1.0|notebook|4.1.0|numpy|1.11.0|openblas|0.2.14
openssl|1.0.2g|pandas|0.18.0|partd|0.3.2|path.py|8.2
patsy|0.4.1|pexpect|4.0.1|pickleshare|0.5|pip|8.1.1
psutil|4.1.0|ptyprocess|0.5|pulp|1.6.1|pycosat|0.6.1
pycrypto|2.6.1|pygments|2.1.3|pyjade|4.0.0|pyparsing|2.0.3
pyqt|4.11.4|python|3.5.1|python-dateutil|2.5.2|pytz|2016.3
pyyaml|3.11|pyzmq|15.2.0|qt|4.8.7|qtconsole|4.2.1
readline|6.2|requests|2.9.1|scikit-learn|0.17.1|scipy|0.17.0
seaborn|0.7.0|setuptools|20.3|simplegeneric|0.8.1|sip|4.16.9
six|1.10.0|sqlite|3.9.2|statsmodels|0.6.1|sympy|1.0
terminado|0.5|tk|8.5.18|toolz|0.7.4|tornado|4.3
traitlets|4.2.1|werkzeug|0.11.5|wheel|0.29.0|xz|5.0.5
yaml|0.1.6|zeromq|4.1.3|zlib|1.2.8||

## jupyter/notebook のインストール済みパッケージ

package|ver|package|ver|package|ver|package|ver
:--|--:|:--|--:|:--|--:|:--|--:
backports-abc|(0.4)|cffi|(1.5.2)|cryptography|(1.2.2)|decorator|(4.0.9)
idna|(2.0)|ipykernel|(4.2.2)|ipython|(4.1.1)|ipython-genutils|(0.1.0)
Jinja2|(2.8)|jsonschema|(2.5.1)|jupyter-client|(4.1.1)|jupyter-core|(4.0.6)
MarkupSafe|(0.23)|mistune|(0.7.1)|nbconvert|(4.1.0)|nbformat|(4.0.1)
ndg-httpsclient|(0.4.0)|nose|(1.3.7)|notebook|(5.0.0.dev0)|path.py|(8.1.2)
pexpect|(4.0.1)|pickleshare|(0.6)|pip|(8.0.2)|ptyprocess|(0.5.1)
pyasn1|(0.1.9)|pycparser|(2.14)|Pygments|(2.1.1)|pyOpenSSL|(0.15.1)
pyzmq|(15.2.0)|requests|(2.9.1)|setuptools|(20.1.1)|simplegeneric|(0.8.1)
six|(1.10.0)|terminado|(0.6)|tornado|(4.3)|traitlets|(4.1.0)
wheel|(0.29.0)|widgetsnbextension|(0.0.2.dev0)||

# <i class='fa fa-download' /> 参考リンク

- [Docker Toolboxのインストール：Windows編](http://qiita.com/maemori/items/52b1639fba4b1e68fccd)
- [現代のエンジニアのための強力なメモ帳 Jupyter notebookのすゝめ](http://techlife.cookpad.com/entry/write-once-share-anywhare)
- ubuntuベースのjupyter: [tsutomu7/jupyter](https://hub.docker.com/r/tsutomu7/jupyter/) (827MB)

以上

