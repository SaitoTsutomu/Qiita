title: Polars `write_csv`と`StringIO`の罠：マルチバイト文字で発生した過去のバグとその原因
tags: Python StringIO Polars BytesIO
url: https://qiita.com/SaitoTsutomu/items/271d0e1b6d996d7ba830
created_at: 2025-07-26 18:02:13+09:00
updated_at: 2025-08-04 09:41:59+09:00
body:

## この記事の対象読者

* Pythonのデータ分析ライブラリPolarsを使用している方
* インメモリでCSVデータを扱おうとしている（例：ファイルに保存せずAPIレスポンスとして返したい）方
* `StringIO`と`BytesIO`の使い分けや、文字コードに起因する問題に関心のある方

## はじめに

Polarsは非常に高速なデータフレームライブラリですが、特定のバージョンで`write_csv`メソッドを`io.StringIO`と組み合わせて使うと、マルチバイト文字（日本語など）が正しく出力されないという問題がありました。

本記事では、Polars `v1.30.0`で発生したこの具体的な事象と、`io.BytesIO`を使った回避策、そしてその技術的な背景について解説します。

現在はPolars `v1.32.0`でこのバグは修正されていますが、ライブラリの内部動作やI/O処理の理解を深める良いケーススタディとなります。

## Polars v1.30.0で発生した問題

PolarsのDataFrameをCSV形式の「文字列」としてメモリ上で取得したい場合、`io.StringIO`を使うのが一般的な方法の一つです。

Polars `v1.29.0`までは、以下のコードで期待通りに動作していました。

```python
import io
import polars as pl

df = pl.DataFrame([{"name": "あいうえおかき", "price": 100}])
buf = io.StringIO()
df.write_csv(buf)
print("Polars version", pl.__version__)
print(buf.getvalue())
```

**出力(v1.29.0)**

```
Polars version 1.29.0
name,price
あいうえおかき,100
```

ところが、`v1.30.0`にアップデートすると、同じコードで意図しない出力が得られました。

```python
# (コードは上記と同一)
```

**出力(v1.30.0)**

```
Polars version 1.30.0
name,price
あいうえおかき,100
おかき,100
```

このように、後半のデータが重複し、一部が切り出されたような余分な行が追加されてしまいました。

### 技術的背景：`StringIO` vs `BytesIO`

この問題はなぜ発生したのでしょうか？鍵となるのは`StringIO`と`BytesIO`の性質の違いと、Polars内部でのデータ処理方法です。

* `io.StringIO`: **文字列**をメモリ上で扱うためのバッファで、文字単位でカーソルを操作
* `io.BytesIO`: **バイナリ**をメモリ上で扱うためのバッファで、バイト単位でカーソルを操作

CSVファイルは本質的にバイトのストリームです。特にUTF-8のような可変長エンコーディングでは、1文字が1バイト以上で表現されます（例：「あ」はUTF-8で3バイト）。

`v1.30.0`の`write_csv`は、内部的にバイト単位での書き込みやシーク（カーソル移動）を行っていたと推測されます。しかし、書き込み先が`StringIO`だったため、文字数とバイト数の不一致からカーソル位置の計算にズレが生じ、結果としてデータの破損や重複が発生したと考えられます。

この推測は、`io.BytesIO`を使うと問題が解決したことからも裏付けられます。


## 回避策と恒久対応

### 回避策: `io.BytesIO`の使用

問題が発生していた`v1.30.0`では、書き込み先を`StringIO`から`BytesIO`に変更することで、期待通りの結果を得ることができました。`BytesIO`はバイト単位でデータを扱うため、ライブラリ内部のバイト単位の処理と整合性が取れたのです。

```python
import io
import polars as pl

df = pl.DataFrame([{"name": "あいうえおかき", "price": 100}])
buf = io.BytesIO()  # 修正
df.write_csv(buf)
print("Polars version", pl.__version__)
print(buf.getvalue().decode())  # 修正
```

**出力(v1.30.0)**

```
Polars version 1.30.0
name,price
あいうえおかき,100
```

この経験から、`write_csv`のようにバイナリデータを扱う操作をインメモリで行う場合は、`BytesIO`を使う方がより安全といえそうです。

### 恒久対応: Polarsのバグ修正

この問題はPolars側のバグであったことが判明し、後のバージョンで修正されました。

https://github.com/pola-rs/polars/releases/tag/py-1.32.0

https://github.com/pola-rs/polars/pull/23647

Polars `v1.32.0`以降では、`StringIO`を使っても当初のコードが問題なく動作します。ライブラリ側で`StringIO`への書き込みが適切に処理されるようになったためです。

## まとめ

Polars `v1.30.0`では、`write_csv`と`StringIO`を組み合わせるとマルチバイト文字が破損するバグが存在しました。

原因は、ライブラリ内部のバイト単位の処理と、`StringIO`のテキスト単位の処理との間の不整合と推測されます。

`v1.30.0`でも`BytesIO`を用いることでこの問題を回避できました。このことからファイルI/Oをメモリ上で行う際は、`BytesIO`がより堅牢な選択肢となる可能性がありそうです。

この問題は**v1.32.0で修正済み**であり、現在は`StringIO`でも安全に利用できます。

ライブラリのバージョンアップによって思わぬ挙動に遭遇することもありますが、その原因を探ることで、PythonのI/O処理や文字コードに関する理解を深める良い機会となりました。

以上

