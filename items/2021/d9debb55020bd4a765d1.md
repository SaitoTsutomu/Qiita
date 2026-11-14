title: BlenderでISBNから書影の自動作成
tags: Python Blender
url: https://qiita.com/SaitoTsutomu/items/d9debb55020bd4a765d1
created_at: 2021-10-20 17:48:55+09:00
updated_at: 2022-05-08 17:54:37+09:00
body:

# 目的

3DCGソフトウェアの[Blender](https://www.blender.org/)では、Pythonを使っていろいろな処理を自動化できます。
ここでは、ISBNから書籍の書影画像を作成する方法を紹介します。

※ macOSのBlender2.93で確認しています。適宜直せばWindowsでも動くはずです。
※ 書影の元画像は、[openBD](https://openbd.jp/)から取得します。openBDに登録してある書籍が対象になります。

# 書影の元になるBlenderファイルの作成手順

- 「[Blenderのコマンドサンプル](https://qiita.com/SaitoTsutomu/items/6b70367455f843a979b1)」を参考に、下記のようにBlenderのPythonに`requests`と`openbd`をインストールしてください。

```
blender_pip install -U requests openbd
```

- 適当なJPEG画像を`/tmp/book.jpg`としてコピーします（この画像は後で上書きされます）。
- Blenderを起動します。
- 起動後に立方体がなければ、`Shift + A`の`メッシュ - 立方体`で作成します。
- 立方体の名前を`book`に変えます。
- `N`でサイドバーを出します。`book`を選択しアイテムタブの寸法のX、Y、Zを`0.21, 0.025, 0.297`にします（A4判のサイズ）。
- `book`のマテリアルを2つ作成し、2つ目のベースカラーを画像テクスチャにし、`/tmp/book.jpg`を指定します。
- 編集モードで正面の面を選択し、2つ目のマテリアルに割り当て、オブジェクトモードに戻ります。
- UV Editingウィンドウにし、右側で`A`を押し、左側で`AS4 + Enter`と`R-90 + Enter`を押した後、`G`で下図のように左の四角が重なるようにします。

![uv.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/072378a6-c70c-0c80-b3d3-9ad87d9027f1.jpeg)

- Scriptウィンドウにし、新規作成し、名前を`book_image.py`にし、下記をコピペします。

```py:book_image.py
import sys

import bpy
import fire
import requests
from openbd import book_info


def book_image(isbn):
    bi = book_info(str(isbn))
    res = requests.get(bi.image)
    with open("/tmp/book.jpg", "wb") as fp:
        fp.write(res.content)
    bpy.data.images["book.jpg"].reload()
    bpy.context.scene.render.filepath = "book"
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile()


if __name__ == "__main__":
    sys.argv = sys.argv[:1] + sys.argv[(sys.argv + ["--"]).index("--") + 1 :]
    fire.Fire(book_image)
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

- テキストメニューの`登録`をチェックします。登録すると起動時に実行できるようになります。
- Layoutウィンドウにし、カメラとライトなどを調整し、レンダリングしたときに好みの書影になるようにします。
- `book_image.blend`という名前で、Blenderを保存し終了します。

# 実行

書影にしたい13桁または10桁のISBNを調べてください（下記では例として 9784764905801 を使っています）。

調べたISBNを使って、下記のように実行します。

```
blender -b -y book_image.blend -- 9784764905801
```

- `-b`は、バックグラウンド実行の指定です。
- `-y`は、自動実行時に確認を省略させる指定です。
- `--`以降が、book_image.pyの関数`book_image`の引数になります。

（適宜モデリングすると）以下のような`book.png`が作成されます。

![book.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/1fdd26e2-31b2-41d0-8d22-61386f07704e.png)


以上

