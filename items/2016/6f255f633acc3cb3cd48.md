title: Jupyterを使ったハンズオンセミナーをdockerを使って開催する方法
tags: Python Docker Jupyter
url: https://qiita.com/SaitoTsutomu/items/6f255f633acc3cb3cd48
created_at: 2016-03-07 15:48:38+09:00
updated_at: 2016-03-09 17:24:00+09:00
body:

# <i class='fa fa-laptop' /> やりたいこと
- Jupyterなどを使ったハンズオンセミナーを開催したいとします。
- 実行環境は、dockerで用意することにします。
- Tmpnbのように、受講者ごとに動的にdockerコンテナを立ち上げて利用できるようにします。

# <i class='fa fa-laptop' /> 実現イメージ
![arch.png](https://qiita-image-store.s3.amazonaws.com/0/13955/54661e95-45c9-839a-d581-dcce71c182ec.png)

- pythonのflaskを使って、webサーバを立ち上げます。
- セミナーの受講者がアクセスすると、自動的にセミナーイメージからコンテナを起動して、そのアドレスをリダイレクトします。
- 下記の説明では、Ubuntu(15.10)上の docker(1.10.2)で確認しています。

webサーバでは、pythonのflaskとdockerの両方を動かします。
これをdockerで提供するのですが、どうせ、ホストでdockerを動かすので、ホストの環境を利用しましょう。pythonもexeとdllを別イメージからvolumeにコピーして、使うことにします。

# <i class='fa fa-laptop' /> Step 1. Making volume for python
pythonとflaskの実行環境を持った[tsutomu7/py3flask](https://hub.docker.com/r/tsutomu7/py3flask/)([Dokcerfile](https://github.com/Tsutomu-KKE/py3flask/blob/master/Dockerfile))からファイルをコピーして、pythonという名前のvolumeを作成します。コンテナはコピー後、廃棄します。

```bash:bash
docker volume rm python
docker run -it --rm -v python:/usr/local tsutomu7/py3flask sh -c "\
    cp /usr/bin/python3.5 /usr/local/bin/python && \
    cp /lib/ld-musl-x86_64.so.1 /usr/local/lib && \
    ln -s /usr/local/lib/ld-musl-x86_64.so.1 /usr/local/lib/libc.musl-x86_64.so.1 && \
    cp /usr/lib/libpython3.5m.so.1.0 /usr/local/lib/ && \
    cp -r /usr/lib/python3.5/ /usr/local/lib/"
```

# <i class='fa fa-laptop' /> Step 2. Start server
[tsutomu7/seminar](https://hub.docker.com/r/tsutomu7/seminar/)([Dockerfile](https://github.com/Tsutomu-KKE/seminar/blob/master/Dockerfile))を使ってwebサーバを起動します。

- **IMAGE環境変数で受講者に起動させたいdockerイメージを指定します**。
- PORT環境変数でそのイメージの利用するポート番号を指定します。
- CoreOSなどのように"/lib/x86_64-linux-gnu"がない場合は、その部分をとってください。

```bash:bash
docker run -it --rm \
   -v /lib/x86_64-linux-gnu/:/lib/x86_64-linux-gnu/:ro \
   -v /lib64:/lib64:ro \
   -v /usr/bin:/usr/bin:ro \
   -v /usr/lib:/usr/lib:ro \
   -v /var/run/docker.sock:/var/run/docker.sock:ro \
   -v python:/usr/local \
   -p 5000:5000 \
   -e IMAGE=tsutomu7/jupyter \
   -e PORT=8888 \
   tsutomu7/seminar
```

# <i class='fa fa-laptop' /> Step 3. Access
ネットワークにつながったPCから「webサーバのホストのアドレス:5000」にブラウザでアクセスしてください。自動的に新しい dockerコンテナが起動し、そのアドレスがリダイレクトされます。
同じPCからのアクセスは、1つのコンテナで対応します。

# <i class='fa fa-laptop' /> サーバプログラムの説明。
pythonもdockerも借り物なので、このサーバイメージは、5MBしかないです。中のプログラム([seminar.py](https://github.com/Tsutomu-KKE/seminar/blob/master/seminar.py))を説明します。

```py3:seminar.py
import os
from flask import Flask, request, redirect
from subprocess import run
app = Flask(__name__)
dct = {}

@app.route('/')
def hello_world():
    addr = request.environ['REMOTE_ADDR']
    if addr not in dct:
        img = os.environ.get('IMAGE', 'tsutomu7/jupyter')
        prt = os.environ.get('PORT', '8888')
        cid = 8001 + len(dct)
        run(['docker', 'run', '-d', '--name', str(cid), '-p', '%d:%s' % (cid, prt), img])
        srvr = request.environ['HTTP_HOST']
        if ':' in srvr:
            srvr = srvr[:srvr.index(':')]
        dct[addr] = 'http://%s:%d' % (srvr, cid)
    return redirect(dct[addr], 302)

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
```

- 同じPCからのアクセスでは、同じコンテナを使うようにします。その対応関係(アクセス元アドレス→コンテナのアドレス)をdctという辞書で持ちます。
- addrに、アクセス元アドレスを入れます。
- addrが最初のアクセスの時、以下を実行します。
  - imgに、受講者用のイメージ名を環境変数IMAGEから取得します。
  - prtに、そのイメージで用いるポート番号を環境変数PORTから取得します。
  - cidに、受講者用コンテナに対し、サーバ側で用いるポート番号を計算します。(8001から通し番号)
  - 受講者用コンテナを起動します。
  - srvrに、サーバのアドレスを入れて、元のポート番号(5000)を消して、新しいコンテナのポート番号を足して、dct[addr]に設定します。
- dct[addr]にリダイレクトします。

以上

