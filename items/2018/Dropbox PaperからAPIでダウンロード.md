title: Dropbox PaperからAPIでダウンロード
tags: Python Dropbox DropboxAPI dropboxPaper
url: https://qiita.com/SaitoTsutomu/items/6f48b93b2a64faa26447
created_at: 2018-04-21 15:02:05+09:00
updated_at: 2018-05-04 19:31:05+09:00
body:

# これなに
Dropbox Paperで定期的にエクスポートしていたが、時間がかかって困っていた。そこでAPIで自動化してみた。

## 結論

該当ページの`doc_id`が分かれば、簡単にできる。
`doc_id`は、URIのハイフン以降である。
備忘録として、手順を記す。

## Dropbox API Explorer

Dropbox API Explorerという非常に便利なものがあった。
下記サイトを開こう。
https://dropbox.github.io/dropbox-api-v2-explorer/
左のリストの下の方に**paper**というものがある。この下がDropbox PaperのAPIのようである。

### doc_idの一覧取得

`dcos/list`をクリックしよう。
https://dropbox.github.io/dropbox-api-v2-explorer/#paper_docs/list

- **Access Token**を設定しよう。持っていなければ、`Get Token`を押せばよい。
- **Request**は空のままでもよい。私は大量に結果が出たので、`filter by`を`docs_created`で自分が作成したものにした。
- **Submit Call**を押すと**Response**にdoc_idの一覧が表示される。

### doc_idの文書をDLするコードを調べる

`docs/download`を開こう。
https://dropbox.github.io/dropbox-api-v2-explorer/#paper_docs/download

各doc_idごとに以下実行できる。

- **Request**の`doc_id`に確認したいものを記入する。`export_format`は適宜選ぶ。
- **Submit Call**を押し、情報を確認する。

**Request**の**Show Code**を押し、**Code**でPython Request（requests library）を選択する。

下に出てくるコードをコピーして使える。

`r.ok`を確認し、`r.content.decode()`で中味を取り出せる。
タイトルは`eval(r.headers['Dropbox-Api-Result'])['title']`になる。


## 参考

APIは100回／日の制限があるらしい。

- [Dropbox PaperにMarkdownファイルをアップロードする](https://qiita.com/norikt/items/3d55b9b2bde88c1cef84)

