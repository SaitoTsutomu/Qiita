title: 自分のDockerイメージをさらしてみる
tags: Python Go Docker 最適化 組合せ最適化
url: https://qiita.com/SaitoTsutomu/items/37a0f795185e58df099e
created_at: 2015-12-05 00:58:51+09:00
updated_at: 2017-09-06 11:11:14+09:00
body:

Docker歴1ヶ月くらいですが、[Docker Hub](https://hub.docker.com/)の自作のイメージを紹介します。Dockerのインストールについては、[DockerでJupyterを起動するまで](http://qiita.com/SaitoTsutomu/items/29414e2d4f30b2bc94ae)をどうぞ。

全てKitematicで簡単に実行できます。

* [tsutomu7/standard](https://hub.docker.com/r/tsutomu7/standard/)：[組合せ最適化 - 典型問題と実行方法](http://qiita.com/SaitoTsutomu/items/0f6c1a4415d196e64314)を実行できるようにしたものです。
* [tsutomu7/puzzle](https://hub.docker.com/r/tsutomu7/puzzle/)：[数理最適化によるパズルの解法](https://github.com/SaitoTsutomu/OptForPuzzle)を実行できるようにしたものです。
* [tsutomu7/gotour](https://hub.docker.com/r/tsutomu7/gotour/)：[Gotour](https://go-tour-jp.appspot.com/)をLocalで実行できるようにしたものです。
* [tsutomu7/alpine-python3](https://hub.docker.com/r/tsutomu7/alpine-python3/)：5MBの軽量OSである[alpine](http://www.alpinelinux.org/)([dockerイメージ](https://hub.docker.com/_/alpine/))にPython3.4やnumpy,scipy,jupyter,matplotlib,pandas等インストールしたものです。python3.4だけなら[frolvlad/alpine-python3](https://hub.docker.com/r/frolvlad/alpine-python3/)でOK。

ついでにDockerfileも説明します。

init.shを使っているのは、Windowsで、*.ipynbファイルを編集できるようにするためと、直接CMDだと失敗したからです。

```docker:standard/Dockerfile
FROM tsutomu7/py3sci

RUN pip install ortoolpy
EXPOSE 8888
VOLUME ["/jupyter"]
WORKDIR /jupyter
COPY *.ipynb /root/tmp/
COPY data/ /root/tmp/data/
COPY init.sh /root/
CMD ["sh", "/root/init.sh"]
```

```bash:standard/init.sh
mv /root/tmp/* /jupyter
jupyter notebook --ip=* --no-browser
```

```docker:puzzle/Dockerfile
FROM debian:jessie

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
ENV PATH /opt/conda/bin:$PATH
ENV LANG C.UTF-8
ENV MINICONDA Miniconda3-3.18.3-Linux-x86_64.sh
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/$MINICONDA && \
    bash /$MINICONDA -b -p /opt/conda && \
    rm $MINICONDA && \
    conda install -y conda==3.18.3 && \
    conda update -y conda && \
    conda install -y jupyter && \
    pip install pulp unionfind && \
    rm -rf /opt/conda/pkgs/*
EXPOSE 8888
VOLUME ["/jupyter"]
WORKDIR /jupyter
COPY data /root/tmp/data/
COPY pic /root/tmp/pic/
COPY *.ipynb /root/tmp/
COPY init.sh /root/
CMD ["sh", "/root/init.sh"]
```

```bash:puzzle/init.sh
mv /root/tmp/* /jupyter
jupyter notebook --ip=* --no-browser
```

```docker:gotour/Dockerfile
FROM alpine

ENV GOPATH=/root/go
RUN apk add --update go git && \
    mkdir /root/go && \
    go get golang.org/x/tour/gotour && \
    apk del git && \
    rm /var/cache/apk/* 
EXPOSE 8080
CMD ["/root/go/bin/gotour", "-http", "0.0.0.0:8080"]
```

```docker:alpine-python3/Dockerfile
FROM alpine

ENV BLAS /usr/local/lib/libfblas.a
ENV LAPACK /usr/local/lib/liblapack.a
RUN apk add --update musl python3-dev freetype-dev make g++ gfortran wget && \
    cd /tmp && wget -q --no-check-certificate \
        https://raw.githubusercontent.com/catholabs/docker-alpine/master/blas.sh \
        https://raw.githubusercontent.com/catholabs/docker-alpine/master/blas.tgz \
        https://raw.githubusercontent.com/catholabs/docker-alpine/master/lapack.sh \
        https://raw.githubusercontent.com/catholabs/docker-alpine/master/lapack.tgz \
        https://raw.githubusercontent.com/catholabs/docker-alpine/master/make.inc \
        http://dl.ipafont.ipa.go.jp/IPAexfont/ipaexg00301.zip && \
    sh ./blas.sh && sh ./lapack.sh && \
    cp ~/src/BLAS/libfblas.a /usr/local/lib && \
    cp ~/src/lapack-3.5.0/liblapack.a /usr/local/lib && \
    pip3 install -U pip && \
    pip install numpy==1.9.3 && \
    pip install scipy matplotlib jupyter networkx pandas \
        scikit-learn blist bokeh statsmodels seaborn dask sympy && \
    unzip -q ipaexg00301.zip && \
    mv ipaexg00301/ipaexg.ttf /usr/lib/python3.4/site-packages/matplotlib/mpl-data/fonts/ttf/ && \
    rm -rf /var/cache/apk/* /tmp/* /root/src/
CMD ["sh"]
```

