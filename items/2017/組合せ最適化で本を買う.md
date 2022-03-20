title: 組合せ最適化で本を買う
tags: Python 数学 最適化 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/aad6649cbdcc5eeb8cbb
created_at: 2017-11-22 07:13:31+09:00
updated_at: 2017-11-22 22:49:43+09:00
body:

# これなに
某社では、技術書やビジネス書を買うと一定額まで補助してもらえるそうです。(本は自分で所有できます)
買いたい本が複数あって、N回 補助の機会があるとき、どの本を買ったら良いでしょうか？
[組合せ最適化](http://qiita.com/SaitoTsutomu/items/bfbf4c185ed7004b5721)で計算してみましょう。

## 考え方

本を買ったら価値は9割になるとして、目的関数を「0.9×購入金額―自腹額」とします。
また、各機会ごとに合計購入金額が補助額を超えた分が自腹額となります。
この目的関数を最大化してみましょう。

下記は、N＝1のときの目的関数のイメージです。傾きは、左側が0.9で、右側が -0.1(=0.9-1)です。

![image.png](https://qiita-image-store.s3.amazonaws.com/0/13955/ca1531a2-ce6f-93a8-e22b-81a3809d9d52.png)

1冊の本は分割できないので、購入額候補（本の組合せ）は、離散的な点になります。

## 買いたい本のリスト

リストを表示します。

```py3:python
import numpy as np, pandas as pd
from pulp import *
from ortoolpy import addvars, addbinvars
a = pd.DataFrame([
    ('吾輩は猫だろう', 981),
    ('風の三四郎', 726),
    ('夏との扉', 1024),
    ('高い城の人', 1335),
    ('天王星年代記', 865),
    ('並列都市の科学', 1171),
    ('星は無慈悲な夜の王', 914),
    ('火の島かご', 463),
    ('ロボットは我', 758),
    ('未来世紀カガワ', 1507),
    ('ケイコとアベ', 689),
    ('48億円の身代金', 1412),
    ('星々の王女様', 826),
    ('猫とゆりかもめ', 649),
    ('風と共にとまる', 1083),
    ], columns=['Title', 'Price'])
a
```

<table>
  <thead>
    <tr>
      <th></th>
      <th>Title</th>
      <th>Price</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>吾輩は猫だろう</td>
      <td>981</td>
    </tr>
    <tr>
      <th>1</th>
      <td>風の三四郎</td>
      <td>726</td>
    </tr>
    <tr>
      <th>2</th>
      <td>夏との扉</td>
      <td>1024</td>
    </tr>
    <tr>
      <th>3</th>
      <td>高い城の人</td>
      <td>1335</td>
    </tr>
    <tr>
      <th>4</th>
      <td>天王星年代記</td>
      <td>865</td>
    </tr>
    <tr>
      <th>5</th>
      <td>並列都市の科学</td>
      <td>1171</td>
    </tr>
    <tr>
      <th>6</th>
      <td>星は無慈悲な夜の王</td>
      <td>914</td>
    </tr>
    <tr>
      <th>7</th>
      <td>火の島かご</td>
      <td>463</td>
    </tr>
    <tr>
      <th>8</th>
      <td>ロボットは我</td>
      <td>758</td>
    </tr>
    <tr>
      <th>9</th>
      <td>未来世紀カガワ</td>
      <td>1507</td>
    </tr>
    <tr>
      <th>10</th>
      <td>ケイコとアベ</td>
      <td>689</td>
    </tr>
    <tr>
      <th>11</th>
      <td>48億円の身代金</td>
      <td>1412</td>
    </tr>
    <tr>
      <th>12</th>
      <td>星々の王女様</td>
      <td>826</td>
    </tr>
    <tr>
      <th>13</th>
      <td>猫とゆりかもめ</td>
      <td>649</td>
    </tr>
    <tr>
      <th>14</th>
      <td>風と共にとまる</td>
      <td>1083</td>
    </tr>
  </tbody>
</table>

## Pythonで計算する

回数を4回、1回当たりの補助額を3000円とします。

```py3:python
N = 4 # 回数
S = 3000 # 1回当たりの補助額
m = LpProblem(sense=LpMaximize)
for i in range(N):
    a[f'Var{i}'] = addbinvars(len(a))
sums = addvars(N) # 購入額
owns = addvars(N) # 自腹額
m += 0.9*lpDot(a.Price,sum(a[f'Var{i}'] for i in range(N))) - lpSum(owns)
for i in range(N):
    m += sums[i] == lpDot(a.Price,a[f'Var{i}'])
    m += owns[i] >= sums[i] - S
for _,r in a.iterrows():
    m += lpSum(r[f'Var{i}'] for i in range(N)) <= 1 # 同じ本は1冊まで
%time m.solve()
print(LpStatus[m.status])
for i in range(N):
    a[f'Val{i}'] = a[f'Var{i}'].apply(value)
    print(a[a[f'Val{i}']>0.5].iloc[:,:2])
    print(f'{i+1} 合計 {value(sums[i])}')
>>>
Wall time: 49.8 s
Optimal
      Title  Price
9   未来世紀カガワ   1507
10   ケイコとアベ    689
12   星々の王女様    826
1 合計 3022.0
       Title  Price
1      風の三四郎    726
4     天王星年代記    865
11  48億円の身代金   1412
2 合計 3003.0
      Title  Price
5   並列都市の科学   1171
8    ロボットは我    758
14  風と共にとまる   1083
3 合計 3012.0
        Title  Price
0     吾輩は猫だろう    981
6   星は無慈悲な夜の王    914
7       火の島かご    463
13    猫とゆりかもめ    649
4 合計 3007.0
```

結構、時間がかかりますね。モデル化の工夫の余地があるかもしれません。
1回だけなら、「天王星年代記, 星は無慈悲な夜の王, 火の島かご, ロボットは我」を買うとちょうど3000円ですが、4回買うとすると、ちょうどの組合せはなくなりました。

以上

