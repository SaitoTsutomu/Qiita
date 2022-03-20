title: 自作のDockerイメージ一覧
tags: Python Docker データ分析 Jupyter 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/6a5cc3fb7ad43481ea4b
created_at: 2016-06-24 20:19:57+09:00
updated_at: 2018-03-06 10:31:16+09:00
body:

# これなに
自作のDockerイメージ一覧[^1]。(ダウンロード数の多い順に掲載、サイズはTagで確認したもの)
[^1]: ライセンスや著作権上で問題があれば、いってください

## 一覧
1. [tsutomu7/alpine-python](https://hub.docker.com/r/tsutomu7/alpine-python) (195 MB)
    - Alpine Linux で Python3.5と98パッケージを利用可能にしたもの
- [tsutomu7/jupyter](https://hub.docker.com/r/tsutomu7/jupyter) (272 MB)
    - tsutomu7/scientific-python で Jupyter を起動するようにしたもの
- [tsutomu7/scientific-python](https://hub.docker.com/r/tsutomu7/scientific-python) (272 MB)
    - Ubuntu16.04LTS で Python3.5と115パッケージを利用可能にしたもの
- [tsutomu7/opt-python](https://hub.docker.com/r/tsutomu7/opt-python) (277 MB)
    - tsutomu7/scientific-python にOpenOptなどを追加したもの
- [tsutomu7/ubuntu-essential](https://hub.docker.com/r/tsutomu7/ubuntu-essential) (37 MB)
    - textlab/ubuntu-essential をマネして作成 (基本的に Ubuntuはこれをベースにしている)
- [tsutomu7/pymc3](https://hub.docker.com/r/tsutomu7/pymc3) (373 MB)
    - Python3.5 に pymc3 など124パッケージを利用可能にしたもの
- [tsutomu7/python-opencv](https://hub.docker.com/r/tsutomu7/python-opencv) (221 MB)
    - Python3.5 に opencv3を利用可能にしたもの
- [tsutomu7/puzzle](https://hub.docker.com/r/tsutomu7/puzzle) (190 MB)
    - 「[数理最適化によるパズルの解法](https://github.com/SaitoTsutomu/OptForPuzzle)」をdocker化したもの
- [tsutomu7/standard](https://hub.docker.com/r/tsutomu7/standard) (273 MB)
    - 「[組合せ最適化 - 典型問題と実行方法](http://qiita.com/SaitoTsutomu/items/0f6c1a4415d196e64314)」をdocker化したもの
- [tsutomu7/qiita-demo](https://hub.docker.com/r/tsutomu7/qiita-demo) (202 MB)
    - 「[Pythonによる最適化関連の投稿一覧をdockerに](http://qiita.com/SaitoTsutomu/items/2bfacb7eba2d5d62aa29)」をdocker化したもの
- [tsutomu7/python](https://hub.docker.com/r/tsutomu7/python) (73 MB)
    - Ubuntu16.04LTS で Python3.5 だけ
- [tsutomu7/janome](https://hub.docker.com/r/tsutomu7/janome) (44 MB)
    - [Janome](http://blog.amedama.jp/entry/2015/11/26/210515)をdocker化したもの
- [tsutomu7/qiita-jupyter](https://hub.docker.com/r/tsutomu7/qiita-jupyter) (201 MB)
    - 「[Qiitaの記事とJupyter notebokとの相互変換](http://qiita.com/SaitoTsutomu/items/168400d2e3ea44a70022)」をdocker化したもの
- [tsutomu7/py3flask](https://hub.docker.com/r/tsutomu7/py3flask) (21 MB)
    - Python3.5 で、さくっと flask を使うためのもの
- [tsutomu7/dioc-python-3.5](https://hub.docker.com/r/tsutomu7/dioc-python-3.5) (299 MB)
    - 「[DigitalOceanの便利ツール作りました](http://qiita.com/SaitoTsutomu/items/2444668c9dedde0d77ae)」をdocker化したもの
- [tsutomu7/gotour](https://hub.docker.com/r/tsutomu7/gotour) (67 MB)
    - gotourをdocker化したもの
- [tsutomu7/keyvalue](https://hub.docker.com/r/tsutomu7/keyvalue) (33 MB)
    - 「[Jupyterのkernelを作ってみる](http://qiita.com/SaitoTsutomu/items/3c996bde01ef2637aadc)」をdocker化したもの
- [tsutomu7/py3sci](https://hub.docker.com/r/tsutomu7/py3sci) (386 MB)
    - tsutomu7/scientific-python の名残
- [tsutomu7/tex](https://hub.docker.com/r/tsutomu7/tex) (1 GB)
    - TeX Live 2013/Debian をdocker化したもの
- [tsutomu7/nim](https://hub.docker.com/r/tsutomu7/nim) (439 MB)
    - 「[Jupyterでnimを使おう](http://qiita.com/SaitoTsutomu/items/f79257430e2d8fcb9196)」をdocker化したもの
- [tsutomu7/golang](https://hub.docker.com/r/tsutomu7/golang) (231 MB)
    - 「[Jupyterでgolang](http://qiita.com/SaitoTsutomu/items/7421cea17e272612bd1a)」できるようにしたもの
- [tsutomu7/picntu](https://hub.docker.com/r/tsutomu7/picntu) (211 MB)
    - 「[絵によるプログラミング](http://qiita.com/SaitoTsutomu/items/d1e6593f76dd1b944803)」をdocker化したもの
- [tsutomu7/seminar](https://hub.docker.com/r/tsutomu7/seminar) (2 MB)
    - 「[Jupyterを使ったハンズオンセミナーをdockerを使って開催する方法](http://qiita.com/SaitoTsutomu/items/6f255f633acc3cb3cd48)」をdocker化したもの
- [tsutomu7/reversi](https://hub.docker.com/r/tsutomu7/reversi) (119 MB)
    - 「[オセロ(リバーシ)で遊ぶ](http://qiita.com/SaitoTsutomu/items/5824eb00250bf08f9197)」をdocker化したもの
- [tsutomu7/python-dep](https://hub.docker.com/r/tsutomu7/python-dep) (320 MB)
    - 「[pythonパッケージの依存関係をgraphvizで可視化](http://qiita.com/SaitoTsutomu/items/895dc98148942e740312)」をdocker化したもの
- [tsutomu7/uploader](https://hub.docker.com/r/tsutomu7/uploader) (5 MB)
    - 「[1バイナリのuploaderに感動した](http://qiita.com/tukiyo3/items/e27241025f2ad90f916c)」をマネしてファイルのアップロードを簡単にできるようにしたもの
- [tsutomu7/test_normal](https://hub.docker.com/r/tsutomu7/test_normal) (196 MB)
    - 「[正規分布の検証](http://qiita.com/SaitoTsutomu/items/e092b742a34354bdb9fd)」を簡単にできるようにしたもの
- [tsutomu7/auto_colorize](https://hub.docker.com/r/tsutomu7/auto_colorize) (1 GB)
    - 「[白黒写真の自動色付けをDockerで試す](http://qiita.com/fuji70/items/c72e2b557731971ac7d3)」をマネして docker化したもの
- [tsutomu7/gensim](https://hub.docker.com/r/tsutomu7/gensim) (93 MB)
    - Python 3.5 and gensim
- [tsutomu7/four-color](https://hub.docker.com/r/tsutomu7/four-color) (232 MB)
    - 「[組合せ最適化で4色問題を解く](http://qiita.com/SaitoTsutomu/items/2a8b5d1f0d39c6dc7f02)」をdocker化したもの
- [tsutomu7/sudouser](https://hub.docker.com/r/tsutomu7/sudouser) (38 MB)
    - sudoできるユーザのサンプル
- [tsutomu7/mxnet](https://hub.docker.com/r/tsutomu7/mxnet) (339 MB)
    - Deep Learning ライブラリの MXNET を docker化したもの
- [tsutomu7/negaposi](https://hub.docker.com/r/tsutomu7/negaposi) (33 MB)
    - 「[ネガポジ判定を行うGem作ってみた](http://qiita.com/moroku0519/items/e6352d31311418f38227)」をマネしてdocker化。
- [tsutomu7/smtp](https://hub.docker.com/r/tsutomu7/smtp) (56 MB)
    - SMTP Server。常時起動するのでなければ、使うべきでない。
- [tsutomu7/alpine-glibc](https://hub.docker.com/r/tsutomu7/alpine-glibc) (5 MB)
    - frolvlad/alpine-glibcをマネしたもの
- [tsutomu7/monkey](https://hub.docker.com/r/tsutomu7/monkey) (206 MB)
    - 「[読書猿Classic:ライブラリーリサーチのための対話環境をJupyter Notebookの上につくってみた](http://readingmonkey.blog45.fc2.com/blog-entry-769.html)」を無理矢理 docker化したもの。エラーになるもの多し。公開OKなのか？

## 分類
- Python関係(29/36)、OS関係(3/36)、Golang関係(2/36)、その他(2/36)
- Ubuntuベース(20/36)、Alpine(15/36)、Debian(1/36)

## 所感
- Dockerでは、GUIが扱いづらいので、ブラウザベースやテキストベースのサービスになる。
    - Jupyter notebookベースが便利である。
- blaze(llvmlite)など、Alpineで動かないものがあるが、今後はAlpineが増えるだろう。Alpine以外であれば、Ubuntuが便利である。
- Pythonのインストールは、Minicondaが非常に便利である。**Ubuntuに最初から入っていればいい**のに。

以上

