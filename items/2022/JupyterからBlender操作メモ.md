title: JupyterからBlender操作メモ
tags: Python 3DCG Blender Jupyter
url: https://qiita.com/SaitoTsutomu/items/854c826bfc65ecae31f9
created_at: 2022-06-04 16:39:58+09:00
updated_at: 2022-06-04 17:00:58+09:00
body:

## 概要

JupyterからBlenderを使ってみたメモです。

## JupyterからBlenderを使うには

記事「[Jupyter NotebookからPythonのAPIでBlenderを操作する](https://qiita.com/odu_beyond/items/8bfb73bc24e8014e0903)」の通りにしてできました。

以降では下記を実行しているとします。

```py
from pathlib import Path
from subprocess import run
import bpy
from mathutils import Vector
from ipywidgets import interact
```

## コマンドの関数を取得するには

メニューやボタンで、`Ctrl + C`を押すと実行用のコードを取得できます。
あるいは、コマンドを実行すると、情報画面に実行したコードが出力されます。
これらのコードはメニューと同じ動作ですが、複数回実行する場合に効率的でないこともあります。
実際に立方体を作成して実行時間を比較してみましょう。

### 実行時間の比較

#### メニューのコード（立方体作成）
```py
%timeit -n 5 -r 5 bpy.ops.mesh.primitive_cube_add()
>>>
1.02 ms ± 138 µs per loop (mean ± std. dev. of 5 runs, 5 loops each)
```

#### 低レベルのコード（立方体作成）
```py
%%timeit -n 5 -r 5
pts = [[-1, -1, -1], [-1, -1, 1], [-1, 1, -1], [-1, 1, 1], [1, -1, -1], [1, -1, 1], [1, 1, -1], [1, 1, 1]]
verts = [Vector(pt) for pt in pts]
faces = [[0, 1, 3, 2], [4, 5, 7, 6], [0, 1, 5, 4], [2, 3, 7, 6], [0, 2, 6, 4], [1, 3, 7, 5]]
mesh = bpy.data.meshes.new(name="Cube")
mesh.from_pydata(verts, [], faces)
obj = bpy.data.objects.new(mesh.name, mesh)
bpy.context.layer_collection.collection.objects.link(obj)
>>>
58.7 µs ± 7.88 µs per loop (mean ± std. dev. of 5 runs, 5 loops each)
```

低レベルのコードの方が、ややこしいですが10倍以上速いです。

## 関数のヘルプを見るには

通常、Jupyterでは、カーソルを関数にあるところで`Ctrl + Tab`を押すとヘルプが見れます。しかし、Blenderの関数だと、詳しくわからないことがあります。その場合は、関数の括弧をつけずに実行すると、デフォルトの引数を確認できることがあります。

## 引数の書き方

Blenderの関数のいくつかは、位置引数ではなくキーワード引数にしないといけないことがあります。

## インタラクティブ操作

Jupyterでは、ipywidgetsを使って、関数の引数をインタラクティブに変更できます。
以下を実行すると、プルダウンから立方体の色を変更できるようになります。

```py
@interact
def cube_color(color={"red": (1, 0, 0), "green": (0, 1, 0), "blue": (0, 0, 1)}):
    if not (obj := bpy.data.objects.get("Cube")):
        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.object
    if not obj.active_material:
        obj.active_material = bpy.data.materials.new("Material")
    mat = obj.active_material 
    mat.use_nodes = False
    mat.diffuse_color = color + (1,)
```

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/1106e742-2558-4c11-cdcd-b48d153c5ce1.png" width="600">
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/72f5efe8-cc9d-d996-77b3-02529c4213a4.png" width="300">

ちなみに、Jupyter Labだと、ipywidgetsが表示されませんでした。

## 複数のblendファイル

Jupyterから複数のblendファイルも扱えます。
下記は、特定のフォルダのblendファイルのオブジェクト数を出力するコードです。

```py
%%time
for fnam in Path(特定のフォルダ).glob("*.blend"):
    bpy.ops.wm.open_mainfile(filepath=str(fnam))
    print(len(bpy.data.objects))
>>>
Wall time: 131 ms
```

blenderのコマンドで、同様のことができますが、時間がかかります。

```py
%%time
cmd = "/Applications/Blender.app/Contents/MacOS/Blender"
for fnam in Path(特定のフォルダ).glob("*.blend"):
    run([cmd, "-b", fnam, "--python-expr",
         'print(len(__import__("bpy").data.objects))'])
>>>
Wall time: 2.98 s
```

20倍以上の時間がかかっています。

以上

