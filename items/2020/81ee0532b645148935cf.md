title: 続・組合せ最適化でN Queen問題を解く
tags: Python 数学 最適化 パズル 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/81ee0532b645148935cf
created_at: 2020-05-12 18:57:31+09:00
updated_at: 2020-05-12 18:57:31+09:00
body:

## これなに

N Queen問題を題材にした、組合せ最適化で求解するときのTipsです。

元記事：[組合せ最適化でN Queen問題を解く](https://qiita.com/SaitoTsutomu/items/8ae87b08668307b58006)

## 結論

制約の順番を変えると、計算時間が変わることがある。
4パターンで検証してみましょう。

## N Queen問題を解く

まずは、8x8で実際に解けるのを確認します。

```py
from ortoolpy import pd, addbinvars, model_min, lpSum, addvals
n = 8
df = pd.DataFrame([(i, j) for i in range(n) for j in range(n)],
                  columns=['X', 'Y'])
addbinvars(df);
m = model_min()
for i in range(n):
    m += lpSum(df[df.X == i].Var) == 1
    m += lpSum(df[df.Y == i].Var) == 1
for i in range(2 * n - 3):
    m += lpSum(df.query(f'X + Y == {i + 1}').Var) <= 1
    m += lpSum(df.query(f'X - Y == {i - n + 2}').Var) <= 1
%time m.solve()
addvals(df)
cc = df.Val.astype(int).map('.O'.__getitem__).values.reshape(n, n)
print('\n'.join(''.join(c) for c in cc))
```

出力

```
Wall time: 27 ms
..O.....
O.......
......O.
....O...
.......O
.O......
...O....
.....O..
```

次から 100 x 100 のサイズで4通りの定式化で実行時間を確認します。

## パターン1（4.0秒）

```py
m = model_min()
for i in range(n):
    m += lpSum(df[df.X == i].Var) == 1
    m += lpSum(df[df.Y == i].Var) == 1
for i in range(2 * n - 3):
    m += lpSum(df.query(f'X + Y == {i + 1}').Var) <= 1
    m += lpSum(df.query(f'X - Y == {i - n + 2}').Var) <= 1
%timeit -r 3 -n 3 m.solve()

```
3.97 s ± 702 ms per loop (mean ± std. dev. of 3 runs, 3 loops each)

## パターン2（4.7秒）

```py
m = model_min()
for i in range(n):
    m += lpSum(df[df.X == i].Var) == 1
    m += lpSum(df[df.Y == i].Var) == 1
for i in range(2 * n - 3):
    m += lpSum(df.query(f'X + Y == {i + 1}').Var) <= 1
for i in range(2 * n - 3):
    m += lpSum(df.query(f'X - Y == {i - n + 2}').Var) <= 1
%timeit -r 3 -n 3 m.solve()
```
4.7 s ± 423 ms per loop (mean ± std. dev. of 3 runs, 3 loops each)


## パターン3（2.2秒）

```py
m = model_min()
for i in range(n):
    m += lpSum(df[df.X == i].Var) == 1
for i in range(n):
    m += lpSum(df[df.Y == i].Var) == 1
for i in range(2 * n - 3):
    m += lpSum(df.query(f'X + Y == {i + 1}').Var) <= 1
    m += lpSum(df.query(f'X - Y == {i - n + 2}').Var) <= 1
%timeit -r 3 -n 3 m.solve()
```
2.24 s ± 36.5 ms per loop (mean ± std. dev. of 3 runs, 3 loops each)

## パターン4（6.4秒）

```py
m = model_min()
for i in range(n):
    m += lpSum(df[df.X == i].Var) == 1
for i in range(n):
    m += lpSum(df[df.Y == i].Var) == 1
for i in range(2 * n - 3):
    m += lpSum(df.query(f'X + Y == {i + 1}').Var) <= 1
for i in range(2 * n - 3):
    m += lpSum(df.query(f'X - Y == {i - n + 2}').Var) <= 1
%timeit -r 3 -n 3 m.solve()
```
6.44 s ± 129 ms per loop (mean ± std. dev. of 3 runs, 3 loops each)

## どうすればよいのか

4パターンは同じ定式化で、制約条件の順番が違うだけです。
しかし、3倍近く計算時間が変わってます。
しかも、nによって傾向が違います。

こういった場合は、今回のように複数パターンを用意して同時に実行し、答えが1つでも見つかったらすべて止める方法が良いかもしれません。

## 補足

計算は ThinkPad X280 でしました。
ライブラリーのインストールは、`pip install ortoolpy`です。

100 x 100 のN Queen問題は、0-1変数が1万個あります。
組み合わせは$10^{3010}$です。途方もない組み合わせ数ですが、無料のソフト（[PuLP](https://coin-or.github.io/pulp/)）で2秒ちょっとで解けるのがすごいですね。


