title: DigitalOceanの公式コマンドラインツール(doctl)の紹介
tags: Ubuntu DigitalOcean doctl
url: https://qiita.com/SaitoTsutomu/items/0ce07e8b7b59c3346fa0
created_at: 2016-05-07 05:36:19+09:00
updated_at: 2016-05-07 05:36:19+09:00
body:


# <i class='fa fa-mixcloud' /> はじめに
[DigitalOcean](https://www.digitalocean.com/?refcode=b5ecd9b2be25)というのは、[AWS](https://aws.amazon.com/jp/)の[EC2](https://aws.amazon.com/jp/ec2/)のようなクラウドサービスです。下記のような特徴があります。

- 安い。支払いの上限あり。1ヶ月5$から。
- 早い。1分以内の起動。全てSSD。
- 簡単。シンプルな管理画面。
- [利用者が多い](http://trends.netcraft.com/www.digitalocean.com)。

ここでは、[新しく使えるようになった、公式コマンドラインツール(doctl)](https://www.digitalocean.com/community/tutorials/how-to-use-doctl-the-official-digitalocean-command-line-client)を紹介をします。
![1.png](https://qiita-image-store.s3.amazonaws.com/0/13955/58361187-e834-5e7f-3062-577ccc39fd34.png)

## DigitalOceanで使われる言葉について

- Droplet： 仮想OSのインスタンス。
- Snapshot： Dropletの状態を保存したもの。Snapshotを元にDropletを作成できます。
- Image(イメージ)： Dropletの元になるもの。公式のものと、Snapshotで作成した私的なものから選べます。公式なものは、OSだけのものや、アプリ込みのものがあります。

## 課金についての注意点
- 1月当たり5\$, 10\$, 20\$, 40\$, 80\$, 160\$, 320\$, 480\$, 640\$のプランがあり、メモリは価格に比例しています。
- Dropletを作成すると、停止(PowerOff)しても破棄(Destroy)するまで、課金されます。不要な課金を避けるためには、Droplet停止、DropletからSnapshot作成、Droplet破棄を行えばよいです。
    - 現在、Snapshotを作成しても無料ですが、将来は課金されるようです。
- データ転送量がリミットを超えても課金が発生します。

# <i class='fa fa-mixcloud' /> DigitalOceanをdoctlから使ってみよう

## DigitalOceanのアカウント作成
1. [DigitalOcean](https://www.digitalocean.com/?refcode=b5ecd9b2be25)[^2]を開いて、e-mailとパスワードを入力し、[Create Account]を押します。
- メールが送られてくるので、リンク先をクリックし、クレジットカードなどの方法を入力します。

[^2]: このURLから登録すると私にポイントが入ります。

以降は、Ubuntu 16.04 上での実行方法の説明になります。

## doctlのインストール

```bash:bash
wget https://github.com/digitalocean/doctl/releases/download/v1.0.0/doctl-1.0.0-linux-amd64.tar.gz
tar xf doctl-1.0.0-linux-amd64.tar.gz
sudo mv ./doctl /usr/local/bin
rm doctl-1.0.0-linux-amd64.tar.gz
```

## DigitalOceanへの認証
下記のコマンドを実行すると、ブラウザが開きますので、ログインして、[Authorize]ボタンを押してください。"updated access token"と出力されれば成功です。

```bash:bash
doctl auth login
```

## doctlコマンドの概要
まずは、"doctl"を実行してみましょう。ヘルプが表示されます。
">>>"以降が出力を表しています。

```bash:bash
doctl
>>>
doctl is a command line interface for the DigitalOcean API.

Usage:
  doctl [command]

Available Commands:
  account     account commands
  auth        auth commands
  compute     compute commands
  version     show the current version

Flags:
  -t, --access-token string   DigitalOcean API V2 Access Token
  -h, --help                  help for doctl
  -o, --output string         output formt [text|json] (default "text")
      --trace                 verbose output
  -v, --verbose               verbose output

Use "doctl [command] --help" for more information about a command.
```

account、auth、compute、versionの4つのコマンドがあります。

## Accountの確認
下記のようにしてAccountの確認ができます。

```bash:bash
doctl account get
>>>
Email       Droplet Limit Email Verified UUID Status
xxx@xxx.xxx 10            true           XXXX active
```

また以下のようにすれば、Accountの制限が確認ができます。これを見ると、1時間に5000回まで実行できるようです。

```bash:bash
doctl account ratelimit
>>>
Limit	Remaining	Reset
5000	4978		2016-05-07 10:10:10 +0900 JST
```

## DigitalOceanのリソースの情報
この後では、computeを用います。順番にいろいろ見ていきましょう。

### computeコマンドのヘルプ
```bash:bash
doctl compute
>>>
表示は省略
```


### 過去の履歴(action)一覧
```bash:bash
doctl compute action list
>>>
ID  Status    Type    Started At Completed At Resource ID Resource Type Region
123 completed destroy 2015-XX-XX 2015-XX-XX   XXX         droplet       sgp1
...以下省略
```

### actionの情報
\<action_id>は上記のIDです。

```bash:bash
doctl compute action get <action_id>
>>>
上記に同じ
```


### リージョンの一覧
```bash:bash
doctl compute region list
>>>
Slug	Name		Available
nyc1	New York 1	true
sfo1	San Francisco 1	true
nyc2	New York 2	true
ams2	Amsterdam 2	true
sgp1	Singapore 1	true
lon1	London 1	true
nyc3	New York 3	true
ams3	Amsterdam 3	true
fra1	Frankfurt 1	true
tor1	Toronto 1	true
```

### イメージの一覧
```bash:bash
doctl compute image list
>>>
ID       Name	         Type     Distribution Slug        Public Min Disk
17168961 1010.3.0 (beta) snapshot CoreOS       coreos-beta true   20
以下省略
```

### サイズの一覧
```bash:bash
doctl compute size list
>>>
Slug	Memory	VCPUs	Disk	Price Monthly	Price Hourly
512mb	512	1	20	5.00		0.007440
1gb	1024	1	30	10.00		0.014880
2gb	2048	2	40	20.00		0.029760
4gb	4096	2	60	40.00		0.059520
8gb	8192	4	80	80.00		0.119050
16gb	16384	8	160	160.00		0.238100
32gb	32768	12	320	320.00		0.476190
48gb	49152	16	480	480.00		0.714290
64gb	65536	20	640	640.00		0.952380
```

## SSH Keyの管理

最初にSSH Keyを作成しましょう。パスフレーズは、忘れないようにしてください。

```bash:bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
# パスフレーズの入力

ssh-add
```

### SSH Keyの登録
```bash:bash
doctl compute ssh-key import id_rsa --public-key-file ~/.ssh/id_rsa.pub 
>>>
ID  Name   FingerPrint
XXX id_rsa XX:XX:XX:XX:XX:XX
```

### SSH Keyの一覧
ここで表示されるFingerPrintを後で使います。

```bash:bash
doctl compute ssh-key list
>>>
ID  Name   FingerPrint
XXX id_rsa XX:XX:XX:XX:XX:XX
```

### 指定したSSH Keyの表示
```bash:bash
doctl compute ssh-key get <FingerPrint>
>>>
ID  Name   FingerPrint
XXX id_rsa XX:XX:XX:XX:XX:XX
```

### SSH Keyの削除
\<ssh_key_id>は上記のIDです。実際には、id_rsaは、使うので消さないでください。

```bash:bash
doctl compute ssh-key delete <ssh_key_id>
```

## Dropletの操作
これ以降の作業は、課金が発生します。また、Dropletを削除しないと、課金が続くのでご注意ください。

### Dropletの作成
メモリ512MBの最小構成でシンガポールリージョンにCoreOSのDropletを作成します。\<FingerPrint>は、先ほどの"XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX"を指定してください。また、”--enable-backups”オプションでバックアップされるようになります。
このコマンドは、サーバーで実行されますので、OSの起動前に制御が戻ります。

```bash:bash
doctl compute droplet create test --size 512mb --image coreos-stable \
  --region sgp1 --ssh-keys <FingerPrint>
>>>
ID  Name Public IPv4 Memory VCPUs Disk Region Image                    Status
XXX test             512    1     20   sgp1   CoreOS 899.17.0 (stable) new
```


### Dropletの一覧
上記コマンドから1分ほどでOSが起動します。起動後に一覧を見ると、IPアドレスも表示されます。

```bash:bash
doctl compute droplet list
>>>
ID  Name Public IPv4 Memory VCPUs Disk Region Image                    Status
XXX test XX.XX.XX.XX 512    1     20   sgp1   CoreOS 899.17.0 (stable) new
```

### Dropletのactionの確認
\<droplet_id>は、上記のIDです。Nameではありません。

```bash:bash
doctl compute droplet actions <droplet_id>
>>>
ID  Status    Type   Started At Completed At Resource ID Resource Type Region
XXX completed create 2016-05-06 2016-05-06   XXX         droplet       sgp1
```

### Dropletのバックアップの確認
先ほどは、バックアップ指定をしませんでしたので、バックアップはありません。

```bash:bash
doctl compute droplet backups <droplet_id>
>>>
ID	Name	Type	Distribution	Slug	Public	Min Disk
```

### Dropletの確認
```bash:bash
doctl compute droplet get <droplet_id>
>>>
ID  Name Public IPv4 Memory VCPUs Disk Region Image                    Status
XXX test XX.XX.XX.XX 512    1     20   sgp1   CoreOS 899.17.0 (stable) active
```

### Dropletのカーネル一覧
このDropletのカーネルはないようです。

```bash:bash
doctl compute droplet kernels <droplet_id>
>>>
ID	Name	Version
```

### 同一物理ハードウェア上の別Dropletの確認
```bash:bash
doctl compute droplet neighbors <droplet_id>
>>>
ID	Name	Public IPv4	Memory	VCPUs	Disk	Region	Image	Status
```

### Dropletのsnapshotの確認
```bash:bash
doctl compute droplet snapshots <droplet_id>
>>>
ID	Name	Type	Distribution	Slug	Public	Min Disk
```

### SSHの実行
"test"は、作成したDropletの名前です。

```bash:bash
doctl compute ssh test
```

### Dropletの削除
```bash:bash
doctl compute droplet delete <droplet_id>
>>>
deleted droplet XXX
```

その他のコマンドについては、[How To Use Doctl, the Official DigitalOcean Command-Line Client](https://www.digitalocean.com/community/tutorials/how-to-use-doctl-the-official-digitalocean-command-line-client)をご覧ください。

# <i class='fa fa-mixcloud' /> 参考

- [DigitalOceanの便利ツール作りました](http://qiita.com/Tsutomu-KKE@github/items/2444668c9dedde0d77ae)

以上

