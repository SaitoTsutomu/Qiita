title: DigitalOceanの便利ツール作りました
tags: Python Docker DigitalOcean
url: https://qiita.com/SaitoTsutomu/items/2444668c9dedde0d77ae
created_at: 2016-01-04 10:02:50+09:00
updated_at: 2016-05-06 00:34:33+09:00
body:

# <i class='fa fa-cloud' /> はじめに
DigitalOceanの管理ツール([dioc](https://pypi.python.org/pypi/dioc))を作成したので、ご紹介します。(利用については自己責任でお願いします。)
操作は、Ubuntu上で、DockerとPython3.5を用います。Windowsの方は、[Ubuntuを入れてDockerを使う方法](http://qiita.com/Tsutomu-KKE@github/items/29414e2d4f30b2bc94ae#ubuntu%E3%82%92%E5%85%A5%E3%82%8C%E3%81%A6docker%E3%82%92%E4%BD%BF%E3%81%86%E6%96%B9%E6%B3%95)を参考に、VirtualBox、Ubuntu14、Docker[^3]をインストールしてください。
Dockerが使えれば、Dockerイメージ[dioc-python-3.5](https://hub.docker.com/r/tsutomu7/dioc-python-3.5/)を用いてすぐに始められます。

[^3]: Linuxでは、"wget -qO- https://get.docker.com/ | sh"

![1.png](https://qiita-image-store.s3.amazonaws.com/0/13955/58361187-e834-5e7f-3062-577ccc39fd34.png)


# <i class='fa fa-cloud' /> 用語
- [DigitalOcean](https://www.digitalocean.com/?refcode=b5ecd9b2be25)： [AWS](https://aws.amazon.com/jp/)の[EC2](https://aws.amazon.com/jp/ec2/)のようなクラウドサービス。
- Droplet： 仮想OSのインスタンス。
- Snapshot： Dropletの状態を保存したもの。Snapshotを元にDropletを作成できます。
- Image： Dropletの元になるもの。公式のものと、Snapshotで作成した私的なものから選べます。公式なものは、OSだけのものや、アプリ[^1]込み(下図)のものがあります。
- 課金： 1月当たり5\$, 10\$, 20\$, 40\$, 80\$, 160\$, 320\$, 480\$, 640\$のプランがあり、メモリは価格に比例しています。Dropletを作成すると、停止(PowerOff)しても破棄(Destroy)するまで、課金されます。不要な課金を避けるためには、Droplet停止、DropletからSnapshot作成、Droplet破棄を行えばよいです。現在、Snapshotを作成しても無料ですが、将来は課金されるようです。また、データ転送量がリミットを超えても課金が発生します。

<img width="501" alt="2.png" src="https://qiita-image-store.s3.amazonaws.com/0/13955/8620988b-35f1-c583-4479-9d047b0768e3.png">

[^1]: DigitalOceanで用意されているアプリ

  - [Cassandra](http://cassandra.apache.org/): NoSQLデータベース
  - [Discourse](https://www.discourse.org/): フォーラム管理
  - [Django](https://www.djangoproject.com/): Webフレームワーク
  - [Docker](https://www.docker.com/): コンテナ管理
  - [Dokku](http://dokku.viewdocs.io/dokku/): Heroku(無料クラウドサーバー)クローン
  - [Drone](https://drone.io/): 継続的インテグレーション
  - [Drupal](https://www.drupal.org/): コンテンツマネジメントシステム
  - [Elixir](http://elixir-lang.org/): プログラミング言語
  - [ELK](https://www.elastic.co/jp/): Elasticsearch, Logstash, Kibana
  - [Ghost](https://ghost.org/): ブログシステム
  - [GitLab](https://about.gitlab.com/): プライベートGitHub
  - [Joomla](https://www.joomla.org/): コンテンツマネジメントシステム
  - [LAMP](https://en.wikipedia.org/wiki/LAMP_(software_bundle)): Linux, Apache, MySQL, PHP
  - [LEMP](https://lemp.io/): Linux, Nginx, MySQL, PHP
  - [Magento](https://magento.com/): ECプラットフォーム
  - [MEAN](http://mean.io): MongoDB, Express, AngularJS, Node
  - [MediaWiki](https://www.mediawiki.org/): プライベートWikipedia
  - [MongoDB](https://www.mongodb.org/): NoSQLデータベース
  - [Mumble](www.mumble.info): ボイスチャット
  - [node](https://nodejs.org/): プログラミング言語
  - [ownCloud](https://owncloud.org/): ファイル共有
  - [PHPMyAdmin](https://www.phpmyadmin.net/): MySQL管理ツール
  - [Redis](http://redis.io/): インメモリデータストア
  - [Redmine](http://www.redmine.org/): プロジェクト管理
  - [Ruby on Rails](http://rubyonrails.org/): Webフレームワーク
  - [WordPress](https://wordpress.org/): ブログシステム

# <i class='fa fa-cloud' /> なぜDigitalOceanか？
- 安い。支払いの上限あり。1ヶ月5$から。
- 早い。1分以内の起動。全てSSD。
- 簡単。シンプルな管理画面。
- [利用者が多い](http://trends.netcraft.com/www.digitalocean.com)。
- 今なら10$の特典つき！？

## DigitalOceanのデメリット
- 東京リージョンがありません。シンガポールを選びましょう。
- AWSに比べて下記の機能がないため、大規模な場合は一手間かかります。
  - Reserved Instance
  - Marketplace
  - AvailabilityZone
  - SecurityGroup
  - ElasticIP
  - ELB
  - VPC

参考：
[AWSのインスタンス高過ぎワロタ。探せば安くて美味いところはあります。](http://qiita.com/kaiinui/items/da47c9850dc09b3cf091)
[使う前に知りたかったDigitalOceanまとめ](http://pocketstudio.jp/log3/2015/04/13/digitalocean_introduction/)

## DigitalOceanでDockerを使うメリット
- アプリケーションを配布するのに比べて、より確実に稼働させることができます。
- 課金のかからないローカルで実行環境を作成できます。
- CoreOSを使えば、デプロイも簡単です。
- 軽快に動作します。

参考：[Docker公式OS一覧](http://qiita.com/Tsutomu-KKE@github/items/f40c63859695da4183d7)

# <i class='fa fa-cloud' /> DigitalOceanのアカウント作成
ここからは、クレジットカードまたはPayPalが必要になり、課金が発生しますのでご注意ください。

1. [DigitalOcean](https://www.digitalocean.com/?refcode=b5ecd9b2be25)[^2]を開いて、e-mailとパスワードを入力し、[Create Account]を押します。
- メールが送られてくるので、リンク先をクリックし、クレジットカードなどの方法を入力します。

[^2]: このURLから登録すると私にポイントが入ります。

# <i class='fa fa-cloud' /> DigitalOceanを使ってみよう
通常、Dropletのログインパスワードはメールで送られてきます。(数分待って)メールでパスワード確認してからログインするのは、手間がかかるので、SSH Keyを用いる方法を説明します。

## SSH Keyの設定
- Ubuntuで下記を実行します。パスフレーズは、ログインで必要になりますので覚えてください。
  - ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
  - ssh-add
- 下記を実行し、表示される内容をコピーしてください。
  - cat ~/.ssh/id_rsa.pub
- DigitalOceanにログインし、右上の<i class='fa fa-cog'/>から[Settings](https://cloud.digitalocean.com/settings)を選んでください。
- 左の[[Security]](https://cloud.digitalocean.com/settings/security)を選び、[Add SSH Key]を押してください。
- [Name]を[id_rsa]にし、[Public SSH Key]にコピーした内容を貼り付けて、[Create SSH Key]を押してください。

## 最初のDropletを作成してみる
- [[Create Droplet]](https://cloud.digitalocean.com/droplets/new)を押します。
- [Choose an image]は[CoreOS]に変えましょう。
- [Choose a size]は一番安い"$5/mo"に変えましょう。
- [Choose a datacenter region]は、日本に近い"Singapore"に変えましょう。
- [Add your SSH keys]は"id_rsa"をチェックしてください。
- [Create]ボタンを押してください。課金が始まります。
- 数十秒ほどで起動します。
- [IP Address]をコピーしてください。
- Ubuntuで下記を実行してください。初回はパスフレーズを聞かれます。
  - ssh core@[コピーしたIP Address]
- 下記を実行するとスペックがわかります。
  - cat /proc/cpuinfo
- ログアウトしてください。
- [Droplet](https://cloud.digitalocean.com/droplets)画面で作成したDropletをDestroyしてください。
- Destroyしないと、ずっと課金されますので注意してください。

## APIトークンの発行
プログラムからDigitalOceanを操作するには、APIトークンが必要になります。下記の方法でトークンを取得してください。トークンがあれば、自由にDigitalOceanを利用できます。トークンは大事に管理してください。
参考：[初心者がAWSでミスって不正利用されて$6,000請求、泣きそうになったお話。](http://qiita.com/mochizukikotaro/items/a0e98ff0063a77e7b694)

- DigitalOceanにログインし、上部の[API](https://cloud.digitalocean.com/settings/applications)を選んでください。
- [[Generate new token]](https://cloud.digitalocean.com/settings/tokens/new)を押してください。
- [Token Name]に"apitok"を入れてください。[Write]はチェックしたままにしてください。
- [Generate Token]を押してください。
- 画面に表示されたトークンを適宜メモしてください。この画面を閉じると同じトークンは、2度と表示されません。
- トークンを忘れてしまったら、削除して再作成してください。

# <i class='fa fa-cloud' /> Diocの紹介

## 環境構築
- cryptographyをインストールしてください。Anacondaであれば、下記のようにしてください。
    - "conda install -y cryptography"
- ローカルで実行したい場合
    - Python3.5を使える状態で"pip install dioc"としてください。その後で、下記のように".bashrc"に追記してください(一度だけでOK)。
- Dockerコンテナ内で実行したい場合
    - ローカルで下記のように".bashrc"に追記してください(一度だけでOK)。その後で、"docker run -it -v ~:/root tsutomu7/dioc-python-3.5
"としてください。

```bash:ubuntu
cat << eof >> .bashrc
export DIOC_TOKEN=「DigitalOceanのAPIトークン」
export DIOC_DEFAULT_SSHKEY=id_rsa
export DIOC_DEFAULT_SIZE=512mb
export DIOC_DEFAULT_REGION=sgp1
if [ -x /usr/local/bin/dio -o -x /opt/conda/bin/dio ]; then
  eval "$(_DIO_COMPLETE=source dio)"
fi
eof
source ~/.bashrc
```

## Bashで使う場合
Bashの操作では、コマンドは"dio"です。bash-completionが使えるようになっています。
"イメージ名"は、例えば、「'899.17.0 (stable)'」としてください。
"dio list image"でイメージの一覧が表示されます。

```bash:ubuntu
# Dropletの作成
dio create "Droplet名" "イメージ名"

# SnapshotからDropletの作成
dio create "Droplet名" "Snapshot名"

# SSHでコマンド実行
dio ssh "Droplet名" "コマンド"

# ファイルコピー
dio scp "Droplet名:ファイルバス" "Droplet名:ファイルバス"

# IPアドレス確認
dio ip "Droplet名"

# Droplet一覧確認
dio list

# その他の一覧確認(対象は、droplet, image, private, ssh, size, regionが選べます)
dio list "対象"

# Dropletの削除
dio destroy "Droplet名"
```

##　Mongodbサーバーの起動例

```bash:ubuntu
dio create test
dio ssh test
mkdir mongo
docker run -d -p 27017:27017 -v ~/mongo:/data/db --name mongo mongo
# docker exec -it mongo mongo
exit
dio destroy test
```

## Webサーバーの起動例
DigitalOceanなら簡単にサーバーの起動もできます。
下記では、GoTourのサーバーを起動しています。

```bash:ubuntu
dio create test '' user_data='"#!/bin/bash\ndocker run -p 80:8080 tsutomu7/gotour"'
firefox `dio ip test`
# do something
dio destroy test
```

## Python3.5から使う場合
基本的に[python-digitalocean](https://pypi.python.org/pypi/python-digitalocean)のラッパーなので、メソッドはそちらを参照してください。DropletメソッドでDropletの起動もします。SSHクライアントは自動的に6回までリトライします。

```py3:python
from dioc import *
# Dropletの作成
d = Droplet('dgoc') # dgocという名前のCoreOSのDropletを作成

# SnapshotからDropletの作成
d = Droplet('dgoc', 'test') # testというsnapshotから名前dgocのDropletを作成

# IPアドレスの確認
print(d.ip_address)

# SSHクライアントの作成
c = ssh_client(d)

# SSHでコマンド実行
c.exec_command(コマンド)

# Dropletの削除
d.destroy()
```
以上

----

