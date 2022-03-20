title: Jupyterの小技2
tags: Python 数学 Jupyter
url: https://qiita.com/SaitoTsutomu/items/708ae8fe0cf293f7f986
created_at: 2017-02-23 14:59:31+09:00
updated_at: 2017-03-03 13:49:45+09:00
body:

[Jupyterの小技](http://qiita.com/Tsutomu-KKE@github/items/aa19a152dd8c80824d95)の続き
# Jupyterで等差数列または等比数列を計算する

準備として、まず、下記を実行してください。

```py3:jupyter_notebook
import re, IPython.core.getipython
from math import log
class NumberSequence:
    def __init__(self, s):
        ss = [t.replace(' ','') for t in re.sub('(.)-', r'\1+-', s).split('+')]
        assert len(ss) == 3 or (len(ss) > 3 and ss[3] == '...')
        tt = [int(i) for i in ss[:3]]
        d, e = tt[1] - tt[0], tt[1]//(tt[0] if tt[0] else 1)
        isratio = tt[2]/(tt[1] if tt[1] else 1) == e
        assert isratio or tt[2]-tt[1] == d
        ssum, self.value = r'\sum_{i=0}', None
        if len(ss) > 4:
            last = int(ss[-1])
            if isratio:
                n = int(round(log(last / tt[0], abs(e)))) + 1
                assert last == tt[0]*e**(n-1)
                self.value = sum(tt[0]*e**i for i in range(n))
            else:
                n = (last-tt[0]) // d + 1
                assert last == tt[0]+d*(n-1)
                self.value = sum(tt[0]+d*i for i in range(n))
            ssum += '^{%d}'%(n-1)
        if isratio:
            self.form = '$%s{%s%d^i}$'%(ssum, '' if tt[0]==1 else r'%s \times '%tt[1], e)
        else:
            self.form = r'$%s{%s%s i}$'%(ssum, '' if tt[0]==0 else '%s + '%tt[0],
                '' if d==1 else '%d \times'%d)
    def _repr_html_(self):
        if self.value is not None:
            print(self.value)
        return self.form
def S_impl(s):
    return NumberSequence(s)
ip = IPython.core.getipython.get_ipython()
if ip:
    ip.register_magic_function(S_impl, magic_name='S')
```

# 実行してみる

```py3:jupyter_notebook
%S 1+4+7+...
```

$\sum_{i=0}{1 + 3 \times i}$

計算式が表示されます。

---

```py3:jupyter_notebook
%S 1+4+7+...+19
>>>
70
```

$\sum_{i=0}^{6}{1 + 3 \times i}$

最後の項があると、合計と計算式が表示されます。

---

```py3:jupyter_notebook
%S 1-3+9+...
```

$\sum_{i=0}{-3^i}$

---

「％S」の「％」を省略できます。

```py3:jupyter_notebook
S 1 - 3 + 9 + ... + 81
>>>
61
```

$\sum_{i=0}^{4}{-3^i}$

```py3:jupyter_notebook
S {'+'.join(['0','1','2','...','100'])}
>>>
5050
```

$\sum_{i=0}^{100}{ i}$

「{ }」で囲むと、先に評価(eval)できます。

以上

