title: alpineベースでpythonをdocker build
tags: Python Docker alpine
url: https://qiita.com/SaitoTsutomu/items/000b58796327b19172a9
created_at: 2016-03-02 13:42:01+09:00
updated_at: 2016-03-02 13:42:01+09:00
body:

# はじめに
python3.5を想定しています。

# alpineでpythonを使いたい
[公式にあります](https://hub.docker.com/r/library/python/tags/)。
下記のようにすればOK。(90MB)

    docker run -it python:3.5-alpine

# alpineでpythonのnumpyを使いたい
- 2.7なら[testingにあります](https://pkgs.alpinelinux.org/packages?name=py-numpy&repo=testing&arch=all&maintainer=all)。
- 3.5でも、[こちら](https://github.com/catholabs/docker-alpine)をベースに頑張るの手もあります。
- もっといい方法があります。alpineでglibcを使えるようにした[frolvlad/alpine-glibc](https://hub.docker.com/r/frolvlad/alpine-glibc/)を使うと、minicondaが使えます。

下記のDockerfileでイメージを作ると、136MBですが、"conda install numpy scipy"でnumpyもscipyも簡単にインストールできます。

```:Dockerfile
FROM frolvlad/alpine-glibc

ENV PATH=/opt/conda/bin:$PATH \
    LANG=C.UTF-8 \
    MINICONDA=Miniconda3-latest-Linux-x86_64.sh
RUN apk add --no-cache bash wget && \
    wget -q --no-check-certificate https://repo.continuum.io/miniconda/$MINICONDA && \
    bash /Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && \
    ln -s /opt/conda/bin/* /usr/local/bin/ && \
    rm -rf /root/.[acpw]* /$MINICONDA /opt/conda/pkgs/*
CMD ["bash"]
```

科学技術計算用に[tsutomu7/alpine-python](https://hub.docker.com/r/tsutomu7/alpine-python/)をつくりました。(782MB)

Kitematicでしたら、"tsutomu7/alpine-python:jupyter" ならクリックで使えて便利です。

以上

