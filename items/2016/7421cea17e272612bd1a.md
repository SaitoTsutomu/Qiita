title: Jupyterでgolang
tags: Python Go Docker Jupyter
url: https://qiita.com/SaitoTsutomu/items/7421cea17e272612bd1a
created_at: 2016-07-06 21:48:43+09:00
updated_at: 2016-10-15 23:05:44+09:00
body:

# これなに
Go言語(golang)のJupyter kernelを手っ取り早く、docker で動かしたい人へ。

[IPython kernels for other languages](https://github.com/ipython/ipython/wiki/IPython-kernels-for-other-languages)の、[Golang kernel](http://www.datadan.io/announcing-a-golang-kernel-for-jupyter-notebooks/)の[docker](https://hub.docker.com/r/dwhitena/gophernotes/tags/)を使ってみると 2.4 GBありました。
せっかくなので、自分で[docker](https://hub.docker.com/r/tsutomu7/golang/)を作ってみました。Alpine Linuxベースにして、698 MB まで小さくできました。

```bash:bash
firefox http://localhost:8888/ &
docker run -it --rm -p 8888:8888 tsutomu7/golang
```

上記のようにすると、下記のように使うことができます。

![go_sample.png](https://qiita-image-store.s3.amazonaws.com/0/13955/8e725609-7a37-85b4-2ffb-8faa8d857af4.png)

## 参考
- [Alpine Linux で Docker イメージを劇的に小さくする](http://qiita.com/asakaguchi/items/484ba262965ef3823f61)
- [Alpine Linux で軽量な Docker イメージを作る](http://qiita.com/pottava/items/970d7b5cda565b995fe7)
- [Jupyterでnimを使おう](http://qiita.com/Tsutomu-KKE@github/items/f79257430e2d8fcb9196)
- [Jupyterのkernelを作ってみる](http://qiita.com/Tsutomu-KKE@github/items/3c996bde01ef2637aadc)

以上

