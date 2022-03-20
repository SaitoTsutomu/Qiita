title: Pythonによる最適化関連の投稿一覧をdockerに
tags: Python Docker 最適化 Jupyter 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/2bfacb7eba2d5d62aa29
created_at: 2016-04-19 12:06:23+09:00
updated_at: 2018-03-08 08:50:32+09:00
body:

# はじめに
私の組合せ最適化関連のいくつかの投稿をdockerにまとめました。
下記のように実行してJupyter上で確認できます。

## Windows & Mac
Kitematic で"tsutomu7/qiita-demo"を検索し、CREATEしてWEB PREVIEWの下をクリックしてください。

## Linux
```bash:bash
docker run -it -d -p 8888:8888 --name qiita-demo tsutomu7/qiita-demo
firefox 127.0.0.1:8888
# コンテナの削除
docker rm -f qiita-demo
```

Jupyterの一覧から、いずれかを選んでクリックすると、別画面が開きます。そこで、順番に「Shift+Enter」を押して実行できます。

# Dockerと投稿一覧
DockerHub: [tsutomu7/qiita-demo](https://hub.docker.com/r/tsutomu7/qiita-demo/)

1. 「因子の部屋」を組合せ最適で解く
- 「基礎からのベイズ統計学」の入社試験問題で考えたこと
- お釣りの枚数を計算する
- サイコロ勝負
- ナップサック問題の結果の図示
- フィボナッチ数列の計算の高速化(Python版)
- ミニサムとかミニマックスって何ですか？
- モンテカルロ法を用いた最短路の計算
- レストランの売上を組合せ最適化で最大化する
- 全域木を列挙する
- 双対問題を調べる
- 取得データ量を最大化するセンサー設置箇所を求める
- 巡視船の航路を最適化で求める
- 待ち行列について
- 数独を組合せ最適で解く
- 最適化でバラバラの写真を復元せよ！
- 最適化で道路設置
- 献立を組合せ最適化で考える
- 研修医配属問題をPythonで解いてみる
- 確率の問題
- 秘書問題（あるいは お見合い問題、あるいは浜辺の美女問題）
- 組合せ最適化で4色問題を解く
- 組合せ最適化でPyCon JP 2016の講演を決めよう
- 組合せ最適化で学会プログラムを作成する
- 組合せ最適化で道路を舗装せよ
- 組合せ最適化で録画番組を決める
- 組合せ最適化で麻雀のあがりを判定する
- 組合せ最適化による研磨回数の最小化

# おまけ
Arukasでサービスしてみました。(しばらくしたら消します)  
[qiita-demo on Arukasサーバー](https://qiita-demo.arukascloud.io/)

# 追記
- SaitoTsutimuのPythonの記事直近20を自動で表示するようにしました。
    - https://hub.docker.com/r/tsutomu7/qiita-jupyter/
        - ポータルのflaskのポートを5000にしています。
        - サブのJupyterのポートは8888にしています。
            - Kitematicのときは、8888に戻してください。
- 一時的にArukasで公開しました。
    - https://qiita-jupyter.arukascloud.io/

以上

