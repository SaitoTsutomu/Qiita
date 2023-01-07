title: Jupyter notebookのパスワード
tags: Python Security Jupyter
url: https://qiita.com/SaitoTsutomu/items/aee41edf1a990cad5be6
created_at: 2016-12-15 11:06:42+09:00
updated_at: 2022-10-24 13:20:59+09:00
body:

# Jupyter notebook最新版のセキュリティ
notebookパッケージが4.3になってから、セキュリティが強化されたようです。
参考: [Security in the Jupyter notebook server](https://jupyter-notebook.readthedocs.io/en/latest/security.html#server-security)

「jupyter notebook」とすると、パスワード入力を求められます。
![image](https://qiita-image-store.s3.amazonaws.com/0/13955/141fcd8b-c605-24b4-3e05-04a883876951.png)

下記の手順で使えるようになります。

## (1) 下記のように設定ファイルを作成する。

```
jupyter notebook --generate-config
```

## (2) 設定ファイルを編集する。
編集方法は、2種類あります。

 |方法|設定内容|説明
:--|:--|:--
A|tokenを設定|平文で文字を指定
B|passwordを設定|暗号化して設定

### (2-A) tokenを指定する場合
下記を~/.jupyter/jupyter_notebook_config.py に追加してください。(xxxは適宜変えてください)

> c.NotebookApp.token = 'xxx'

この場合、login画面のパスワードとして「xxx」を入力するか、ブラウザのURLで下記のようにするかのどちらかで利用できるようです。

> http:ホストのURL:8888/?token=xxx

### (2-B) passwordを指定する場合
まず、pythonで、下記を実行し、パスワード(例えば xxx)を2回入力し、ハッシュ文字を取得してください。

```
python -c 'from notebook.auth import passwd;print(passwd())'
>>>
sha1:152704c5513c:0e0781437e7d013892eb7662f5ee5a67b235ec1a
```

~/.jupyter/jupyter_notebook_config.py に下記のように追加してください。

> c.NotebookApp.password = 'sha1:152704c5513c:0e0781437e7d013892eb7662f5ee5a67b235ec1a'

この場合、login画面で指定したパスワードで入力できます。URLのオプションは使えないようです。

## 2022/08/02追記

JupyterLabの場合の説明ページ：https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html

以上

