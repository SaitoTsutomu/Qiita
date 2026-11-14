title: Docker公式OS一覧
tags: Docker
url: https://qiita.com/SaitoTsutomu/items/f40c63859695da4183d7
created_at: 2016-01-03 05:47:50+09:00
updated_at: 2016-04-18 15:21:24+09:00
body:

[Docker公式](https://github.com/docker-library/official-images/tree/master/library)OSを目視で検索したメモ。ROSとかneurodebianみたいな特殊なものは除きました。Verは2016/4/15時点でlatestのものです。

OS|Ver|Download Size|Image Size|Memo
:--|:--|--:|--:|:--
[scratch](https://hub.docker.com/_/scratch/)||0 MB|0 MB|GO exeで便利
[busybox](https://busybox.net/)|1.24|676 KB|1.113 MB|最小の実行ファイルとなるよう設計されたプログラム群
[alpine](http://www.alpinelinux.org/)|3.3|2 MB|4.798 MB|busyboxがベース
[cirros](https://launchpad.net/cirros/)|0.3.4|4 MB|7.735 MB|パッケージマネージャーなし
[ubuntu-debootstrap](https://hub.docker.com/r/library/ubuntu-debootstrap/)|14.04|35 MB|87.09  MB|Deprecated(alpineへ代替)
[opensuse](https://ja.opensuse.org/)|13.2|38 MB|97.7  MB
[photon](https://vmware.github.io/photon/)|1.0RC|43 MB|119.1 MB|VMware製
[debian](https://www.debian.org/)|8.4|51 MB|125.1 MB
[ubuntu](http://www.ubuntulinux.jp/)|14.04|66 MB|188 MB
[mageia](http://www.mageia.org/ja/)|5|72 MB|193.1 MB
[centos](https://www.centos.org/)|7|71 MB|196.7   MB
[oraclelinux](http://www.oracle.com/jp/technologies/linux/)|7.2|74 MB|205.9 MB
[fedora](https://getfedora.org/ja/)|23|74 MB|204.7 MB
[ubuntu-upstart](https://hub.docker.com/_/ubuntu-upstart/)|14.04|102 MB|253.3 MB|デーモン用の起動が早い版
[crux](https://crux.nu/)|3.1|122 MB|341.7 MB
[sourcemage](http://www.sourcemage.org/)|0.61|233 MB|644.7 MB|sourceベース

- alpineが小さくてよいですね。(ubuntu-debootstrapはdeprecatedになりました。)
- 下記参考リンクのubuntu-essentialで、科学技術計算用Python3.5環境([tsutomu7/scientific-python](https://hub.docker.com/r/tsutomu7/scientific-python/))作ってみました。
    - Anaconda 4.0を利用したMKL版("tsutomu7/scientific-python:mkl")も用意しました。
- alpineベースでも、[frolvlad/alpine-glibc](https://hub.docker.com/r/frolvlad/alpine-glibc/)を使えば、Anacondaが使えます。同じように科学技術計算用Python3.5環境[tsutomu7/alpine-python](https://hub.docker.com/r/tsutomu7/alpine-python/)(659MB)を作ってみました。



参考

- [Alpine Linux で Docker イメージを劇的に小さくする](http://qiita.com/asakaguchi/items/484ba262965ef3823f61)
- [Alpine Linux で軽量な Docker イメージを作る](http://qiita.com/pottava/items/970d7b5cda565b995fe7)
- [効率的に安全な Dockerfile を作るには](http://qiita.com/pottava/items/452bf80e334bc1fee69a)
- [お前のDockerイメージはまだ重い💢💢💢](https://speakerdeck.com/stormcat24/oqian-falsedockerimezihamadazhong-i)
- [ubuntu-essential 最小構成の Ubuntu Docker Image](http://qiita.com/A-I/items/af0f654eeac2cc464d1e)
- [超軽量 Docker Image true (125 bytes) と sleeping-beauty (129 bytes)](http://qiita.com/kitsuyui/items/ba6eb17e6bbe97aa6b04)
- [official-images一覧](https://github.com/docker-library/official-images/tree/master/library)

以上

