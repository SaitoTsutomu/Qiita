title: Polarsの学習教材の紹介
tags: Python UV Polars
url: https://qiita.com/SaitoTsutomu/items/debe20277e58f665e658
created_at: 2024-11-03 10:31:47+09:00
updated_at: 2024-12-01 07:03:46+09:00
body:

## はじめに

「データサイエンティスト協会スキル定義委員」の「**データサイエンス100本ノック（構造化データ加工編）**」というのがあります。

この問題に追加／削除／アレンジした（学習ドリル的な）**学習教材**を作成したので紹介します。

この教材は知識の確認用なので、この教材だけではPolarsを学べません。出題範囲もPolarsの一部の機能だけです。実施にあたっては、必要に応じてドキュメントなどを読むことをおすすめします。

https://polars-ja.github.io/docs-ja/

### 対象者

* Polarsの知識を試してみたい人

### 教材の特徴

* 学習内容に応じて分類しました
* 模範解答を確認できます
* 正解かどうかをチェックできます

## 準備

`uv`を使います。次からインストールしてください。

https://docs.astral.sh/uv/getting-started/installation/

ターミナルで次を実行してください。`curl`が使えない場合は、この「[Download ZIP](https://github.com/SaitoTsutomu/study-polars/archive/refs/heads/master.zip)」をクリックしてください。また、`unzip`が使えない場合は、適宜解凍してください。

```
curl -L -o study-polars.zip https://github.com/SaitoTsutomu/study-polars/archive/refs/heads/master.zip
unzip study-polars.zip
cd study-polars-master
```

## 学習開始

教材は、`nbs/study_polars.ipynb`です。
次のコマンドを実行すると、教材を`work/study_polars.ipynb`にコピーし、Jupyterが起動します。

```
uv run study-polars
```

:::note info
**ノート**
`work/study_polars.ipynb`が存在する場合はコピーしません。2回目以降は続きから学習できます。もし、新規に始めたい場合は、`uv run study-polars --new`としてください。
:::

`study_polars.ipynb`を開いて学習を始めてください。

### 手順

* 青いセルの説明を読む
* 白いセルに問題の解答を書く
* 黄色いセルを実行して正解かどうかを確認する

### 問題例

![img.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/8388c185-77d6-2fa7-b910-890c621b5e2a.png)

## さいごに

Polarsは、はじめたばかりで、実務ではまだ使っていません。しかし、次のようなところが気にいっています。

* 高速！
* エクスプレッションがいい
  * 列ごとにメソッドチェーンを書けて柔軟
* 型などに厳しいので間違いに早く気づける
  * データが厳格でないとき、pandasは勝手に解釈するので探索的データ分析（EDA）に向いているが、実アプリケーションでリスクになる

基本的な処理を組み合わせて複雑な処理を書けるので、書きやすくわかりやすいと感じています。
（pandasだと、複雑な処理を短く書けることも多いですが、いざ書こうとしたときに、どう書くのか悩みやすい）

さいごに、本記事で紹介した学習教材一式は、次にあります。

https://github.com/SaitoTsutomu/study-polars

以上

