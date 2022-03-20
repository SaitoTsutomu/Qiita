title: 組合せ最適化でPyCon JP 2016の講演を決めよう
tags: Python 数学 最適化 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/196a9f09a0ceb0adfcb9
created_at: 2016-02-26 18:58:41+09:00
updated_at: 2016-02-26 18:58:41+09:00
body:

# <i class='fa fa-calendar' /> PyCon JP 2016の講演を決めよう
(これは、あくまでジョークです)

PyConの今年のテーマは、[「みんなちがって、みんないい」](http://pyconjp.blogspot.jp/2016/02/theme-of-pyconjp2016.html)だそうです。

ということで、全ての要素を盛込んだ講演を選んでみましょう。
[組合せ最適化](http://qiita.com/Tsutomu-KKE@github/items/bfbf4c185ed7004b5721)の集合被覆問題を使います。

# <i class='fa fa-calendar' /> ランダムに講演候補を作成します
講演者の国籍や、講演のレベル、講演の分野などをランダムに作成します。
得点は、例えば「いいね」の数とします。

```py3:python
import numpy as np, pandas as pd
np.random.seed(1)
n = 20
a = pd.DataFrame({
        '国': np.random.choice('アメリカ イギリス インド フランス ロシア 中国'.split(), n),
        'レベル': np.random.choice('初級 中級 上級'.split(), n),
        '分野': np.random.choice('データ分析 最適化 機械学習 ドキュメント Web'.split(), n),
        '得点': np.random.randint(1, 10, n),
    })
print(a)
```

 |レベル|分野|国|得点
:--|:--|:--|:--|:--
0|初級|Web|中国|4
1|上級|最適化|フランス|3
2|初級|データ分析|ロシア|1
...|...|...|...|...
19|初級|データ分析|フランス|8

# <i class='fa fa-calendar' /> 集合被覆問題を解きます
ortoolpy.set_coveringを使います。最小化なので、得点の逆数を重みにしました。

```py3:python
from ortoolpy import set_covering
n = sum(b.nunique() for b in [a.レベル, a.分野, a.国]) # 総ユニーク数
res = set_covering(n, [(1/r.得点, r[:3].tolist()) for _, r in a.iterrows()])
print(a.ix[res])
```

 |レベル|分野|国|得点
:--|:--|:--|:--|:--
5|上級|機械学習|フランス|8
8|中級|ドキュメント|アメリカ|7
10|初級|最適化|ロシア|8
13|中級|データ分析|イギリス|6
14|中級|最適化|インド|4
16|上級|Web|中国|9

全項目が出現しているのがわかります。

以上

