title: Blenderで、Pythonを使って頂点カラーに色を塗る
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/05b2481e5d1d98652043
created_at: 2022-01-29 08:47:06+09:00
updated_at: 2022-05-06 20:36:15+09:00
body:

## やること

オブジェクト内の頂点の高さに応じて、色を塗ってみましょう。
ノードでもできますが、ここではPythonを使います。

## 完成物

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/c21b226e-0c08-540c-1db4-b727372c0eb7.jpeg" width="300">

図はスザンヌの例ですが、どんなメッシュでも同じようにできます。
頂点カラーは、一番高いところを赤に、一番低いところを青にしています。

## 手順

- オブジェクト作成
- Pythonで頂点カラー作成
- マテリアル作成

## やってみよう

最初に、スザンヌを作成してください。

※ スザンヌ以外のメッシュのオブジェクトで試すこともできます。その場合は、後述のコードの`Suzanne`を変えてください。

Sciptingワークスペースで新規作成して、下記をコピペして実行してください。

```py
import colorsys
import bpy

obj = bpy.data.objects["Suzanne"]  # 対象オブジェクト
zz = [v.co[2] for v in obj.data.vertices]  # 頂点の高さ
if not obj.data.vertex_colors:
    obj.select_set(state=True)
    bpy.ops.mesh.vertex_color_add()  # 頂点カラーの作成
vc = obj.data.vertex_colors[0].data  # 頂点カラーのデータ
a = (max(zz) - min(zz)) / 0.7
b = min(zz)

for polygon in obj.data.polygons:
    for i, v in zip(polygon.loop_indices, polygon.vertices):
        h = 0.7 - (zz[v] - b) / a
        vc[i].color = colorsys.hsv_to_rgb(h, 1, 1) + (1,)
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

Layoutワークスペースに戻ってください。
このままでは、頂点カラーは見えません。マテリアルを設定することで頂点カラーを確認できます。

※ 下記のように、シェーディングのカラーを頂点にするとマテリアルを設定せずに頂点カラーを確認できますが、レンダリングでは色は付きません。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/45767f35-4563-7ea7-378d-c1c38b3c4786.jpeg" width="300">

Shadingワークスペースで、マテリアルを新規作成して、下記のようにしてください。頂点カラーノードは、追加の入力にあります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/dcdd3077-8c00-7908-0bd9-9e357c293339.jpeg" width="500">

## Pythonコードの簡単な説明

1つのオブジェクトに対して処理します。対象オブジェクトを下記のように`obj`に入れます。

```py
obj = bpy.data.objects["Suzanne"]  # 対象オブジェクト
```

頂点の高さが必要になるので、頂点ごとの高さを`zz`に入れます。

```py
zz = [v.co[2] for v in obj.data.vertices]  # 頂点の高さ
```

頂点カラーは、オブジェクトの新規作成時には存在していません。1つのオブジェクトに頂点カラーをいくつでも作成できます。コードでは、1つも頂点カラーが存在しないときに、下記で頂点カラーを作成しています。

```py
bpy.ops.mesh.vertex_color_add()  # 頂点カラーの作成
```

頂点カラーを作成すると、オブジェクトデータプロパティで、下記のように確認できます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/79698a44-a2a0-14ad-c2ca-c3fe5deadf1c.jpeg" width="200">

作成した頂点カラー（上記の`Col`）のデータを下記のように`vc`に入れます。

```py
vc = obj.data.vertex_colors[0].data
```

下記のようにして、オブジェクトの面（`polygon`）ごとに処理をします。

```py
for polygon in obj.data.polygons:
```

頂点カラーの値は、「面と頂点の組み合わせ」ごとに持っています。たとえば、`i`番目の「面と頂点の組み合わせ」の色は、`vc[i].color`です。

「面と頂点の組み合わせ」のインデックスは、`polygon.loop_indices`に入っています。
また、対応する頂点のインデックスは、`polygon.vertices`に入っています。

グラデーションはHSVの色相（`h`）を変えることで、作成しています。
`h`の値は、高さが一番高いところが`1`に、低いところが`0.7`になるように計算しています。
HSVからRGBの変換には、`colorsys.hsv_to_rgb`を使います。BlenderのカラーはRGBとアルファの4つの値なので、` + (1,)`でアルファを追加します。

## ノードの例

下記のようにするとノードだけでもできます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2baab017-4613-9fa5-4a12-4a75e66fe857.jpeg" width="６00">


以上

