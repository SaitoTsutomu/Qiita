title: joinの書き方クイズ
tags: Python クイズ join
url: https://qiita.com/SaitoTsutomu/items/173c490e2311cb816f9f
created_at: 2025-11-11 19:38:16+09:00
updated_at: 2025-12-05 07:04:02+09:00
body:

## 問題

次のPythonの記述はすべて同じ結果になります。
計算時間もほぼ一緒ですが、1つだけ少し時間がかかります。
その書き方はどれでしょうか？

1. `"".join(map(str, range(1_000_000)))`
2. `"".join(str(i) for i in range(1_000_000))`
3. `"".join([str(i) for i in range(1_000_000)])`

&nbsp;
&nbsp;
&nbsp;
&nbsp;
&nbsp;

## 解答

答えは`2`です。

実際に確認してみましょう。下記はPython 3.13で実行した結果です。

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/4e9d2a51-1130-47da-bdfb-764af7500752.png)


たしかに2番のジェネレーターだけ少し遅いです。

下記のブログによると、`str.join()`は、ジェネレーターを渡すとリストに変換してから計算するようです。
その変換の分だけ時間がよけいにかかると思われます。

https://berglyd.net/blog/2024/06/joining-strings-in-python/

`str.join()`の公式ドキュメントには、特に記述はないようです。

https://docs.python.org/ja/3.14/library/stdtypes.html#str.join

なお、先のブログによると、この現象はCPython特有とのことです。

## まとめ

`str.join()`の書き方の違いによる計算時間を確認しました。
ジェネレーターとリストの内包表記が同じ結果になるとき、一般に、ジェネレーターの方が効率的です。
しかし、`str.join()`に限っては内包表記の方が若干効率的になります。


