title: Blenderの画像とPythonあれこれ
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/b0baf098017f01dffea8
created_at: 2022-09-04 11:29:00+09:00
updated_at: 2022-09-04 18:31:56+09:00
body:

## Blenderの画像とPythonあれこれ

### PNG画像をJPEGで保存するとき

ファイルサイズを圧縮するために、PNGファイルをJPEGで保存すると、色合いが変化することがありました。
完全な解決方法かはわからないですが、下記のようにしたら改善しました。

- レンダープロパティのカラーマネジメントのビュー変換をFlimicから標準に変える

| 変更前 | | 変更後 |
|--|--|--|
| <img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9e66a40c-f4fe-d6c5-d003-08cb49754230.png" width="240"> | → | <img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/97eb94ca-4465-18e1-e227-ea85259f7c5b.png" width="240"> |

Pythonの場合

```py
bpy.context.scene.view_settings.view_transform = "Standard"  # 標準に設定
# 画像保存
bpy.context.scene.view_settings.view_transform = "Filmic"  # Flimicに戻す
```

### 品質などを指定して画像を保存

画像を保存するときに、ダイアログでフォーマットやカラーや品質を設定できます。
Pythonでこれを実現するとします。Imageオブジェクトの`save()`メソッドには引数がなく、オブジェクトの属性にもこれらの項目はありません。これらを設定するには、下記のようにする必要があるようです。

```py
stng = bpy.context.scene.render.image_settings
stng.file_format = フォーマット  # ex. "JPEG", "PNG"
stng.color_mode = カラー  # ex. "BW", "RGB", "RGBA"
stng.quality = 品質  # 0-100

img = bpy.data.images[対象画像]
img.save_render(パス, scene=bpy.context.scene)
```

`color_mode`の設定では、先に`file_format`を決定する必要があることに注意してください。
たとえば、`file_format == "JPEG"`のときに、`color_mode`を`"RGBA"`にするとエラーになります。
なお、`color_mode == "RGBA"`のときに`file_format`を`"JPEG"`にすると、`color_mode`が`"RGB"`に変わるだけでエラーにはなりません。

### アルファがあるかどうかの判定

画像がアルファを持っているかどうかを直接表す属性はないようですが、下記のようにして判定できました。ただし、JPEGとPNGのいくつかの種類でのみ確認しています。

```py
img = bpy.data.images[対象画像]
has_alpha = img.depth // (img.is_float * 3 + 1) // 8 % 2 == 0
```

調べた範囲では、`img.depth // (img.is_float * 3 + 1) // 8`は、`1, 2, 3, 4`の値を取り、それぞれ、「1色、1色＋α、3色、3色＋α」でした。

以上

