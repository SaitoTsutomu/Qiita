title: Python2系と3系(Anaconda編)
tags: Python Anaconda
url: https://qiita.com/SaitoTsutomu/items/1dadca8bde023d55af8f
created_at: 2015-11-04 13:58:39+09:00
updated_at: 2015-11-04 13:58:39+09:00
body:

# Pythonのバージョンによるパッケージの違い
Python3.5がリリース[^1]されました。Anaconda[^2]も対応したようです。
普段は、Anacondaを利用しているので、Anaconda上でパッケージがどのように変わったかを確認してみます。
まず、Anacondaのサイトからデータを取得してpandasの表にしてみます。

```py3:
import pandas as pd
from urllib import request
from bs4 import BeautifulSoup
with request.urlopen('http://docs.continuum.io/anaconda/pkg-docs') as fp:
    s = fp.readall()
bs = BeautifulSoup(s)
ls = bs.findAll('table', attrs={'class':'docutils'})
vers = [2.7, 3.4, 3.5]
res = []
for i in range(len(vers)):
    rows = ls[i].findAll('tr')
    for r in rows[1:]:
        t = r.findAll('td')
        res.append((vers[i], t[0].find('a').text, len(t[3].contents) > 0))
a = pd.DataFrame(res, columns=['ver', 'nam', 'ini'])
```

含まれているパッケージの数を見てみます。

```py3:
print('Number of supported packages:', a.groupby('ver').size())
>>>
Number of supported packages: ver
2.7    387
3.4    323
3.5    317
dtype: int64
```

初期インストール数を見てみます。3.4は対象外のようです。

```py3:
print('In intaller:', a[a.ini].groupby('ver').size())
>>>
In intaller: ver
2.7    168
3.5    153
dtype: int64
```

一旦、setにします。

```py3:
a27, a34, a35 = a.groupby('ver').nam
a27, a34, a35 = set(a27[1]), set(a34[1]), set(a35[1])
```

Python3系にあって2系にないもの。

```py3:
print('Only 3.X', (a34|a35) - a27)
>>>
Only 3.X {'blosc', 'xz'}
```

Python3.4だけのものは、無いようです。

```py3:
print('Only 3.4', a34 - (a27|a35))
>>>
Only 3.4 set()
```

Python3.5で増えたものも無いようです。

```py3:
print('In 3.5 but 3.4', a35 - a34)
>>>
In 3.5 but 3.4 set()
```

Python3.5で削られたパッケージ。

```py3:
print('Disappeared at 3.5', a34 - a35)
>>>
Disappeared at 3.5 {'yt', 'azure', 'bottleneck', 'llvmlite', 'numba', 'blaze'}
```

Python2.7にあって、Python3.Xにないもの。ただし、この中にはpipでインストールできるものもあるようです。

```py3:
print('Only 2.7', a27 - (a34|a35))
>>>
Only 2.7 {'starcluster', 'python-gdbm', 'mtq', 'traitsui', 'scrapy', 'graphite-web', 'casuarius', 'gensim', 'progressbar', 'ssh', 'grin', 'singledispatch', 'cheetah', 'llvm', 'protobuf', 'websocket', 'gdbm', 'faulthandler', 'gevent-websocket', 'dnspython', 'envisage', 'pyamg', 'py2cairo', 'pixman', 'hyde', 'vtk', 'python-ntlm', 'cdecimal', 'db', 'chaco', 'chalmers', 'mysql-python', 'paste', 'pep381client', 'mercurial', 'mesa', 'fabric', 'googlecl', 'ipaddress', 'apptools', 'gevent', 'bsddb', 'pysam', 'enaml', 'enum34', 'pysal', 'atom', 'supervisor', 'whisper', 'pil', 'ndg-httpsclient', 'essbasepy', 'cairo', 'enable', 'kiwisolver', 'traits', 'orange', 'uuid', 'opencv', 'pandasql', 'gdata', 'lcms', 'xlutils', 'pyaudio', 'pyface', 'ssl_match_hostname'}
```

docker hubのanaconda3[^3]も3.5に変わったようです。


[^1]: [Python 3.5 リリース](http://www.python.jp/news/python-3.5.html)
[^2]: [Anaconda Download](https://www.continuum.io/downloads)
[^3]: [continuumio/anaconda3](https://hub.docker.com/r/continuumio/anaconda3/)

