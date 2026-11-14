title: 「ミリジャン」の手役を組合せ最適化で求める
tags: Python 数学 pandas 最適化 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/260ac8f89a8d8ededf9d
created_at: 2020-05-04 22:21:40+09:00
updated_at: 2021-12-18 08:30:39+09:00
body:

## これなに

「[「ミリジャン」の手役を自動で判定するアルゴリズムを改良しました](https://qiita.com/YSRKEN/items/dd033edbd0ddedbef98b)」を、Pythonで[組合せ最適化](https://qiita.com/SaitoTsutomu/items/bfbf4c185ed7004b5721)を使って解いてみました。

## サンプルデータ

元記事のパターン2を使います。

```py
# パターン2
hands = ['春香', '千早', '美希', '真', '貴音', 'やよい', 'まつり', '真美', 'エミリー', '亜美', '桃子', '伊織', '育']

hand_unit_list = [
 {'member': {'伊織', 'エミリー'}, 'name': 'little trip around the world'},
 {'member': {'エミリー', 'まつり'}, 'name': 'Charlotte・Charlotte'},
 {'member': {'真美', 'やよい'}, 'name': 'わんつ→ているず'},
 {'member': {'千早', '春香'}, 'name': 'CRIMSON LOVERS'},
 {'member': {'美希', '伊織'}, 'name': "始めのDon't worry"},
 {'member': {'育', '伊織', '桃子'}, 'name': 'きゅんっ！ヴァンパイアガール'},
 {'member': {'真', '伊織', 'やよい'}, 'name': '待ち受けプリンス'},
 {'member': {'美希', '伊織', '貴音'}, 'name': '99 Nights'},
 {'member': {'真', '真美', '春香'}, 'name': '咲きませ！！乙女塾'},
 {'member': {'美希', '千早', '春香'}, 'name': 'Fate of the World'},
 {'member': {'真美', '亜美', 'やよい'}, 'name': 'Funny Logic'},
 {'member': {'美希', '真美', '亜美', '伊織'}, 'name': '星彩ステッパー'},
 {'member': {'美希', '春香', '真', '千早', 'やよい'}, 'name': 'メリー'},
 {'member': {'美希', '春香', '真', '千早', 'エミリー'}, 'name': 'World changer'},
 {'member': {'伊織', '春香', '真', '真美', '亜美'}, 'name': 'Miracle Night'},
 {'member': {'美希', '貴音', '真', '真美', 'やよい', '亜美'}, 'name': 'ザ・ライブ革命でSHOW!'}
]
```

## 解いてみる

[組合せオークション問題](https://qiita.com/SaitoTsutomu/items/614aa24b4025d3f7cc73)として解いてみましょう。

```py
import pandas as pd
from pulp import lpSum
from ortoolpy import model_max, addbinvars, addvals
df = pd.DataFrame([hand_unit['name'] for hand_unit in hand_unit_list],
                  columns=['name'])
for hand in hands:
    df[hand] = False
for i, hand_unit in enumerate(hand_unit_list):
    for member in hand_unit['member']:
        df.loc[i, member] = True
addbinvars(df)

m = model_max()
m += lpSum(df.Var)
for hand in hands:
    m += lpSum(df[df[hand] == True].Var) <= 1
m.solve()
addvals(df)
print(df[df.Val > 0])
```

|    | name                         | 春香   | 千早   | 美希   | 真    | 貴音   | やよい   | まつり   | 真美   | エミリー   | 亜美   | 桃子   | 伊織   | 育    | Var     |   Val |
|---:|:-----------------------------|:-------|:-------|:-------|:------|:-------|:---------|:---------|:-------|:-----------|:-------|:-------|:-------|:------|:--------|------:|
|  1 | Charlotte・Charlotte         | False  | False  | False  | False | False  | False    | True     | False  | True       | False  | False  | False  | False | v000002 |     1 |
|  2 | わんつ→ているず              | False  | False  | False  | False | False  | True     | False    | True   | False      | False  | False  | False  | False | v000003 |     1 |
|  3 | CRIMSON LOVERS               | True   | True   | False  | False | False  | False    | False    | False  | False      | False  | False  | False  | False | v000004 |     1 |
|  5 | きゅんっ！ヴァンパイアガール | False  | False  | False  | False | False  | False    | False    | False  | False      | False  | True   | True   | True  | v000006 |     1 |

元記事と同じ結果が得られました。


