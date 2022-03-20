title: 中学校の委員分け（NetworkX版）
tags: Python 数学 最適化 networkx 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/d68cd02df4fc097d7672
created_at: 2020-04-29 10:38:58+09:00
updated_at: 2020-04-29 10:43:11+09:00
body:

## 問題

生徒の希望を元に「クラスの委員を割り当てる問題」をマッチング問題として解きます。

## 参考

- 元記事「[中学校の委員分けを最小費用流で最適化してみた話](https://qiita.com/defineprogram/items/b8eb70bb92101241703b)」：[最小費用流問題](https://qiita.com/SaitoTsutomu/items/41d625df63f1946c7216)として求解
- 前記事「[中学校の委員分け](https://qiita.com/SaitoTsutomu/items/9075a3f9b76e1abf4866)」：混合整数最適化として求解

##  方針

今回は、マッチング問題として解きます。
そのためには、委員の必要数がn人のときに、その委員のノードをn個に増やす必要があります。
また、[最大重み最大マッチング問題](https://qiita.com/SaitoTsutomu/items/bbebc69ebc2549b0d5d2)にするので、重みwを「40 - w」に変換します。

## 解いてみよう

```py
import networkx as nx

lst = [['タプリス', '風紀委員', 10], ['青葉', '学級代表', 10], ['かぐや', '風紀委員', 10],
       ['チノ', '学級代表', 10], ['ミラ', '風紀委員', 10],
       ['タプリス', '学級代表', 30], ['青葉', '図書委員', 30], ['かぐや', '図書委員', 30],
       ['チノ', '風紀委員', 30], ['ミラ', '学級代表', 30]]
need = {"学級代表": 1, "図書委員": 2, "風紀委員": 2}
g = nx.Graph()
lst2 = [(s, f'{c}{i}', 40 - w) for s, c, w in lst for i in range(need[c])]
g.add_weighted_edges_from(lst2)
print(nx.max_weight_matching(g, maxcardinality=True))
```

出力

```
{('かぐや', '図書委員1'),
 ('チノ', '学級代表0'),
 ('図書委員0', '青葉'),
 ('風紀委員0', 'ミラ'),
 ('風紀委員1', 'タプリス')}
```

元記事や前記事と同じ解が出ました。

## 補足

マッチングは社会の色々なところで使われます。たとえば、下記のマッチングを研究している先生のサイトに紹介されています（今回利用した[重みマッチング](https://qiita.com/SaitoTsutomu/items/bbebc69ebc2549b0d5d2)ではなく[安定マッチング](https://qiita.com/SaitoTsutomu/items/2ec5f7626054f4b4de63)ですが）。

参考：https://www.nii.ac.jp/faculty/informatics/yokoi_yu/

今回、`networkx.max_weight_matching`（エドモンズ法）で解きましたが、現実問題を解くときは、数理最適化モデルの方が柔軟にモデルを作成できますし、[高速に計算できる](https://qiita.com/SaitoTsutomu/items/7fd199a95d78a6f3b741)でしょう。



