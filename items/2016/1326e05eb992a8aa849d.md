title: AnacondaのJupyter notebookでnbextensionsを使う
tags: Python Docker Jupyter Anaconda
url: https://qiita.com/SaitoTsutomu/items/1326e05eb992a8aa849d
created_at: 2016-08-29 09:39:31+09:00
updated_at: 2017-03-13 14:41:36+09:00
body:

# はじめに
データ分析、機械学習、最適化、可視化で [Jupyter notebook](http://jupyter.org/)を使っている人が多いかと思います。
また、Pythonの実行環境構築のために、[anaconda](https://www.continuum.io/) を利用している人も増えているようです。
Jupyterの拡張機能として、[nbextensions](https://github.com/ipython-contrib/jupyter_contrib_nbextensions)がありますが、最新の anaconda の jupyter では、単純には利用できないようです。
ここでは、anaconda の jupyter でnbextensionsを使う方法を説明します。

# Anaconda cloudを使う
conda コマンドでは、continuum社で稼働確認したパッケージをインストールできます。それとは別に、[PyPI](https://pypi.python.org/)のように、anacondaに特化したコミュニティパッケージサイトがあります。それが、[anaconda cloud](https://anaconda.org/)です。このサイトの先人たちの用意してくれたパッケージを使うと、通常だと苦労するインストールがとてもはかどることがあります。

anaconda の jupyter でnbextensions を使う1つの方法として、下記のようにできます。

```bash:bash
conda install -y -c conda-forge jupyter_contrib_nbextensions
```

インストールできたら、jupyter notebook を起動してみましょう。下記のように nbextensions が使えるようになっています。

![image](https://qiita-image-store.s3.amazonaws.com/0/13955/07a94c7f-6c2d-884b-67d8-5bb607b9c1de.png)

また、"conda list | grep conda-forge" で conda-forge でインストールまたは更新されたパッケージを確認できます。

# 手っ取り早く docker で試す
docker も用意しました。下記のようにして、簡単に試せます。docker 起動後にブラウザを更新してください。

```bash:bash
firefox http://localhost:8888 &
docker run -it --rm -p 8888:8888 tsutomu7/jupyter
```

# Anaconda cloudで探す
上記の方法は、anaconda cloud のコマンドである anaconda で調べました。下記のようにすると、いくつかの候補が出てきますので、いろいろと試した結果、conda-forge がよさそうでしたので、利用しています。

```bash:bash
anaconda search nbextensions
```

以上

