title: BlenderでアニメーションをWebpで保存する
tags: Python 3DCG Blender WebP
url: https://qiita.com/SaitoTsutomu/items/499c7307bdcdfb2f1662
created_at: 2022-04-25 20:27:25+09:00
updated_at: 2022-04-25 20:32:19+09:00
body:

## 概要

Blender3.1で、アニメーションを[Webp](https://ja.wikipedia.org/wiki/WebP)で保存するアドオンをPythonで作成したので紹介します。

## やり方

### アドオンのインストール

- [Blender Add-on: MakeWebp](https://github.com/SaitoTsutomu/MakeWebp)の画面にしたがってインストールしてください。
    - アドオンのチェックでは「テスト中」を選んでください。

### Pillowのインストール

本アドオンは、Pillowを利用しています。
そのため、下記のように、コマンドラインでBlenderにPillowをインストールする必要があります。コマンドラインからBlenderを操作する方法については、「[Blenderのコマンドサンプル](https://qiita.com/SaitoTsutomu/items/6b70367455f843a979b1)」も参考にしてください。

- macOSの場合
```
/Applications/Blender.app/Contents/Resources/3.1/python/bin/python3.10 -m pip install Pillow
```

- Windowsの場合
```
"C:\Program Files\Blender Foundation\Blender 3.1\3.1\python\bin\python" -m pip install Pillow
```

### 作成

- オブジェクトメニューの`Make Webp`を選んでください。
- 出力フォルダに`webp.webp`という名前で出力されます。

### Pythonのコード

https://github.com/SaitoTsutomu/MakeWebp/blob/main/__init__.py

下記のように、複数の画像ファイルをimgsに入れておけば、PillowではWebpファイルを簡単に作成できます。

```py
imgs[0].save(
    Path(pre_filepath) / "webp.webp",
    save_all=True,
    append_images=imgs[1:],
)
```

以上

