title: 無料JupyterサービスのBinderの紹介
tags: Python 最適化 パズル 組合せ最適化 binder
url: https://qiita.com/SaitoTsutomu/items/821ebd608c412e57382d
created_at: 2016-12-05 00:03:20+09:00
updated_at: 2017-09-10 18:38:06+09:00
body:

# これなに
[Binder](http://mybinder.org/)という無料サービスの紹介をします。
github上のJupyter notebook のリポジトリから、実行可能なサービスを簡単に試せます。

つまり、ブラウザだけでいろいろな実行環境を作ることができます。


# サンプルで試してみる
サンプルとして、私の公開しているパズルを解く[SaitoTsutomu/OptForPuzzle](https://github.com/SaitoTsutomu/OptForPuzzle)を試してみましょう。

## 手順
- http://mybinder.org/ を開いてください。
- Build a repositoryに「SaitoTsutomu/OptForPuzzle」と入力して、submitボタンを押してください。
  - 自動的にdockerのイメージが作成され[状態](http://mybinder.org/status/saitotsutomu/optforpuzzle)が更新されます。

![image.png](https://qiita-image-store.s3.amazonaws.com/0/13955/85f485e0-c91f-e238-079c-ab196476a188.png)


---
- completedが緑になったら、右上の[launchボタン](http://mybinder.org/repo/saitotsutomu/optforpuzzle)を押してください。
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/ba742893-9cae-bf86-ced2-facb84918199.png)

---
- Jupyter notebookが起動するので、適当に開いて実行してみましょう。
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/9b889bbf-cac4-aaa3-785d-9183fd1b2a18.png)

# GitHubリポジトリに必要なもの
- 1つ以上の拡張子が「.ipynb」のファイル
- requirements.txt (追加で必要なライブラリ)

以上

