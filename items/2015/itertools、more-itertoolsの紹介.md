title: itertools、more-itertoolsの紹介
tags: Python itertools
url: https://qiita.com/SaitoTsutomu/items/ddb5076ef62745f03b56
created_at: 2015-12-25 20:34:25+09:00
updated_at: 2024-07-22 00:11:23+09:00
body:

# itertools、more-itertools(10.3.0)の紹介 (2024年7月更新)

繰り返し関連の[itertools](https://docs.python.org/ja/3/library/itertools.html)、[more-itertools](https://more-itertools.readthedocs.io/)について紹介します。
itertoolsは標準ライブラリーなのでそのまま使えます。`more-itertools`は、`pip install more-itertools`とインストールすることで使えます。

各機能は、後述の表の**サンプルコード**という列を参考にしてください。

### 準備

サンプルコードをシンプルにするため、あらかじめ以下を実行したものとします。

```python
from itertools import *
from operator import gt, neg, not_, sub
from more_itertools import *

L = list  # リスト化
L0 = lambda it: [i[0] for i in it]  # 要素ごとに先頭
LL = lambda it: [list(i) for i in it]  # 要素をリスト化
LJ = lambda it: ["".join(i) for i in it]  # 要素をjoin
G = lambda it: [(k, list(v)) for k, v in it]  # 要素の2番目をリスト化
r3 = range(3)  # 1〜3
r1_5 = range(1, 6)  # 1〜5
```

## itertoolsの紹介

### 無限に続くもの

| 関数       | 引数              | 結果                                            |
| :--------- | :---------------- | :---------------------------------------------- |
| `count()`  | `start=0, step=1` | start, start+step, start+2*step, ...            |
| `cycle()`  | `iterable`        | p0, p1, ... p_last, p0, p1, ...                 |
| `repeat()` | `object [,times]` | object, object, object, ... 無限もしくはtimes回 |

| サンプルコード          | 実行結果                    |
| :---------------------- | :-------------------------- |
| `take(4, count(10))`    | `[10, 11, 12, 13]`          |
| `take(5, cycle('ABC'))` | `['A', 'B', 'C', 'A', 'B']` |
| `L(repeat(10, 3))`      | `[10, 10, 10]`              |



### 一番短い入力で止まるもの

| 関数                    | 引数                                   | 結果                     |
| :---------------------- | :------------------------------------- | :----------------------- |
| `accumulate()`          | `iterable, func=None, *, initial=None` | p0, p0+p1, p0+p1+p2, ... |
| `batched()`             | `iterable, n, *, strict=False`         | n個ずつまとめたもの      |
| `chain()`               | `*iterables`                           | 連結したもの             |
| `chain.from_iterable()` | `iterable`                             | 連結したもの             |

| サンプルコード                              | 実行結果                    |
| :------------------------------------------ | :-------------------------- |
| `L(accumulate(r1_5))`                       | `[1, 3, 6, 10, 15]`         |
| `LJ(batched('ABCDE', n=2))`                 | `['AB', 'CD', 'E']`         |
| `L(chain('AB', 'C', 'DE'))`                 | `['A', 'B', 'C', 'D', 'E']` |
| `L(chain.from_iterable(['AB', 'C', 'DE']))` | `['A', 'B', 'C', 'D', 'E']` |

**参考**

https://blog.pyq.jp/entry/python_kaiketsu_231108

<br>

| 関数            | 引数                  | 結果                                             |
| :-------------- | :-------------------- | :----------------------------------------------- |
| `compress()`    | `data, selectors`     | (d[0] if s[0]), (d[1] if s[1]), ...              |
| `dropwhile()`   | `predicate, iterable` | p_n, p_n+1, ...（predicateが偽の場所から始まる） |
| `filterfalse()` | `function, iterable`  | 偽になる要素                                     |

| サンプルコード                               | 実行結果               |
| :------------------------------------------- | :--------------------- |
| `L(compress('ABCDEF', [1, 0, 1, 0, 1, 1]))`  | `['A', 'C', 'E', 'F']` |
| `L(dropwhile(lambda x: x < 5, [1,4,6,4,1]))` | `[6, 4, 1]`            |
| `L(filterfalse(lambda x: x % 2, r1_5))`      | `[2, 4]`               |

<br>

| 関数         | 引数                                              | 結果                              |
| :----------- | :------------------------------------------------ | :-------------------------------- |
| `groupby()`  | `iterable, key=None`                              | keyの値で連続する値でグループ化   |
| `islice()`   | `iterable, stop`, `iterable, start, stop[, step]` | iterable[start:stop:step]         |
| `pairwise()` | `iterable`                                        | 隣通しをペアにして返す            |
| `starmap()`  | `function, iterable`                              | func(*seq[0]), func(*seq[1]), ... |

| サンプルコード                            | 実行結果                            |
| :---------------------------------------- | :---------------------------------- |
| `G(groupby('aab'))`                       | `[('a', ['a', 'a']), ('b', ['b'])]` |
| `L(islice(count(), 3, 8, 2))`             | `[3, 5, 7]`                         |
| `L(pairwise(r1_5))`                       | `[(1, 2), (2, 3), (3, 4), (4, 5)]`  |
| `L(starmap(pow, [(2,5), (3,2), (10,3)]))` | `[32, 9, 1000]`                     |

<p>

| 関数            | 引数                                     | 結果                                             |
| :-------------- | :--------------------------------------- | :----------------------------------------------- |
| `takewhile()`   | `predicate, iterable`                    | predicateが偽になるまで                          |
| `tee()`         | `iterable, n=2`                          | it1, it2 , ... itn 一つの反復子をn個に分ける |
| `zip_longest()` | `iter1 [,iter2 [...]], [fillvalue=None]` | (p[0], q[0]), (p[1], q[1]), ...                  |

| サンプルコード                                   | 実行結果                         |
| :----------------------------------------------- | :------------------------------- |
| `L(takewhile(lambda x: x < 5, [1, 4, 6, 4, 1]))` | `[1, 4]`                         |
| `LJ(tee('ABC'))`                                 | `['ABC', 'ABC']`                 |
| `L(zip_longest(r3, 'xy', fillvalue='-'))`        | `[(0, 'x'), (1, 'y'), (2, '-')]` |


### 組み合わせ

| 関数                              | 引数                 | 結果                                          |
| :-------------------------------- | :------------------- | :-------------------------------------------- |
| `product()`                       | *iterables, repeat=1 | デカルト積、ネストしたforループと等価         |
| `permutations()`                  | iterable, r=None     | 長さrのタプル列, 繰り返しを許さない順列       |
| `combinations()`                  | iterable, r          | 長さrのタプル列, 繰り返しを許さない組み合わせ |
| `combinations_with_replacement()` | iterable, r          | 長さrのタプル列, 繰り返しを許した組み合わせ   |

| サンプルコード                                | 実行結果                                                 |
| :-------------------------------------------- | :------------------------------------------------------- |
| `LJ(product('ABC', repeat=2))`                | `['AA', 'AB', 'AC', 'BA', 'BB', 'BC', 'CA', 'CB', 'CC']` |
| `LJ(permutations('ABC', 2))`                  | `['AB', 'AC', 'BA', 'BC', 'CA', 'CB']`                   |
| `LJ(combinations('ABC', 2))`                  | `['AB', 'AC', 'BC']`                                     |
| `LJ(combinations_with_replacement('ABC', 2))` | `['AA', 'AB', 'AC', 'BB', 'BC', 'CC']`                   |


---

## more_itertoolsの紹介

カテゴリごとに紹介します。

:::note info
**ノート**
`strict`引数を持つ一部の関数で、要素数が揃ってないときに`strict=True`を指定すると`ValueError`になります。
:::

### Grouping

| 関数             | 引数                      | 結果                           |
| :--------------- | :------------------------ | :----------------------------- |
| `chunked()`      | iterable, n, strict=False | n個ずつまとめてリスト化        |
| `ichunked()`     | iterable, n               | 要素がジェネレーターのchunked  |
| `chunked_even()` | iterable, n               | 長さの差が1になるようにchunked |

| サンプルコード                 | 実行結果                      |
| :----------------------------- | :---------------------------- |
| `L(chunked(r1_5, 2))`          | `[[1, 2], [3, 4], [5]]`       |
| `LL(ichunked(r1_5, 2))`        | `[[1, 2], [3, 4], [5]]`       |
| `L(chunked_even(range(7), 3))` | `[[0, 1, 2], [3, 4], [5, 6]]` |

#### n個ずつまとめたい場合

* 要素がタプル：`itertools.batched()`
* 要素がリスト：`more_itertools.chunked()`
* 要素がジェネレーター：`more_itertools.ichunked()`
* 要素の長さを揃えたい場合：`more_itertools.chunked_even()`

**参考**

https://blog.pyq.jp/entry/python_kaiketsu_231108

<p>

| 関数                    | 引数                                                            | 結果                                          |
| :---------------------- | :-------------------------------------------------------------- | :-------------------------------------------- |
| `sliced()`              | seq, n, strict=False                                            | sequenceで使えるchunked                       |
| `constrained_batches()` | iterable, max_size, max_count=None,<br>get_len=len, strict=True | 累積長さを上限以下にまとめる                  |
| `distribute()`          | n, iterable                                                     | 各反復子の順にたどって、n個の反復子を返す |
| `divide()`              | n, iterable                                                     | n個に分割して返す                             |

| サンプルコード            | 実行結果                                  |
| :------------------------ | :---------------------------------------- |
| `L(sliced(r1_5, 2))`      | `[range(1, 3), range(3, 5), range(5, 6)]` |
| `LL(distribute(2, r1_5))` | `[[1, 3, 5], [2, 4]]`                     |
| `LL(divide(2, r1_5))`     | `[[1, 2, 3], [4, 5]]`                     |

#### `constrained_batches()`のサンプルコード

下記では、文字列の長さの和が7を超えないようにまとめます。

```python
iterable = ["123", "1", "12345", "1", "1", "1", "1"]
print(L(constrained_batches(iterable, 7)))
>>>
[('123', '1'), ('12345', '1', '1'), ('1', '1')]
```

第3引数で要素数の上限を指定できます。

```python
print(L(constrained_batches(iterable, 7, 2)))
>>>
[('123', '1'), ('12345', '1'), ('1', '1'), ('1',)]
```

<p>

| 関数             | 引数                                              | 結果                           |
| :--------------- | :------------------------------------------------ | :----------------------------- |
| `split_at()`     | iterable, pred, maxsplit=-1, keep_separator=False | 条件を満たす要素を削除して分割 |
| `split_before()` | iterable, pred, maxsplit=-1                       | 条件を満たす前で分割           |
| `split_after()`  | iterable, pred, maxsplit=-1                       | 条件を満たす後で分割           |
| `split_into()`   | iterable, sizes                                   | sizesごとに分割                |
| `split_when()`   | iterable, pred, maxsplit=-1                       | 前後に対し、条件を満たせば分割 |

| サンプルコード                                  | 実行結果                               |
| :---------------------------------------------- | :------------------------------------- |
| `L(split_at('abcdba', lambda x: x == 'b'))`     | `[['a'], ['c', 'd'], ['a']]`           |
| `L(split_before('abcdba', lambda x: x == 'b'))` | `[['a'], ['b', 'c', 'd'], ['b', 'a']]` |
| `L(split_after('abcdba', lambda x: x == 'b'))`  | `[['a', 'b'], ['c', 'd', 'b'], ['a']]` |
| `L((split_into(r1_5, [1, 2, 2])))`              | `[[1], [2, 3], [4, 5]]`                |
| `L(split_when([1, 3, 2, 5, 2], gt))`            | `[[1, 3], [2, 5], [2]]`                |

<p>

| 関数          | 引数                                           | 結果                  |
| :------------ | :--------------------------------------------- | :-------------------- |
| `bucket()`    | iterable, key, validator=None                  | groupbyのようなもの   |
| `unzip()`     | iterable                                       | zipの逆               |
| `batched()`   | `itertools.batched`を参照                      |                       |
| `grouper()`   | iterable, n, incomplete='fill', fillvalue=None | n個ずつの組にして返す |
| `partition()` | pred, iterable                                 | 条件で分ける          |
| `transpose()` | it                                             | 行と列を入れ替え      |

| サンプルコード                         | 実行結果                                       |
| :------------------------------------- | :--------------------------------------------- |
| `LL(unzip(zip(r1_5, 'ABCDE')))`        | `[[1, 2, 3, 4, 5], ['A', 'B', 'C', 'D', 'E']]` |
| `L(grouper('ABC', 2))`                 | `[('A', 'B'), ('C', None)]`                    |
| `LL(partition(lambda x: x % 2, r1_5))` | `[[2, 4], [1, 3, 5]]`                          |
| `L(transpose([r3, r3]))`               | `[(0, 0), (1, 1), (2, 2)]`                     |

※ `bucket()`のサンプルコードは省略します。

下記はすべて同じ結果です。

```python
LL(unzip(zip(r1_5, 'ABCDE')))
LL(zip(*zip(r1_5, 'ABCDE')))
LL(transpose(zip(r1_5, 'ABCDE')))
```

### Lookahead and lookback

| 関数         | 引数                  | 結果                                |
| :----------- | :-------------------- | :---------------------------------- |
| `spy()`      | iterable, n=1         | n個の先頭を見る                     |
| `peekable()` | iterable              | peek([default])で消費せずに値を見る |
| `seekable()` | iterable, maxlen=None | seek可能な反復子                |

サンプルコードは、[公式ドキュメント](https://more-itertools.readthedocs.io/en/stable/api.html#lookahead-and-lookback)を参照してください。

### Windowing

| 関数                   | 引数                           | 結果                          |
| :--------------------- | :----------------------------- | :---------------------------- |
| `windowed()`           | seq, n, fillvalue=None, step=1 | stepずつずらして、n個づつ返す |
| `substrings()`         | iterable                       | スライスとしての部分集合      |
| `substrings_indexes()` | seq, reverse=False             | インデックス付きsubstrings    |


| サンプルコード                | 実行結果                                   |
| :---------------------------- | :----------------------------------------- |
| `L(windowed(r1_5, 3))`        | `[(1, 2, 3), (2, 3, 4), (3, 4, 5)]`        |
| `LJ(substrings('ABC'))`       | `['A', 'B', 'C', 'AB', 'BC', 'ABC']`       |
| `L(substrings_indexes('AB'))` | `[('A', 0, 1), ('B', 1, 2), ('AB', 0, 2)]` |

<p>

| 関数                  | 引数                                                           | 結果                                  |
| :-------------------- | :------------------------------------------------------------- | :------------------------------------ |
| `stagger()`           | iterable, offsets=(-1, 0, 1),<br>longest=False, fillvalue=None | 前後も返す                            |
| `windowed_complete()` | iterable, n                                                    | 3分割を列挙する。真ん中の要素数はn    |
| `pairwise()`          | `itertools.pairwise`を参照                                     |                                       |
| `triplewise()`        | iterable                                                       | 1つスライドしつつ、三つ組みで返す |
| `sliding_window()`    | iterable, n                                                    | 1つスライドしつつ、n個ずつ返す    |
| `subslices()`         | iterable                                                       | スライスとしての部分集合              |


| サンプルコード                  | 実行結果                                               |
| :------------------------------ | :----------------------------------------------------- |
| `L(stagger(r1_5))`              | `[(None, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5)]`      |
| `L(windowed_complete(r1_5, 4))` | `[((), (1, 2, 3, 4), (5,)), ((1,), (2, 3, 4, 5), ())]` |
| `L(triplewise(r1_5))`           | `[(1, 2, 3), (2, 3, 4), (3, 4, 5)]`                    |
| `L(sliding_window(r1_5, 4))`    | `[(1, 2, 3, 4), (2, 3, 4, 5)]`                         |
| `LJ(subslices('ABC'))`          | `['A', 'AB', 'ABC', 'B', 'BC', 'C']`                   |

* `sliding_window()`でできることは`windowed()`でもできますが、`windowed()`の方が多機能です。
* `substrings()`と`subslices()`は同じ機能ですが、要素がタプルとリストで異なります。また、順序も異なります。

### Augmenting

| 関数            | 引数                                                     | 結果                                         |
| :-------------- | :------------------------------------------------------- | :------------------------------------------- |
| `count_cycle()` | iterable, n=None                                         | n回、cycle。要素は繰返し回数と元の値のタプル |
| `intersperse()` | e, iterable, n=1                                         | 間にeを挿入                                  |
| `padded()`      | iterable, fillvalue=None,<br>n=None, next_multiple=False | n個になるまで埋める                          |
| `repeat_each()` | iterable , n=2                                           | 要素をn回ずつ繰り返す                        |
| `mark_ends()`   | iterable                                                 | (先頭か、末尾か、要素)に変換                 |
| `repeat_last()` | iterable, default=None                                   | 最後の要素をずっと繰り返す                   |

| サンプルコード                | 実行結果                                                  |
| :---------------------------- | :-------------------------------------------------------- |
| `L(count_cycle('AB', 2))`     | `[(0, 'A'), (0, 'B'), (1, 'A'), (1, 'B')]`                |
| `L(intersperse('-', 'ABC'))`  | `['A', '-', 'B', '-', 'C']`                               |
| `L(padded('AB', '-', 4))`     | `['A', 'B', '-', '-']`                                    |
| `L(repeat_each(r3, 2))`       | `[0, 0, 1, 1, 2, 2]`                                      |
| `L(mark_ends(r3))`            | `[(True, False, 0), (False, False, 1), (False, True, 2)]` |
| `take(4, repeat_last('ABC'))` | `['A', 'B', 'C', 'C']`                                    |

<p>

| 関数                  | 引数                                                    | 結果                         |
| :-------------------- | :------------------------------------------------------ | :--------------------------- |
| `adjacent()`          | predicate, iterable, distance=1                         | 条件一致する前後もTrueに     |
| `groupby_transform()` | iterable, keyfunc=None, valuefunc=None, reducefunc=None | groupby後に、キーと値を変換  |
| `pad_none()`          | iterable                                                | 反復子が終了したらNoneを返す |
| `ncycles()`           | iterable, n                                             | 反復子をn回繰り返す          |

| サンプルコード                                | 実行結果                                                    |
| :-------------------------------------------- | :---------------------------------------------------------- |
| `L(adjacent(lambda x: x == 3, r1_5))`         | `[(False, 1), (True, 2), (True, 3), (True, 4), (False, 5)]` |
| `G(groupby_transform('ABB', ord, str.lower))` | `[(65, ['a']), (66, ['b', 'b'])]`                           |
| `take(4, pad_none('AB'))`                     | `['A', 'B', None, None]`                                    |
| `L(ncycles('AB', 2))`                         | `['A', 'B', 'A', 'B']`                                      |

※ `repeat_each()`と`ncycles()`は、どちらも反復子をn回繰り返しますが、順番が異なります。

### Combining

| 関数                   | 引数                                                 | 結果                                               |
| :--------------------- | :--------------------------------------------------- | :------------------------------------------------- |
| `collapse()`           | iterable, base_type=None, levels=None                | 多段可のflatten                                    |
| `sort_together()`      | iterables, key_list=(0,),<br>key=None, reverse=False | 同じ順番で各要素を並べ替え                         |
| `interleave()`         | *iterables                                           | いずれかの反復子がなくなるまで各反復子から順に出力 |
| `interleave_longest()` | *iterables                                           | 各反復子から順に出力                               |
| `interleave_evenly()`  | *iterables, lengths=None                             | 各反復子から均等になるように出力                   |

| サンプルコード                             | 実行結果                         |
| :----------------------------------------- | :------------------------------- |
| `L(collapse([[1], 2, [[3], [[4, 5]]]]))`   | `[1, 2, 3, 4, 5]`                |
| `sort_together(["BAC", r3])`               | `[('A', 'B', 'C'), (1, 0, 2)]`   |
| `L(interleave('ABC', 'D', 'EF'))`          | `['A', 'D', 'E']`                |
| `L(interleave_longest('ABC', 'D', 'EF'))`  | `['A', 'D', 'E', 'B', 'F', 'C']` |
| `L(interleave_evenly(['123', 'A', 'xy']))` | `['1', 'x', '2', 'A', '3', 'y']` |

※ `sort_together(["BAC", r3])`と`L(zip(*sorted(zip("BAC", r3))))`は同じ結果になります。

<p>

| 関数              | 引数                                                  | 結果                                        |
| :---------------- | :---------------------------------------------------- | :------------------------------------------ |
| `zip_offset()`    | *iterables, offsets,<br>longest=False, fillvalue=None | offsetsを指定できるzip                      |
| `zip_equal()`     | *iterables                                            | 長さが一致していないとUnequalIterablesError |
| `zip_broadcast()` | *iterables                                            | スカラーも使えるzip                         |


| サンプルコード                            | 実行結果                               |
| :---------------------------------------- | :------------------------------------- |
| `L(zip_offset(r3, 'xy', offsets=[1, 0]))` | `[(1, 'x'), (2, 'y')]`                 |
| `L(zip_broadcast(-1, r3, 9))`             | `[(-1, 0, 9), (-1, 1, 9), (-1, 2, 9)]` |

※ `zip_equal()` のサンプルコードは省略します。

<p>

| 関数                | 引数            | 結果                                 |
| :------------------ | :-------------- | :----------------------------------- |
| `flatten()`         | listOfLists     | 要素をフラットにする                 |
| `roundrobin()`      | *iterables      | interleave_longestと同じ             |
| `prepend()`         | value, iterator | 最初に要素を追加                     |
| `value_chain()`     | value, iterator | 要素をフラットにする（文字列を除く） |
| `partial_product()` | value, iterator | デカルト積の一部を返す               |

| サンプルコード                          | 実行結果                       |
| :-------------------------------------- | :----------------------------- |
| `L(flatten([[1], [2, 3], [4]]))`        | `[1, 2, 3, 4]`                 |
| `L(prepend(1, [2, 3]))`                 | `[1, 2, 3]`                    |
| `L(value_chain([1, 2], 3))`             | `[1, 2, 3]`                    |
| `LJ(partial_product('AB', 'C', 'DEF'))` | `['ACD', 'BCD', 'BCE', 'BCF']` |

※ `roundrobin()`の出力は`interleave_longest()`と同じなのでサンプルコードは省略します。なお、サイズが小さい時に`roundrobin()`の方が高パフォーマンスかもしれません。
※ `partial_product()`はデカルト積の一部だけ返しますが、全反復子の全要素が必ず含まれます。

#### フラット化関数の違い

| 関数            | 引数の解釈                                                            | 文字列の扱い       |
| :-------------- | :-------------------------------------------------------------------- | :----------------- |
| `flatten()`     | 第1引数の各要素は1段とみなしスカラーは禁止                            | イテラブルとみなす |
| `prepend()`     | 第1引数はスカラーとみなす<br>第2引数の要素は1段とみなしスカラーは禁止 | イテラブルとみなす |
| `value_chain()` | 各引数は、スカラーまたは1段とみなす                                   | スカラーとみなす   |
| `collapse()`    | 第1引数の各要素は、スカラーまたは多段が使える                         | スカラーとみなす   |

### Summarizing

| 関数                   | 引数                           | 結果                           |
| :--------------------- | :----------------------------- | :----------------------------- |
| `ilen()`               | iterable                       | 要素数                         |
| `unique_to_each()`     | *iterables                     | 他反復子にないもの             |
| `sample()`             | iterable, k, weights=None      | iterableからサンプリング       |
| `consecutive_groups()` | iterable, ordering=lambda x: x | 要素が+1するものをグルーピング |

| サンプルコード                              | 実行結果                  |
| :------------------------------------------ | :------------------------ |
| `ilen(r1_5)`                                | `5`                       |
| `unique_to_each('AB', 'BC', 'DCA')`         | `[[], [], ['D']]`         |
| `LL(consecutive_groups([2, 3, -2, -1, 1]))` | `[[2, 3], [-2, -1], [1]]` |

※ `sample()`のサンプルコードは省略します。

<p>

| 関数                | 引数                                               | 結果                             |
| :------------------ | :------------------------------------------------- | :------------------------------- |
| `run_length.encode` | iterable                                           | 連続する要素と連続する数へ変換   |
| `run_length.decode` | iterable                                           | 連続する要素と連続する数から変換 |
| `map_reduce()`      | iterable, keyfunc, valuefunc=None, reducefunc=None | 適用して辞書化                   |
| `join_mappings()`   | **field_to_map                                     | 複数辞書から辞書の辞書を作成     |
| `exactly_n()`       | iterable, n, predicate=bool                        | ちょうどn個かどうか              |
| `is_sorted()`       | iterable, key=None, reverse=False, strict=False    | ソートされているかどうか         |

| サンプルコード                               | 実行結果                         |
| :------------------------------------------- | :------------------------------- |
| `L(run_length.encode('bbcaaa'))`             | `[('b', 2), ('c', 1), ('a', 3)]` |
| `L(run_length.decode([('b', 1), ('a', 2)]))` | `['b', 'a', 'a']`                |
| `dict(map_reduce('abb', lambda c: ord(c)))`  | `{97: ['a'], 98: ['b', 'b']}`    |
| `exactly_n(r1_5, 5)`                         | `True`                           |
| `is_sorted(r1_5)`                            | `True`                           |

※ `is_sorted()`で`strict=True`を指定すると、等しい値があるとFalseになります。

#### `join_mappings()`のサンプルコード

```python
person_points = {1: 10, 2: 20}
person_names = {1: "Alice", 2: "Bob"}
join_mappings(point=person_points, name=person_names)
>>>
{1: {'point': 10, 'name': 'Alice'}, 2: {'point': 20, 'name': 'Bob'}}
```

<p>

| 関数           | 引数                                                      | 結果                 |
| :------------- | :-------------------------------------------------------- | :------------------- |
| `all_equal()`  | iterable                                                  | 全要素が同じか       |
| `all_unique()` | iterable, key=None                                        | すべて異なるかどうか |
| `minmax()`     | iterable_or_value, *others,<br>key=None, default=<marker> | 最小値と最大値       |
| `first_true()` | iterable, default=None, pred=None                         | 最初に真になる値     |
| `quantify()`   | iterable, pred=bool                                       | Trueの数を返す       |
| `iequals()`    | *iterables                                                | すべて同順で同値か   |

| サンプルコード                           | 実行結果 |
| :--------------------------------------- | :------- |
| `all_equal('AAA')`                       | `True`   |
| `all_unique('ABA')`                      | `False`  |
| `minmax(r1_5)`                           | `(1, 5)` |
| `first_true(r1_5, pred=lambda x: x > 2)` | `3`      |
| `quantify([True, False, True])`          | `2`      |
| `iequals(r3, (0, 1, 2), [0, 1, 2])`      | `True`   |

### Selecting

| 関数                | 引数                                             | 結果                                                                     |
| :------------------ | :----------------------------------------------- | :----------------------------------------------------------------------- |
| `islice_extended()` | iterable, *arg                                   | 負を許すislice                                                           |
| `first()`           | iterable[, default]                              | 最初の要素、なければデフォルト値、<br>デフォルトなしはValueError         |
| `last()`            | iterable[, default]                              | 最後の要素、なければデフォルト値、<br>デフォルトなしはValueError         |
| `one()`             | iterable, too_short=None,<br>too_long=None       | 1要素以外はValueError                                                    |
| `only()`            | iterable, default=None,<br>too_long=None         | ちょうど1つならその値、0個ならデフォルト値、<br>そうでないならValueError |
| `strictly_n()`      | iterable, n,<br>too_short=None,<br>too_long=None | ちょうどn個か、<br>そうでないならValueError                              |

| サンプルコード                          | 実行結果    |
| :-------------------------------------- | :---------- |
| `L(islice_extended(count(), 7, 5, -1))` | `[7, 6]`    |
| `first([], 5)`                          | `5`         |
| `last(r1_5)`                            | `5`         |
| `one([5])`                              | `5`         |
| `only([], 5)`                           | `5`         |
| `L(strictly_n(r3, 3))`                  | `[0, 1, 2]` |

<p>

| 関数              | 引数                             | 結果                                       |
| :---------------- | :------------------------------- | :----------------------------------------- |
| `strip()`         | iterable, pred                   | 前後で条件が真が続く間、捨てた残り         |
| `lstrip()`        | iterable, pred                   | 条件で真が続く間、捨てた残り               |
| `rstrip()`        | iterable, pred                   | 後ろから条件で真が続く間、捨てた残り       |
| `filter_except()` | validator, iterable, *exceptions | validatorが例外を返すものを除く            |
| `map_except()`    | function, iterable, *exceptions  | 関数を適用する。例外を返すものを除く       |
| `filter_map()`    | func, iterable                   | 関数を適用する。Noneを除く                 |
| `iter_suppress()` | iterable, *exceptions            | 要素を順番に返す。指定した例外がでたら終了 |


| サンプルコード                        | 実行結果          |
| :------------------------------------ | :---------------- |
| `L(strip([0, 0, 1, 0, 2, 0], not_))`  | `[1, 0, 2]`       |
| `L(lstrip([0, 0, 1, 0, 2, 0], not_))` | `[1, 0, 2, 0]`    |
| `L(rstrip([0, 0, 1, 0, 2, 0], not_))` | `[0, 0, 1, 0, 2]` |

※ `filter_except()`、`map_except()`、`filter_map()`、`iter_suppress()`のサンプルコードは省略します。

<p>

| 関数                 | 引数                      | 結果                                                                  |
| :------------------- | :------------------------ | :-------------------------------------------------------------------- |
| `nth_or_last()`      | iterable, n[, default]    | nthか最後の要素、なければデフォルト値、<br>デフォルトなしはValueError |
| `unique_in_window()` | iterable, n, key=None     | n個以内でユニーク値なら返す                                           |
| `before_and_after()` | predicate, it             | predicateがFalseになる前と以降で分ける                                |
| `nth()`              | iterable, n, default=None | n番目の値を取得                                                       |
| `take()`             | n, iterable               | 最初のn個を返す                                                       |
| `tail()`             | n, iterable               | 後ろからn個                                                           |

| サンプルコード                              | 実行結果          |
| :------------------------------------------ | :---------------- |
| `nth_or_last(r1_5, 2)`                      | `3`               |
| `L(unique_in_window('ABAC', 3))`            | `['A', 'B', 'C']` |
| `LJ(before_and_after(str.islower, "abCd"))` | `['ab', 'Cd']`    |
| `nth(r1_5, 5)`                              | `None`            |
| `take(3, r1_5)`                             | `[1, 2, 3]`       |
| `L(tail(2, r1_5))`                          | `[4, 5]`          |

<p>

| 関数                    | 引数                                 | 結果                         |
| :---------------------- | :----------------------------------- | :--------------------------- |
| `unique_everseen()`     | iterable, key=None                   | ユニーク値を返す             |
| `unique_justseen()`     | iterable, key=None                   | 連続する値を除いて返す       |
| `unique()`              | iterable, key=None,<br>reverse=False | ソートしてユニーク値を返す   |
| `duplicates_everseen()` | iterable, key=None                   | 以前存在した値を返す         |
| `duplicates_justseen()` | iterable, key=None                   | 直前の値と同じなら返す       |
| `classify_unique()`     | iterable, key=None                   | 各要素ごとにユニーク性を返す |

| サンプルコード                            | 実行結果               |
| :---------------------------------------- | :--------------------- |
| `L(unique_everseen('ABBCcA', str.lower))` | `['A', 'B', 'C']`      |
| `L(unique_justseen('AABBCA'))`            | `['A', 'B', 'C', 'A']` |
| `L(unique('ACBCA'))`                      | `['A', 'B', 'C']`      |
| `L(duplicates_everseen("abaa"))`          | `['a', 'a']`           |
| `L(duplicates_justseen("abaa"))`          | `['a']`                |

#### `classify_unique()`のサンプルコード

```python
L(classify_unique("abaa"))
>>>
[('a', True, True), ('b', True, True), ('a', True, False), ('a', False, False)]
```

戻り値の要素の1番目は元の値を、2番目は`unique_justseen()`で出力されるかを、3番目は`unique_everseen()`で出力されるかを表します。

<p>

| 関数                      | 引数                | 結果                                      |
| :------------------------ | :------------------ | :---------------------------------------- |
| `longest_common_prefix()` | iterable            | 最長の接頭辞                              |
| `takewhile_inclusive()`   | predicate, iterable | predicateが偽になるまで（最後の値を含む） |


| サンプルコード                                          | 実行結果     |
| :------------------------------------------------------ | :----------- |
| `L(longest_common_prefix(['abcd', 'abc', 'abd']))`      | `['a', 'b']` |
| `L(takewhile_inclusive(lambda x: x < 5, [1, 4, 6, 4]))` | `[1, 4, 6]`  |

### Math

| 関数           | 引数           | 結果                     |
| :------------- | :------------- | :----------------------- |
| `dft()`        | xarr           | 離散フーリエ変換         |
| `idft()`       | Xarr           | 逆離散フーリエ変換       |
| `convolve()`   | signal, kernel | 畳み込み                 |
| `dotproduct()` | vec1, vec2     | 内積を返す               |
| `factor()`     | n              | 素因数分解して素数を返す |
| `matmul()`     | m1, m2         | 行列の積                 |

| サンプルコード                                  | 実行結果             |
| :---------------------------------------------- | :------------------- |
| `dotproduct([2, 2], [3, 3])`                    | `12`                 |
| `L(factor(360))`                                | `[2, 2, 2, 3, 3, 5]` |
| `L(matmul([(1, 2), (3, 1)], [(1, 2), (3, 1)]))` | `[(7, 4), (6, 7)]`   |

※ `dft()`、`idft()`、`convolve()`のサンプルコードは省略します。

<p>

| 関数                      | 引数            | 結果                                             |
| :------------------------ | :-------------- | :----------------------------------------------- |
| `polynomial_from_roots()` | roots           | 多項式の係数                                     |
| `polynomial_derivative()` | coefficients    | 多項式の一次導関数                               |
| `polynomial_eval()`       | coefficients, x | 特定の値で多項式の評価                           |
| `sieve()`                 | n               | n未満の素数を返す                                |
| `sum_of_squares()`        | it              | 自乗和                                           |
| `totient()`               | n               | n以下の自然数で、nと<br>互いに素となる個数を返す |


| サンプルコード                  | 実行結果                       |
| :------------------------------ | :----------------------------- |
| `polynomial_eval([1, 6, 9], 2)` | `25`                           |
| `L(sieve(20))`                  | `[2, 3, 5, 7, 11, 13, 17, 19]` |
| `sum_of_squares(range(4))`      | `14`                           |
| `totient(6)`                    | `2`                            |

※ `polynomial_from_roots()`、`polynomial_derivative()`のサンプルコードは省略します。

### Combinatorics

| 関数                      | 引数             | 結果                                             |
| :------------------------ | :--------------- | :----------------------------------------------- |
| `distinct_permutations()` | iterable, r=None | ユニークなpermutation                            |
| `distinct_combinations()` | iterable, r      | 重複を除く組み合わせ                             |
| `circular_shifts()`       | iterable         | shiftしたものを繰り返す                          |
| `partitions()`            | iterable         | 順序を保った分割の仕方を繰り返す                 |
| `set_partitions()`        | iterable, k=None | 順序を保たない分割の仕方を繰り返す。分割数指定可 |

| サンプルコード                           | 実行結果                            |
| :--------------------------------------- | :---------------------------------- |
| `L(distinct_permutations([1, 0, 1]))`    | `[(0, 1, 1), (1, 0, 1), (1, 1, 0)]` |
| `L(distinct_combinations([0, 0, 1], 2))` | `[(0, 0), (0, 1)]`                  |
| `circular_shifts(r3)`                    | `[(0, 1, 2), (1, 2, 0), (2, 0, 1)]` |

#### `partitions()`と`set_partitions()`のサンプルコード

```python
L(partitions(r3))
>>>
[[[0, 1, 2]], [[0], [1, 2]], [[0, 1], [2]], [[0], [1], [2]]]
```

```python
L(set_partitions(r3))
>>>
[[[0, 1, 2]], [[0], [1, 2]], [[0, 1], [2]], [[1], [0, 2]], [[0], [1], [2]]]
```

<p>

| 関数                                   | 引数              | 結果                                     |
| :------------------------------------- | :---------------- | :--------------------------------------- |
| `product_index()`                      | element, *args    | デカルト積（product）のインデックス      |
| `combination_index()`                  | element, iterable | 組み合わせ（combinations）のインデックス |
| `permutation_index()`                  | element, iterable | 順列（permutations）のインデックス       |
| `combination_with_replacement_index()` | element, iterable | 重複あり組み合わせのインデックス         |

| サンプルコード                                          | 実行結果 |
| :------------------------------------------------------ | :------- |
| `product_index(("2", "B"), "12", "ABC")`                | `4`      |
| `combination_index(('B', 'C'), "ABC")`                  | `2`      |
| `permutation_index(('B', 'C'), "ABC")`                  | `3`      |
| `combination_with_replacement_index(('B', 'C'), "ABC")` | `4`      |

<p>

| 関数                 | 引数                             | 結果                                    |
| :------------------- | :------------------------------- | :-------------------------------------- |
| `gray_product()`     | *iterables                       | （要素が1つだけ変化する順の）デカルト積 |
| `outer_product()`    | func, xs, ys,<br>*args, **kwargs | 一般化されたデカルト積を返す            |
| `powerset()`         | iterable                         | 各要素の全部分集合を返す                |
| `powerset_of_sets()` | iterable                         | 各要素の全部分集合を返す                |


| サンプルコード                  | 実行結果                    |
| :------------------------------ | :-------------------------- |
| `LJ(gray_product("AB", "CD"))`  | `['AC', 'BC', 'BD', 'AD']`  |
| `L(powerset(range(2)))`         | `[(), (0,), (1,), (0, 1)]`  |
| `L(powerset_of_sets(range(2)))` | `[set(), {0}, {1}, {0, 1}]` |

※ `outer_product()`のサンプルコードは省略します。

<p>

| 関数                                    | 引数             | 結果                            |
| :-------------------------------------- | :--------------- | :------------------------------ |
| `random_product()`                      | *args, repeat=1  | 各反復子ごとにランダムに返す    |
| `random_permutation()`                  | iterable, r=None | r個分ランダムに繰り返さずに返す |
| `random_combination()`                  | iterable, r      | ランダムにr個選ぶ               |
| `random_combination_with_replacement()` | iterable, r      | 重複を許してランダムにr個選ぶ   |


| サンプルコード                               | 実行結果          |
| :------------------------------------------- | :---------------- |
| `random_product(r1_5, 'ABC')`                | `(4, 'A')`        |
| `random_permutation(r1_5)`                   | `(4, 2, 5, 3, 1)` |
| `random_combination(r1_5, 3)`                | `(1, 2, 4)`       |
| `random_combination_with_replacement(r3, 5)` | `(0, 0, 1, 2, 2)` |

※ 実行ごとに結果は変わります。

<p>

| 関数                                 | 引数               | 結果                                   |
| :----------------------------------- | :----------------- | :------------------------------------- |
| `nth_product()`                      | index, *args       | list(product(*args))[index]            |
| `nth_permutation()`                  | iterable, r, index | list(permutations(iterable, r))[index] |
| `nth_combination()`                  | iterable, r, index | list(combinations(iterable, r))[index] |
| `nth_combination_with_replacement()` | iterable, r, index | list(combinations(iterable, r))[index] |

| サンプルコード                               | 実行結果 |
| :------------------------------------------- | :------- |
| `nth_product(5, r3, r3)`                     | `(1, 2)` |
| `nth_permutation(r3, 2, 3)`                  | `(1, 2)` |
| `nth_combination(r3, 2, 2)`                  | `(1, 2)` |
| `nth_combination_with_replacement(r3, 2, 4)` | `(1, 2)` |

### Wrapping

| 関数                  | 引数                                                | 結果                                                    |
| :-------------------- | :-------------------------------------------------- | :------------------------------------------------------ |
| `always_iterable()`   | obj[, base_type]                                    | iterableはそのまま、<br>iterableでないものもiterable に |
| `always_reversible()` | iterable                                            | reversedできないiterableも<br>reversedを適用する        |
| `countable()`         | iterable                                            | カウント可能な反復子を作成                              |
| `consumer()`          | func                                                | PEP342を実現するためのデコレーター                      |
| `with_iter()`         | context_manager                                     | withでラップする                                        |
| `callback_iter()`     | func, callback_kwd=<br>'callback', wait_seconds=0.1 | 関数を反復子化                                          |
| `iter_except()`       | func, exception,<br>first=None                      | エラーが出るまで繰り返す                                |

| サンプルコード                                             | 実行結果               |
| :--------------------------------------------------------- | :--------------------- |
| `L(always_iterable('AB')), L(always_iterable('AB', None))` | `(['AB'], ['A', 'B'])` |
| `L(always_reversible('AB'))`                               | `['B', 'A']`           |
| `(line.upper() for line in with_iter(open('foo')))`        | 省略                   |
| `L(iter_except([1, 3, 2].pop, IndexError))`                | `[2, 3, 1]`            |

`callback_iter()`のサンプルコードについては、[公式ドキュメント](https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.callback_iter)を参照してください。

※ `consumer()`のサンプルコードは省略します。

#### `countable()`のサンプルコード

```python
it = countable(["apple", "banana", "carrot"])
try:
    while True:
        print(it.items_seen, next(it))
except StopIteration:
    pass
>>>
0 apple
1 banana
2 carrot
```

### Others

| 関数        | 引数                                                      | 結果                                                    |
| :---------- | :-------------------------------------------------------- | :------------------------------------------------------ |
| `locate()`  | iterable, pred=bool,<br>window_size=None                  | 条件を満たすindexを返す                                 |
| `rlocate()` | iterable, pred=bool,<br>window_size=None                  | presがTrueになる位置を逆順で返す。<br>window_size指定可 |
| `replace()` | iterable, pred, substitutes,<br>count=None, window_size=1 | predを満たす要素をsubstitutesで<br>置き換える           |

| サンプルコード                        | 実行結果               |
| :------------------------------------ | :--------------------- |
| `L(locate([1, 1, 0, 1]))`             | `[0, 1, 3]`            |
| `L(rlocate([1, 1, 0, 1]))`            | `[3, 1, 0]`            |
| `L(replace('ABC', 'B'.__eq__, 'XY'))` | `['A', 'X', 'Y', 'C']` |

<p>

| 関数               | 引数                                                        | 結果                                       |
| :----------------- | :---------------------------------------------------------- | :----------------------------------------- |
| `numeric_range()`  | *args                                                       | 数値的なものを許すrange                    |
| `side_effect()`    | func, iterable, chunk_size=None,<br>before=None, after=None | 副作用を起こしてそのものを返す             |
| `iterate()`        | func, start                                                 | start, func(start), func(func(start)), ... |
| `difference()`     | iterable, func=sub, *, initial=None                         | 差分を返す。accumulateの逆                 |
| `make_decorator()` | wrapping_func, result_index=0                               | デコレーターを作る                         |

| サンプルコード                         | 実行結果               |
| :------------------------------------- | :--------------------- |
| `L(numeric_range(0, 2, 0.5))`          | `[0.0, 0.5, 1.0, 1.5]` |
| `take(4, iterate(lambda x: 2 * x, 1))` | `[1, 2, 4, 8]`         |
| `L(difference([1, 3, 6, 10]))`         | `[1, 2, 3, 4]`         |

※ `side_effect()`、`make_decorator()`のサンプルコードは省略します。

<p>

| 関数             | 引数                                                   | 結果                                                 |
| :--------------- | :----------------------------------------------------- | :--------------------------------------------------- |
| `SequenceView`   | target                                                 | read-only viewを作成する                             |
| `time_limited()` | limit_seconds, iterable                                | 実行時間制限のある反復子                             |
| `map_if()`       | iterable, pred, func,<br>func_else=<identity function> | predの評価でfunc<br>またはfunc_elseを実行            |
| `iter_index()`   | iterable, value,<br>start=0, stop=None                 | 値と等しいインデックス                               |
| `consume()`      | iterator, n=None                                       | 反復子をn進める。<br>nが未指定の場合、最後まで進める |

| サンプルコード               | 実行結果    |
| :--------------------------- | :---------- |
| `L(iter_index("ABAA", "A"))` | `[0, 2, 3]` |

※ `SequenceView`、`time_limited()`、`consume()`のサンプルコードは省略します。

#### `map_if()`のサンプルコード

```python
def is_even(x):
    return x % 2 == 0

L(map_if(r1_5, is_even, neg))
>>>
[1, -2, 3, -4, 5]
```

<p>

| 関数              | 引数                    | 結果                        |
| :---------------- | :---------------------- | :-------------------------- |
| `tabulate()`      | function, start=0       | functionを適用して返す      |
| `repeatfunc()`    | func, times=None, *args | times回funcの結果を繰り返す |
| `reshape()`       | matrix, cols            | 2次元データの列数を変える   |
| `doublestarmap()` | func, iterable          | starmapのキーワード引数版   |

| サンプルコード                            | 実行結果                 |
| :---------------------------------------- | :----------------------- |
| `take(5, tabulate(lambda x: x**2, -2))`   | `[4, 1, 0, 1, 4]`        |
| `L(repeatfunc(lambda: 9, 2))`             | `[9, 9]`                 |
| `L(reshape([(0, 1), (2, 3), (4, 5)], 3))` | `[(0, 1, 2), (3, 4, 5)]` |

#### `doublestarmap()`のサンプルコード

```python
lst = [{"base": 2, "exp": 3}, {"base": 5, "exp": -1}]
L(doublestarmap(pow, lst))
>>>
[8, 0.2]
```

## 参考

- [役に立つ繰り返し構文 - PyQ](https://pyq.jp/quests/#mo_iter)
- [色々な繰り返し用関数 - PyQ](https://pyq.jp/quests/#mo_more)

