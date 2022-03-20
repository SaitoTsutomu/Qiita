title: itertools、more-itertoolsの紹介
tags: Python itertools
url: https://qiita.com/SaitoTsutomu/items/ddb5076ef62745f03b56
created_at: 2015-12-25 20:34:25+09:00
updated_at: 2020-11-08 18:59:33+09:00
body:

# itertools、more-itertools(8.6)の紹介 (2020年11月更新)

繰り返し関連のitertools、[more-itertools](https://more-itertools.readthedocs.io/)について紹介する。
itertoolsは標準なのでインストール不要、more-itertoolsは、`pip install more-itertools`でインストールする。

### 準備

サンプルをシンプルにするため、以下を実行したものとする。

```
L = list
L0 = lambda it: [i[0] for i in it]
LL = lambda it: [list(i) for i in it]
G = lambda it: [(k, list(v)) for k, v in it]
r3 = range(3)
r1_5 = range(1, 6)  # [1, 2, 3, 4, 5]
gt = operator.gt
not_ = operator.not_
```

## itertoolsの紹介

関数|引数|結果|例
:--|:--|:--|:--
`accumulate()` | iterable, func=None, *, initial=None | p0, p0+p1, p0+p1+p2, ... | `L(accumulate(r1_5)) --> [1, 3, 6, 10, 15]`
`chain()` | *iterables | 連結したもの | `L(chain('AB', 'C', 'DE')) --> ['A', 'B', 'C', 'D', 'E']`
`chain.from_iterable()` | iterable | 連結したもの | `L(chain.from_iterable(['AB', 'C', 'DE'])) --> ['A', 'B', 'C', 'D', 'E']`
`combinations()` | iterable, r | 長さrのタプル列, 繰り返しを許さない組合せ | `L(combinations('ABC', 2)) --> [('A', 'B'), ('A', 'C'), ('B', 'C')]`
`combinations_with_`<br>`replacement()` | iterable, r | 長さrのタプル列, 繰り返しを許した組合せ | `L(combinations_with_replacement('ABC', 2)) --> [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')]`
`compress()` | data, selectors | (d[0] if s[0]), (d[1] if s[1]), ... | `L(compress('ABCDEF', [1, 0, 1, 0, 1, 1])) --> ['A', 'C', 'E', 'F']`
`count()` | start=0, step=1 | start, start+step, start+2*step, ... | `take(4, count(10)) --> [10, 11, 12, 13]`
`cycle()` | iterable | p0, p1, ... plast, p0, p1, ... | `take(5, cycle('ABC')) --> ['A', 'B', 'C', 'A', 'B']`
`dropwhile()` | predicate, iterable | p_n, p_n+1, ...（predicateが偽の場所から始まる） | `L(dropwhile(lambda x: x < 5, [1,4,6,4,1])) --> [6, 4, 1]`
`filterfalse()` | function, iterable | 偽になる要素 | `L(filterfalse(lambda x: x % 2, r1_5)) --> [2, 4]`
`groupby()` | iterable, key=None | keyの値で連続する値でグループ化 | `G(groupby('aab')) --> [('a', ['a', 'a']), ('b', ['b'])]`
`islice()` | iterable, stop, iterable, start, stop[, step] | iterable[start:stop:step] | `L(islice(count(), 3, 8, 2)) --> [3, 5, 7]`
`permutations()` | iterable, r=None | 長さrのタプル列, 繰り返しを許さない順列 | `L(permutations('ABC', 2)) --> [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]`
`product()` | *iterables, repeat=1 | デカルト積、ネストしたforループと等価 | `L(product('ABC', repeat=2)) --> [('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'B'), ('C', 'C')]`
`repeat()` | object [,times] | object, object, object, ... 無限もしくはtimes回 | `L(repeat(10, 3)) --> [10, 10, 10]`
`starmap()` | function, iterable | func(*seq[0]), func(*seq[1]), ... | `L(starmap(pow, [(2,5), (3,2), (10,3)])) --> [32, 9, 1000]`
`takewhile()` | predicate, iterable | predicateが偽になるまで | `L(takewhile(lambda x: x < 5, [1, 4, 6, 4, 1])) --> [1, 4]`
`tee()` | iterable, n=2 |it1, it2 , ... itn 一つのイテレータをn個に分ける | `LL(tee('ABC')) --> [['A', 'B', 'C'], ['A', 'B', 'C']]`
`zip_longest()` | iter1 [,iter2 [...]], [fillvalue=None] | (p[0], q[0]), (p[1], q[1]), ... | `L(zip_longest(r3, 'xy', fillvalue='-')) --> [(0, 'x'), (1, 'y'), (2, '-')]`

## more_itertoolsの紹介

`strict`引数を持つ関数で、要素数が揃ってないときに、`strict=True`を指定すると`ValueError`になる。

### Grouping

| 関数             | 引数                        | 結果                                          | 例 |
|:-----------------|:----------------------------|:----------------------------------------------|:---|
| `chunked()`      | iterable, n, strict=False   | n個ずつまとめてリスト化                       | `L(chunked(r1_5, 2)) --> [[1, 2], [3, 4], [5]]` |
| `ichunked()`     | iterable, n                 | 要素がジェネレーターのchunked                 | `LL(ichunked(r1_5, 2)) --> [[1, 2], [3, 4], [5]]` |
| `sliced()`       | seq, n, strict=False        | squenceで使えるchunked                        | `L(sliced(r1_5, 2)) --> [range(1, 3), range(3, 5), range(5, 6)]` |
| `distribute()`   | n, iterable                 | 各iteratorの順にたどって、n個のiteratorを返す | `LL(distribute(2, r1_5)) --> [[1, 3, 5], [2, 4]]` |
| `divide()`       | n, iterable                 | n個に分割して返す                             | `LL(divide(2, r1_5)) --> [[1, 2, 3], [4, 5]]` |
| `split_at()`     | iterable, pred, maxsplit=-1, keep_separator=False | 条件を満たす要素を削除して分割 | `L(split_at('abcdba', lambda x: x == 'b')) --> [['a'], ['c', 'd'], ['a']]` |
| `split_before()` | iterable, pred, maxsplit=-1 | 条件を満たす後で分割                          | `L(split_before('abcdba', lambda x: x == 'b')) --> [['a'], ['b', 'c', 'd'], ['b', 'a']]` |
| `split_after()`  | iterable, pred, maxsplit=-1 | 条件を満たす前で分割                          | `L(split_after('abcdba', lambda x: x == 'b')) --> [['a', 'b'], ['c', 'd', 'b'], ['a']]` |
| `split_into()`   | iterable, sizes             | sizesごとに分割                               | `L((split_into(r1_5, [1, 2, 2]))) --> [[1], [2, 3], [4, 5]]` |
| `split_when()`   | iterable, pred, maxsplit=-1 | 前後に対し、条件を満たせば分割                | `L(split_when([1, 3, 2, 5, 2], operator.gt)) --> [[1, 3], [2, 5], [2]]` |
| `bucket()`       | iterable, key, validator=None | groupbyのようなもの                         | 省略 |
| `unzip()`        | iterable                    | zipの逆                                       | `LL(unzip(zip(r1_5, 'ABCDE'))) --> [[1, 2, 3, 4, 5], ['A', 'B', 'C', 'D', 'E']]` |
| `grouper()`      | n, iterable, fillvalue=None | n個ずつの組にして返す                         | `L(grouper(2, 'ABC', '-')) --> [('A', 'B'), ('C', '-')]` |
| `partition()`    | pred, iterable              | 条件で分ける                                  | `LL(partition(lambda x: x % 2, r1_5)) --> [[2, 4], [1, 3, 5]]` |

### Lookahead and lookback

| 関数         | 引数                  | 結果                                | 例   |
|:-------------|:----------------------|:------------------------------------|:-----|
| spy()        | iterable, n=1         | n個の先頭を見る                     | 省略 |
| peekable()   | iterable              | peek([default])で消費せずに値を見る | 省略 |
| seekable()   | iterable, maxlen=None | seek可能なイテレータ                | 省略 |

### Windowing

| 関数                   | 引数                  | 結果                             | 例 |
|:-----------------------|:----------------------|:---------------------------------|:---|
| `windowed()`           | seq, n, fillvalue=None, step=1 | stepずつずらして、n個づつ返す | `L(windowed(r1_5, 3)) --> [(1, 2, 3), (2, 3, 4), (3, 4, 5)]` |
| `substrings()`         | iterable              | 文字列のスライスとしての部分集合 | `L(substrings('AB')) --> [('A',), ('B',), ('A', 'B')]` |
| `substrings_indexes()` | seq, reverse=False    | インデックス付きsubstrings       | `L(substrings_indexes('AB')) --> [('A', 0, 1), ('B', 1, 2), ('AB', 0, 2)]` |
| `stagger()`            | iterable, offsets=(-1, 0, 1), longest=False, fillvalue=None | 前後も返す | `L(stagger(r1_5)) --> [(None, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5)]` |
| `windowed_complete()`  | iterable, n           | 3分割を列挙する。真ん中の要素数はn | `L(windowed_complete(r1_5, 4)) --> [((), (1, 2, 3, 4), (5,)), ((1,), (2, 3, 4, 5), ())]` |
| `pairwise()`           | iterable              | 隣通しをペアにして返す           | `L(pairwise(r1_5)) --> [(1, 2), (2, 3), (3, 4), (4, 5)]` |

### Augmenting

| 関数                  | 引数                         | 結果                                         | 例 |
|:----------------------|:-----------------------------|:---------------------------------------------|:---|
| `count_cycle()`       | iterable, n=None             | n回、cycle。要素は繰返し回数と元の値のタプル | `L(count_cycle('AB', 2)) --> [(0, 'A'), (0, 'B'), (1, 'A'), (1, 'B')]` |
| `intersperse()`       | e, iterable, n=1             | 間にeを挿入                                  | `L(intersperse('-', 'ABC')) --> ['A', '-', 'B', '-', 'C']` |
| `padded()`            | iterable, fillvalue=None, n=None, next_multiple=False | n個になるまで埋める | `L(padded('AB', '-', 4)) --> ['A', 'B', '-', '-']` |
| `mark_ends()`         | iterable                     | (先頭か、末尾か、要素)に変換                 | `L(mark_ends(r3)) --> [(True, False, 0), (False, False, 1), (False, True, 2)]` |
| `repeat_last()`       | iterable, default=None       | 最後の要素をずっと繰り返す                   | `take(4, repeat_last('ABC')) --> ['A', 'B', 'C', 'C']` |
| `adjacent()`          | predicate, iterable, distance=1 | 条件一致する前後もTrueに                  | `L(adjacent(lambda x: x == 3, r1_5)) --> [(False, 1), (True, 2), (True, 3), (True, 4), (False, 5)]` |
| `groupby_transform()` | iterable, keyfunc=None, valuefunc=None, reducefunc=None | groupby後に、キーと値を変換 | `G(groupby_transform('ABB', ord, str.lower)) --> [(65, ['a']), (66, ['b', 'b'])]` |
| `padnone()`           | iterable                     | 反復子が終了したらNoneを返す                 | `take(4, padnone('AB')) --> ['A', 'B', None, None]` |
| `ncycles()`           | iterable, n                  | 反復子をn回繰り返す                          | `L(ncycles('AB', 2)) --> ['A', 'B', 'A', 'B']` |

### Combining

| 関数            | 引数            | 結果                                             | 例 |
|:----------------|:----------------|:-------------------------------------------------|:---|
| `collapse()`    | iterable, base_type=None, levels=None | 多段可のflatten            | `L(collapse([[1], 2, [[3], [[4, 5]]]])) --> [1, 2, 3, 4, 5]` |
| `sort_together()` | iterables, key_list=(0,), reverse=False | 各々ソート             | 省略 |
| `interleave()`  | *iterables      | 何れかの反復子がなくなるまで各反復子から順に出力 | `L(interleave('ABC', 'D', 'EF')) --> ['A', 'D', 'E']`|
| `interleave_longest()` | *iterables | 各反復子から順に出力                           | `L(interleave_longest('ABC', 'D', 'EF')) --> ['A', 'D', 'E', 'B', 'F', 'C']` |
| `zip_offset()`         | *iterables, offsets, longest=False, fillvalue=None | offsetsを指定できるzip | `L(zip_offset(r3, 'xy', offsets=[1, 0])) --> [(1, 'x'), (2, 'y')]` |
| `zip_equal()`   | *iterables      | 長さが一致していないとエラー                     | 省略 |
| `dotproduct()`  | vec1, vec2      | 内積を返す                                       | `dotproduct([2, 2], [3, 3]) --> 12` |
| `flatten()`     | listOfLists     | 要素をフラットにする                             | `L(flatten([[1], [2, 3], [4]])) --> [1, 2, 3, 4]` |
| `roundrobin()`  | *iterables      | interleave_longestと同じ                         | 省略 |
| `prepend()`     | value, iterator | 最初に要素を追加                                 | `L(prepend(1, [2, 3])) --> [1, 2, 3]` |

### Summarizing

| 関数               | 引数                              | 結果                             | 例 |
|:-------------------|:----------------------------------|:---------------------------------|:---|
| `ilen()`           | iterable                          | 要素数                           | `ilen(r1_5) --> 5` |
| `unique_to_each()` | *iterables                        | 他反復子にないもの               | `unique_to_each('AB', 'BC', 'DCA') --> [[], [], ['D']]` |
| `sample()`         | iterable, k, weights=None         | iterableからサンプリング         | 省略 |
| `consecutive_groups()` | iterable, ordering=lambda x: x | 要素が+1するものをグルーピング | `LL(consecutive_groups([2, 3, -2, -1, 1])) --> [[2, 3], [-2, -1], [1]]` |
| `class run_length` | nan                               | 連続する要素と連続する数         | `L(run_length.encode('bbcaaa')) --> [('b', 2), ('c', 1), ('a', 3)]` |
| `map_reduce()`     | iterable, keyfunc, valuefunc=None, reducefunc=None | 適用して辞書化  | 省略 |
| `exactly_n()`      | iterable, n, predicate=bool       | ちょうどn個かどうか              | `exactly_n(r1_5, 5) --> True` |
| `is_sorted()`      | iterable, key=None, reverse=False | ソートされているかどうか         | `is_sorted(r1_5) --> True` |
| `all_equal()`      | iterable                          | 全要素が同じか                   | `all_equal('AAA') --> True` |
| `all_unique()`     | iterable, key=None                | すべて異なるかどうか             | `all_unique('ABA') --> False`
| `first_true()`     | iterable, default=None, pred=None | 最初に真になる値                 | `first_true(r1_5, pred=lambda x: x > 2) --> 3` |
| `quantify()`       | iterable, pred=bool               | Trueの数を返す                   | `quantify([True, False, True]) --> 2` |

### Selecting

| 関数                | 引数                             | 結果                                 | 例 |
|:--------------------|:---------------------------------|:-------------------------------------|:---|
| `islice_extended()` | iterable, *arg                   | 負を許すislice                       | `L(islice_extended(count(), 7, 5, -1)) --> [7, 6]` |
| `first()`           | iterable[, default]              | 最初の要素、なければデフォルト値、デフォルトなしはエラー | `first([], 5) --> 5` |
| `last()`            | iterable[, default]              | 最後の要素、なければデフォルト値、デフォルトなしはエラー | `last(r1_5) --> 5` |
| `one()`             | iterable, too_short=None, too_long=None | 1要素以外はエラー             | `one([5]) --> 5` |
| `only()`            | iterable, default=None, too_long=None | ちょうど1つならその値、0個ならデフォルト値、そうでないならエラー | `only([], 5) --> 5` |
| `strip()`           | iterable, pred                   | 前後で条件が真が続く間、捨てた残り   | `L(strip([0, 0, 1, 0, 2, 0], not_)) --> [1, 0, 2]` |
| `lstrip()`          | iterable, pred                              | 条件で真が続く間、捨てた残り | `L(lstrip([0, 0, 1, 0, 2, 0], not_)) --> [1, 0, 2, 0]` |
| `rstrip()`          | iterable, pred                              | 後ろから条件で真が続く間、捨てた残り | `L(rstrip([0, 0, 1, 0, 2, 0], not_)) --> [0, 0, 1, 0, 2]` |
| `filter_except()`   | validator, iterable, *exceptions | validatorが例外を返すものを除く      | 省略 |
| `map_except()`      | function, iterable, *exceptions  | 関数を適用する。例外を返すものを除く | 省略 |
| `nth_or_last()`     | iterable, n[, default]           | nthか最後の要素、なければデフォルト値、デフォルトなしはエラー | `nth_or_last(r1_5, 2) --> 3` |
| `nth()`             | iterable, n, default=None        | n番目の値を取得                      | `nth(r1_5, 5) --> None` |
| `take()`            | n, iterable                      | 最初のn個を返す                      | `take(3, r1_5) --> [1, 2, 3]` |
| `tail()`            | n, iterable                      | 後ろからn個                          | `L(tail(2, r1_5)) --> [4, 5]` |
| `unique_everseen()` | iterable, key=None               | ユニーク値を返す                     | `L(unique_everseen('ABBCcA', str.lower)) --> ['A', 'B', 'C']`|
| `unique_justseen()` | iterable, key=None               | 連続する値を除いて返す               | `L(unique_justseen('AABBCA')) --> ['A', 'B', 'C', 'A']` |

### Combinatorics

| 関数                   | 引数               | 結果                                             | 例 |
|:-----------------------|:-------------------|:-------------------------------------------------|:---|
| `distinct_permutations()` | iterable        | ユニークなpermutation                            | `L(distinct_permutations([1, 0, 1])) --> [(0, 1, 1), (1, 0, 1), (1, 1, 0)]` |
| `distinct_combinations()` | iterable, r     | 重複を除く組み合わせ                             | `L(distinct_combinations([0, 0, 1], 2)) --> [(0, 0), (0, 1)]` |
| `circular_shifts()`    | iterable           | shiftしたものを繰り返す                          | `circular_shifts(r3) --> [(0, 1, 2), (1, 2, 0), (2, 0, 1)]` |
| `partitions()`         | iterable           | 順序を保った分割の仕方を繰り返す                 | `L(partitions(r3)) --> [[[0, 1, 2]], [[0], [1, 2]], [[0, 1], [2]], [[0], [1], [2]]]` |
| `set_partitions()`     | iterable, k=None   | 順序を保たない分割の仕方を繰り返す。分割数指定可 | `L(set_partitions(r3)) --> [[[0, 1, 2]], [[0], [1, 2]], [[0, 1], [2]], [[1], [0, 2]], [[0], [1], [2]]]` |
| `powerset()`           | iterable           | 各要素の全部分集合を返す                         | `L(powerset(range(2))) --> [(), (0,), (1,), (0, 1)]` |
| `random_product()`     | *args, repeat=1    | 各反復子ごとにランダムに返す                     | `random_product(r1_5, 'ABC') --> (4, 'A')` |
| `random_permutation()` | iterable, r=None   | r個分ランダムに繰り返さずに返す                  | `random_permutation(r1_5) --> (4, 2, 5, 3, 1)` |
| `random_combination()` | iterable, r        | ランダムにr個選ぶ                                | `random_combination(r1_5, 3) --> (1, 2, 4)` |
| `random_combination_`<br>`with_replacement()` | iterable, r | 重複を許してランダムにr個選ぶ    | `random_combination_with_replacement(r3, 5) --> (0, 0, 1, 2, 2)` |
| `nth_product()`        | index, *args       | list(product(*args))[index]                      | `nth_product(5, r3, r3) --> (1, 2)` |
| `nth_permutation()`    | iterable, r, index | list(permutations(iterable, r))[index] | `nth_permutation(r3, 2, 3) --> (1, 2)` |
| `nth_combination()`    | iterable, r, index | list(combinations(iterable, r))[index] | `nth_combination(r3, 2, 2) --> (1, 2)` |

### Wrapping

| 関数                  | 引数             | 結果                                                | 例 |
|:----------------------|:-----------------|:----------------------------------------------------|:---|
| `always_iterable()`   | obj[, base_type] | iterableはそのまま、iterableでないものもiterable に | `L(always_iterable('AB')), L(always_iterable('AB', None)) --> (['AB'], ['A', 'B'])` |
| `always_reversible()` | iterable         | reversedできないiterableもreversedを適用する        | `L(always_reversible('AB')) --> ['B', 'A']` |
| `consumer()`          | func             | PEP342を実現するためのデコレーター                  | 省略 |
| `with_iter()`         | context_manager  | withでラップする                                    | `(line.upper() for line in with_iter(open('foo')))` |
| `iter_except()`       | func, exception, first=None | エラーが出るまで繰り返す                 | `L(iter_except([1,3,2].pop, IndexError)) --> [2, 3, 1]` |

### Others

| 関数              | 引数                                         | 結果                                           | 例 |
|:------------------|:---------------------------------------------|:-----------------------------------------------|:---|
| `locate()`        | iterable, pred=bool, window_size=None        | 条件を満たすindexを返す                        | `L(locate([1, 1, 0, 1])) --> [0, 1, 3]` |
| `rlocate()`       | iterable, pred=bool, window_size=None        | presがTrueになる位置を逆順で返す。window_size指定可 | `L(rlocate([1, 1, 0, 1])) --> [3, 1, 0]` |
| `replace()`       | iterable, pred, substitutes, count=None, window_size=1 | predを満たす要素をsubstitutesで置き換える      | `L(replace('ABC', 'B'.__eq__, 'XY')) --> ['A', 'X', 'Y', 'C']` |
| `numeric_range()` | *args                                        | 数値的なものを許すrange                        | `L(numeric_range(0, 2, 0.5)) --> [0.0, 0.5, 1.0, 1.5]` |
| `side_effect()`   | func, iterable, chunk_size=None, before=None, after=None | 副作用を起こしてそのものを返す     | 省略 |
| `iterate()`       | func, start                                  | start, func(start), func(func(start)), ...     | `take(4, iterate(lambda x: 2 * x, 1)) --> [1, 2, 4, 8]` |
| `difference()`    | iterable, func=operator.sub, *, initial=None | 差分を返す。accumulateの逆                     | `L(difference([1, 3, 6, 10])) --> [1, 2, 3, 4]` |
| `make_decorator()` | wrapping_func, result_index=0               | デコレーターを作る                             | 省略 |
| `class SequenceView` | target                                    | read-only viewを作成する                       | 省略 |
| `time_limited()`  | limit_seconds, iterable                      | 実行時間制限のあるイテラブル                   | 省略 |
| `consume()`       | iterator, n=None                             | 反復子をn進める。n==Noneの場合、最後まで進める | 省略 |
| `tabulate()`      | function, start=0                            | functionを適用して返す                         | `take(5, tabulate(lambda x: x**2, -2)) --> [4, 1, 0, 1, 4]` |
| `repeatfunc()`    | func, times=None, *args                      | times回funcの結果を繰り返す                    | `L(repeatfunc(lambda: 9, 2)) --> [9, 9]` |

### 参考

- [役に立つ繰り返し構文 - PyQ](https://pyq.jp/quests/#mo_iter)
- [色々な繰り返し用関数 - PyQ](https://pyq.jp/quests/#mo_more)

