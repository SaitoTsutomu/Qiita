title: DockerでJupyterを起動するまで
tags: Python VirtualBox Docker
url: https://qiita.com/SaitoTsutomu/items/29414e2d4f30b2bc94ae
created_at: 2015-12-03 00:06:23+09:00
updated_at: 2015-12-04 16:29:25+09:00
body:

これは、[Python Advent Calendar 2015](http://qiita.com/advent-calendar/2015/python)の3日目の記事です。

# 何をするのか？
WindowsやMacで、いろいろなパッケージを含めてJupyter(IPython Notebook)を使おうとすると、インストールが大変です。そこで、今回は、Dockerを使って、Windows(64ビット)上にJupyterを起動するまでを、説明します。利用できるパッケージは、[DockerHub](https://hub.docker.com/r/tsutomu7/jupyter/)をご確認ください。
サクッとやりたい場合は、[Docker Toolboxを使う方法](#docker-toolboxを使う方法)を見てください。
いろいろ試したい場合は、[Ubuntuを入れてDockerを使う方法](#ubuntuを入れてdockerを使う方法)を見て下さい。

# Docker Toolboxを使う方法

Docker Toolboxを使うことで、簡単にDockerを使えるようになります。
Docker Toolboxをインストールすると、下記のソフトウェアが使えるようになります。

- Docker Client：シェルで操作
- Docker Machine：ホストの作成
- Docker Compose：複数コンテナ操作
- Docker Kitematic：GUIで操作
- VirtualBox：仮想OS（CoreOS）の実行

## Docker Toolboxのインストール
[Docker Toolbox](https://www.docker.com/docker-toolbox)からインストーラをダウンロードして、インストールしてください。

## Kitematicの起動
Docker Toolboxの中のKitematicを使うと、GUI上からDockerを操作できます。Kitematicを起動してください。
下記のように検索テキストに[tsutomu7/jupyter]を入れて、[CREATE]ボタンを押してください。
<img width="485" alt="1.png" src="https://qiita-image-store.s3.amazonaws.com/0/13955/0ab4e84b-1d9c-dd35-1f87-a755a0549ef8.png">

しばらくすると、ステータスが[RUNNING]になります。右下の[VOLUMES]の[/jupyter]をクリックし、[Enable Volumes]を選ぶとWindows上にファイルを保存できるようになります。[WEB PREVIEW]の下をクリックするとブラウザが起動してJupyterを使うことができます。
<img width="485" alt="2.png" src="https://qiita-image-store.s3.amazonaws.com/0/13955/9edc2336-b3bf-b779-25db-2debf71d1b82.png">

ブラウザで右上の[New]から[Python3]を選んでください。
<img width="516" alt="3.png" src="https://qiita-image-store.s3.amazonaws.com/0/13955/84d127f9-8466-b6b2-f52d-ebc330b3d3b0.png">

[Untitled1.ipynb]が開いたら、「!conda list」を打ち込んで、[Shift＋Enter]を押すと、インストールされているパッケージの一覧が表示されます。

# Ubuntuを入れてDockerを使う方法
下記について順番に説明します。

- [VirtualBoxのインストール](#virtualboxのインストール)
- [Ubuntuのインストール](#ubuntuのインストール)
- [仮想マシンの登録と起動](#仮想マシンの登録と起動)
- [Ubuntuの設定](#ubuntuの設定)
- [Ubuntuの起動とDockerのインストール](#ubuntuの起動とdockerのインストール)
- [Jupyterの起動](#jupyterの起動)


## VirtualBoxのインストール

[Download VirtualBox](https://www.virtualbox.org/wiki/Downloads)から自分のOSのインストーラをダウンロードしインストールしてください。
必須ではないですが、[エクステンションパックの導入](http://vboxmania.net/content/%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%86%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%B3%E3%83%91%E3%83%83%E3%82%AF%E3%81%AE%E5%B0%8E%E5%85%A5)をしておくと便利です。

## Ubuntuのインストール
[仮想ハードディスクイメージのダウンロード](https://www.ubuntulinux.jp/download/ja-remix-vhd)から、Ubuntu 14.04 LTS[^1]のディスクイメージをダウンロードし解凍してください。

## 仮想マシンの登録と起動
VirtualBoxを起動し、[新規]を押してください。下記のように指定し、次へ行きます。
<img width="353" alt="4.png" src="https://qiita-image-store.s3.amazonaws.com/0/13955/c7e46c56-ff93-bc6c-d758-73503eab9a5c.png">

メモリーサイズは、2048MB以上を推奨します。後で変更可能です。
ハードディスクは、[すでにある…]を選択し、右のアイコンをクリックし、解凍したUbuntu 14.04 LTSのディスクイメージを指定し、[作成]ボタンを押してください。
<img width="353" alt="5.png" src="https://qiita-image-store.s3.amazonaws.com/0/13955/dac3b7ec-3000-43cc-54c0-6ea593ae11d6.png">

## Ubuntuの設定
Ubuntu14.04を選んで、[設定]を押してください。
[一般]の[高度]で下記のように設定すると便利になります。
<img width="581" alt="6.png" src="https://qiita-image-store.s3.amazonaws.com/0/13955/97cc6cb7-b314-3e57-6a5c-a3c4ccbcd23b.png">

エクステンションパックの導入をしていれば、下記のように設定することにより、リモートデスクトップで[ホストのIPアドレス:13389]にアクセスして使うことができます。
<img width="581" alt="7.png" src="https://qiita-image-store.s3.amazonaws.com/0/13955/cf5852bd-2461-7b9a-cad5-da937ff6f6ee.png">

[ネットワーク]の[アダプター2]を選んで下記のように設定してください。
[アダプター1]の設定はそのままにしてください。
<img width="581" alt="8.png" src="https://qiita-image-store.s3.amazonaws.com/0/13955/f64b5ac5-b3fe-82bc-b897-506349080b6f.png">

設定の意味については[ネットワーク設定](http://vboxmania.net/content/%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E8%A8%AD%E5%AE%9A)を参照してください。

## Ubuntuの起動とDockerのインストール
[起動]を押してUbuntuを起動し、ログインしてください。

### aptの更新
下記のように実行します。(以降1行ずつコピペ推奨)

```:ubuntu
sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
sudo gedit /etc/apt/sources.list.d/docker.list
```
エディタが開くので、下記の内容にして保存終了ください。
「deb https://apt.dockerproject.org/repo ubuntu-trusty main」

### linux-image-extraの更新
下記のように実行します。

```:ubuntu
sudo apt-get update
sudo apt-get install linux-image-extra-$(uname -r)
```

### Dockerのインストール
下記のように実行します。

```:ubuntu
sudo apt-get update
sudo apt-get install docker-engine
sudo service docker start
```
「docker --version」でバージョンを確認できます。
詳細は、[Installation on Ubuntu](http://docs.docker.com/engine/installation/ubuntulinux/)を参考にしてください。

### 非rootユーザでdockerコマンドを使うには
下記を実行し、ログインし直してください。

```:ubuntu
sudo gpasswd -a $USER docker
```

## Jupyterの起動
Dockerでサーバを起動し、ブラウザで確認します。

### IPアドレスの確認
下記を実行し、[inet]の後ろのIPアドレスを覚えてください。このアドレスは、Windowsでブラウザを開くときに使います。

```:ubuntu
ip addr show eth1
```

### Jupyterのサーバの起動
下記を実行するだけです。

```:ubuntu
mkdir jupyter
docker run -d -p 8888:8888 -v $(pwd)/jupyter:/jupyter tsutomu7/jupyter
```

### Jupyterのクライアントの確認
Windowsのブラウザで上で確認した「http://確認したIPアドレス:8888」を開いてみてください。
Python3.5のJupyterが起動します。

Ubuntuのブラウザで見る場合は、「http://172.17.0.2:8888 」を見てください。

### Jupyterのサーバの終了
サーバの終了は、下記のように行います。

```:ubuntu
docker stop $(docker ps -aq)
```

### Jupyterのサーバの再起動
サーバの再起動は、下記のように行います。

```:ubuntu
docker start $(docker ps -aq)
```

[^1]: 2015/10/23では、Ubuntu 15.10が最新ですが、長期保証版(LTS)の最新は、14.04です。

