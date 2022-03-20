title: BlenderでカメラからISBNを読みとり書影画像を作成する
tags: Python 3DCG Blender ISBN
url: https://qiita.com/SaitoTsutomu/items/7a5cfeb2b4abde80e159
created_at: 2022-03-01 20:52:05+09:00
updated_at: 2022-03-04 14:05:49+09:00
body:

## カメラからISBNを読みとり書影画像を作成

コマンド1つで、以下のような書影画像を作成します。
対象の本は、カメラからISBNを読み取って認識します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a3b9f7da-721a-f67c-954f-61bfb428da97.jpeg" width="200">

※ **カメラつきのmac**で確認しています。

## 準備

レンダリングはBlender3.0で行います。
「[Blenderのコマンドサンプル](https://qiita.com/SaitoTsutomu/items/6b70367455f843a979b1)」を参考に、`blender`コマンドと`blender_pip`コマンドを使えるようにしてください。

コマンドプロンプトで、BlenderのPythonに下記のようにインストールします。

```
blender_pip install -U requests openbd opencv-python pyzbar
```

また、`pyzbar`を使うために、下記のようにインストールします。

```
brew install zbar
```

書影のモデルや実行するためのPythonコードは、blenderのファイルに記述して、下記のSketchfabに用意しました。「Download 3D Model」をクリックし、「Original format (blend)」のDOWNLOADを押してください。

- [Set book image from ISBN](https://skfb.ly/oqqQX)

解凍した中の、`set-book-image-from-isbn/source/load_book.blend`を使います。
※ Pythonのコードは上記ファイルに記述されています。

書影を作りたい本を用意してください。

## 書影作成

コマンドプロンプトで下記を実行してください。カメラがアクティブになるので、ISBNのバーコードをカメラに見せてください。日本のISBNは、978ではじまります。192ではじまるバーコードではISBNを取得できないので、カメラに見せるときに指で隠してください。

```
blender -b -y load_book.blend --python-expr '__import__("bpy").ops.object.capture()' -o ./ -F JPEG -f 0
```

数秒ほどでカレントディレクトリに`0000.jpg`というファイルに書影が作成されます。

### オプションの説明

- `-b`：バックグラウンド実行
- `-y`：blenderファイルのPythonコード実行時に確認を省略
- `--python-expr コード`：コードを実行
- `-o パス`：画像の出力パス
- `-F フォーマット`：画像の出力形式
- `-f フレーム番号`：レンダリングするフレーム

※ `blender`コマンドの引数の順番通りに処理されます。

参考：[BlenderでISBNから書影の自動作成](https://qiita.com/SaitoTsutomu/items/d9debb55020bd4a765d1)

以上

