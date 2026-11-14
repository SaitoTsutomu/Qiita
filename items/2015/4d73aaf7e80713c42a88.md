title: Dockerのvolume問答
tags: Docker
url: https://qiita.com/SaitoTsutomu/items/4d73aaf7e80713c42a88
created_at: 2015-12-12 00:32:35+09:00
updated_at: 2015-12-12 13:26:05+09:00
body:

DockerのvolumeについてQ&A風にまとめてみました。

# <i class='fa fa-user' style='font-size:1em;' /> volumeって何のためにあるの？

- コンテナのデータは、コンテナが消えると一緒に消えてしまいます。
- [-v ホストのパス:コンテナのパス]オプションで、ホスト側にデータを持てますが、データの可搬性がなくなります。
- そこで、コンテナとは別にデータを管理するしくみとして、volumeがあります。

# <i class='fa fa-user' style='font-size:1em;' /> どうやってvolumeを使うの？

下記のようにすれば、自動的に[ボリューム名]のvolumeが使えます。
```
docker run -v ボリューム名:コンテナのパス イメージ名
```

# <i class='fa fa-user' style='font-size:1em;' /> data volume container って何？
volumeは、誰にも使われなくなったときに、[--rm]をつけて実行(run)すると、停止時に削除されてしまします。そこで、削除されないように、そのvolumeにヒモ付けたコンテナを作成しておきます。それがdata volume containerとよばれるものですが、普通のコンテナです。

# <i class='fa fa-user' style='font-size:1em;' /> data volume container は何でもいいの？
何でもいいです。busyboxが使われることが多いですが、練習として、最小のイメージを作ってやってみましょう。

```
mkdir zero
cat << eof > zero/Dockerfile
FROM scratch
ADD _ /
eof
touch zero/_
docker build -t zero zero
```

このzeroイメージを使って、下記のようにdata volume containerを作成できます。
data volume containerとvolumeの名前は共に、myvolとします。

```
docker create --name myvol -v myvol:/_ zero _
```

下記を実行すると、myvolというボリュームができているのが確認できます。

```
docker volume ls
```

# <i class='fa fa-user' style='font-size:1em;' /> data volume container を使うといいことあるの？

マウントの指定を使いまわすことができます。[volumeを使ってprivate docker repositoryを使ってみよう](#-volumeを使ってprivate-docker-repositoryを使ってみよう)を見てください。

# <i class='fa fa-user' style='font-size:1em;' /> 作ったvolumeを使うには？

下記のようにします。
```
docker run -v myvol:コンテナのパス 使いたいイメージ
```
例えば、こんな風に。
```
docker run -it --rm -v myvol:/myvol busybox
cd myvol
touch hello
exit
```

また、［--volumes-from コンテナ名］とすれば、そのコンテナの全てのボリュームを使うことができます。

# <i class='fa fa-user' style='font-size:1em;' /> volumeのバックアップは？

下記のようにします。
```
docker run --rm -v myvol:/myvol -v ~:/_ busybox tar cf _/myvol.tar myvol
```
カレントディレクトリに myvol.tarができます。下記のようにして中味を確認できます。
```
tar tf myvol.tar
```

# <i class='fa fa-user' style='font-size:1em;' /> バックアップを戻すには？

別のボリューム(yourvol)に戻してみましょう。最初にdata volume containerを作成しておきます。
```
docker create --name yourvol -v yourvol:/_ zero _
docker run --rm -v yourvol:/myvol -v ~:/_ busybox tar xf _/myvol.tar 
```

下記のようにして、yourvolに戻せたことを確認できます。
```
docker run --rm -v yourvol:/_ busybox ls _
```

# <i class='fa fa-user' style='font-size:1em;' /> volumeを消したいんだけど？

data volume container(を含む全ての利用しているコンテナ)を消せば、volumeを消せるようになります。
```
docker rm myvol yourvol
docker volume rm myvol yourvol
```

# <i class='fa fa-user' style='font-size:1em;' /> なるほど！
[Docker の Data Volume まわりを整理する](http://qiita.com/lciel/items/e21a4ede3bac7fb3ec5a)や[dockerのデータボリュームとそのバックアップ方法](http://qiita.com/74th/items/41393f506d223850f2c3)も参考にしてください。

# <i class='fa fa-check-square' style='font-size:1em;' /> volumeを使ってprivate docker repositoryを使ってみよう

private docker repositoryを作成して、イメージをpushしてみましょう。

## data volume container を作りましょう
data volume containerであることがわかるような名前がいいです。
```
docker create --name registryvol -v registry:/tmp/registry busybox
```

## registryサーバ－を起動しよう
公式dockerのregistryを使うとprivate docker repositoryのサーバーを簡単に実行できます。マウントの指定は、先ほどのregistryvolコンテナのものを使います。
```
docker run --volumes-from registryvol -d --name registry -p 5000:5000 registry
```

## registryサーバーへpushしてみよう
busyboxをregistryサーバーに入れてみましょう。
```
docker tag busybox localhost:5000/busybox
docker push localhost:5000/busybox
```
入ったかどうか見てみましょう。
```
docker run --rm --volumes-from registryvol busybox ls -R /tmp
```

## registryサーバーからpullしてみよう
イメージ名に[サーバー名:5000/]を付ければ同じように使えるようです。
```
docker pull localhost:5000/busybox
```


