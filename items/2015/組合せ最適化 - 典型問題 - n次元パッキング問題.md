title: 組合せ最適化 - 典型問題 - n次元パッキング問題
tags: Python 最適化 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/0ac9bd564ae9f91285d7
created_at: 2015-07-11 00:30:20+09:00
updated_at: 2017-09-29 19:45:56+09:00
body:

[典型問題と実行方法](0f6c1a4415d196e64314)

##n次元パッキング問題

n次元の直方体に、なるべく多くのn次元の直方体の詰込む。その方法を求めよ。
nは、1から3にあたる。nが1の場合、ナップサック問題で容量と価値が同じケースとなる。


##実行方法(ギロチンカットによる2次元パッキング問題)

```text:usage
Init signature: TwoDimPackingClass(self, width, height, items=None)
Docstring:
2次元パッキング問題
    ギロチンカットで元板からアイテムを切り出す(近似解法)
入力
    width, height: 元板の大きさ
    items: アイテムの(横,縦)のリスト
出力
    容積率と入ったアイテムの(横,縦,x,y)のリスト
```

```python:python
from ortoolpy import TwoDimPackingClass
TwoDimPackingClass(500, 300, [(240, 150), (260, 100), \
    (100, 200), (240, 150), (160, 200)]).solve()
```

```text:結果
(1.0,
 [(240, 150, 0, 0),
  (260, 100, 240, 0),
  (160, 200, 240, 100),
  (100, 200, 400, 100),
  (240, 150, 0, 150)])
```

```python:python
# pandas.DataFrame
from ortoolpy.optimization import TwoDimPacking
TwoDimPacking('data/tdpacking.csv', 500, 300)[1]
```

<table>
  <thead>
    <tr>
      <th></th>
      <th>width</th>
      <th>height</th>
      <th>x</th>
      <th>y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>240</td>
      <td>150</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>260</td>
      <td>100</td>
      <td>240</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>160</td>
      <td>200</td>
      <td>240</td>
      <td>100</td>
    </tr>
    <tr>
      <th>2</th>
      <td>100</td>
      <td>200</td>
      <td>400</td>
      <td>100</td>
    </tr>
    <tr>
      <th>3</th>
      <td>240</td>
      <td>150</td>
      <td>0</td>
      <td>150</td>
    </tr>
  </tbody>
</table>

##データ
- [data/tdpacking.csv](https://www.dropbox.com/s/y9tq0drwruyl8eo/tdpacking.csv)

