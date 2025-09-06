title: Polars100本ノック
tags: Python データ分析 Polars uv(astral-sh)
url: https://qiita.com/SaitoTsutomu/items/1a19dd484c88b77a4f2a
created_at: 2025-08-05 22:35:08+09:00
updated_at: 2025-08-11 08:20:42+09:00
body:

## はじめに

以前公開した下記の記事に続き、Polars 100本ノックの第2弾を作成しましたので、ご紹介します。

https://qiita.com/SaitoTsutomu/items/debe20277e58f665e658

この演習は、すでにある程度Polarsの知識がある方を対象とした、知識の確認や腕試しを目的としています。そのため、この演習だけでPolarsの基礎からすべてを学ぶことは難しいかもしれません。

演習を進める中で不明な点が出てきた場合は、公式ドキュメントなどを参照することをおすすめします。

https://docs.pola.rs/

### 対象者

* Polarsの知識を腕試ししたい方
* Polarsの機能を体系的に整理・確認したい方

### 演習の特徴

* Polarsの主要な機能を網羅的に扱っています
* 各問題には模範解答が用意されています
* 解答が正しいかどうかをその場でチェックできます
* [索引](https://github.com/SaitoTsutomu/study-polars2/blob/master/nbs/index.md)から学習したい項目の問題を見つけられます

## 準備

演習環境のセットアップには`uv`を利用します。未インストールの方は、公式サイトの手順に従ってインストールしてください。

https://docs.astral.sh/uv/getting-started/installation/

次に、ターミナルで以下のコマンドを順に実行してください。

```shell
curl -L -o study-polars2.zip https://github.com/SaitoTsutomu/study-polars2/archive/refs/heads/master.zip
unzip study-polars2.zip
cd study-polars2-master
```

**注**: もし`curl`や`unzip`コマンドが利用できない場合は、リポジトリページの「[Download ZIP](https://github.com/SaitoTsutomu/study-polars2/archive/refs/heads/master.zip)」から手動でダウンロードし、ご自身の環境に合った方法で解凍してください。

## 演習開始

演習の内容は`nbs/study_polars2.ipynb`というJupyter Notebookファイルに記述されています。
次のコマンドを実行すると、このファイルが`work/study_polars2.ipynb`にコピーされ、Jupyter Labが起動します。

```
uv run study-polars2
```

:::note info
**補足**
2回目以降にコマンドを実行した場合、`work/study_polars2.ipynb`は上書きされず、前回の続きから演習を再開できます。もし最初からやり直したい場合は、`uv run study-polars2 --new`コマンドを実行してください。
:::

Jupyterで`study_polars2.ipynb`を開いて演習を始めてください。

### 手順

Jupyter Notebookは、以下の3種類のセルで構成されています。

* **青いセル**: 問題の説明が書かれているセル
* **白いセル**: 解答コードを記述するセル
* **黄色いセル**: 解答が正しいかチェックするためのセル

## 問題例

ほとんどの問題は1文で解答できますが、最後の2問だけ総合演習になっており、複数の機能を組み合わせて解答する必要があります。

最後の問題は次のようになっています。

> **問題 5.3.2 顧客のRFM分析**
この最終演習では、Online Retailデータセットを用いて、顧客セグメンテーションの一般的な手法であるRFM（Recency, Frequency, Monetary）分析を行います。これは、データクリーニング、時系列処理、複雑な集計など、多くのスキルを統合する実践的な課題です。
`_df`を元に、各顧客についてRFM指標を計算し、最終結果を変数`ans`に代入してください。
> 
> **手順**
> 
> 1.　データクリーニング
>   * InvoiceDateをdatetime型に変換(`format="%m/%d/%y %H:%M"`)
>   * Quantity > 0、UnitPrice > 0、CustomerIDが欠損以外でフィルタリング
> 
> 2.　RFM指標を計算
>   * CustomerIDでグループ化し以下を修正
>     * 列`Recency`として、「グループ化前のInvoiceDateの最大値」からInvoiceDateの最大値を引いた日数+1
>     * 列`Frequency`として、InvoiceNoのユニーク数
>     * 列`Monetary`として、(Quantity * UnitPrice)の合計
> 
> 3.　列`Monetary`で降順に、列`CustomerID`で昇順にソート


<details><summary>解答例</summary>

```python
# 1. データクリーニング
_tmp = _df.with_columns(
    col.InvoiceDate.str.to_datetime(format="%m/%d/%y %H:%M"),
).filter(
    col.Quantity > 0,
    col.UnitPrice > 0,
    col.CustomerID.is_not_null(),
)

# 2. RFM指標を計算
_tmp = (
    _tmp.with_columns(
        Recency=(
            col.InvoiceDate.max() - col.InvoiceDate.max().over("CustomerID")
        ).dt.total_days() + 1,
    )
    .group_by("CustomerID")
    .agg(
        col.Recency.first(),
        Frequency=col.InvoiceNo.n_unique(),
        Monetary=(col.Quantity * col.UnitPrice).sum(),
    )
)

# 3. 列`Monetary`で降順に、列`CustomerID`で昇順にソート
ans = _tmp.sort(["Monetary", "CustomerID"], descending=[True, False]).collect()
```
</details>

## さいごに

100本ノック、お疲れ様でした。

この演習を通して、Polarsの様々な機能に触れ、理解を深めることができたのであれば幸いです。

もし問題に誤りや分かりにくい点、あるいは「もっと良い解き方がある」といった改善案がありましたら、ぜひGitHubリポジトリのIssueやPull Requestにてご提案ください。皆様からのフィードバックをお待ちしております。

この演習が、皆さんのデータ分析ライフの一助となることを願っています。

