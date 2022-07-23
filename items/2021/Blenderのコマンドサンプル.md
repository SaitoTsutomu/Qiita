title: Blenderのコマンドサンプル
tags: Python Blender Fire
url: https://qiita.com/SaitoTsutomu/items/6b70367455f843a979b1
created_at: 2021-10-14 22:25:00+09:00
updated_at: 2022-05-25 11:29:56+09:00
body:

# 目的

Blender2.93でPythonを実行するコマンドのサンプルを紹介します。
macOSの例ですが、適宜読み替えればWindowsでも動くはずです。

## 作成するコマンドの内容

コマンドの引数にテキストを指定すると、Blenderでテキストオブジェクト、カメラ、ライトを作成しBlenderファイルとして保存したり、レンダリングしてPNGファイルを作成したりします。

# コード

機能は、Scriptingの「テンプレート → Python → Background Job」のコードをベースに下記の2点を修正しました。

- argparseでなくFireを使うように修正。Fireについては「[Python-Fireについて](https://qiita.com/SaitoTsutomu/items/a5eb827737c9d59af2af)」を参照されたし。
- ライトの明るさを1000Wに修正。

```py:background_job.py
import sys
import bpy
import fire


def example_function(text, render_path=None, save_path=None):
    # Clear existing objects.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    txt_data = bpy.data.curves.new(name="MyText", type="FONT")

    # Text Object
    txt_ob = bpy.data.objects.new(name="MyText", object_data=txt_data)
    scene.collection.objects.link(txt_ob)  # add the data to the scene as an object
    txt_data.body = text  # the body text to the command line arg given
    txt_data.align_x = "CENTER"  # center text

    # Camera
    cam_data = bpy.data.cameras.new("MyCam")
    cam_ob = bpy.data.objects.new(name="MyCam", object_data=cam_data)
    scene.collection.objects.link(cam_ob)  # instance the camera object in the scene
    scene.camera = cam_ob  # set the active camera
    cam_ob.location = 0.0, 0.0, 10.0

    # Light
    light_data = bpy.data.lights.new("MyLight", "POINT")
    light_ob = bpy.data.objects.new(name="MyLight", object_data=light_data)
    scene.collection.objects.link(light_ob)
    light_ob.location = 2.0, 2.0, 5.0
    light_data.energy = 1000

    bpy.context.view_layer.update()
    if save_path:
        bpy.ops.wm.save_as_mainfile(filepath=save_path)
    if render_path:
        render = scene.render
        render.use_file_extension = True
        render.filepath = render_path
        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    sys.argv = sys.argv[:1] + sys.argv[(sys.argv + ["--"]).index("--") + 1 :]
    fire.Fire(example_function)
```

`background_job.py`として作成してください。

# 準備

コマンドをシンプルに記述するために、シェルで下記を設定しているとします。

```bash
alias blender=/Applications/Blender.app/Contents/MacOS/Blender
alias blender_pip="/Applications/Blender.app/Contents/Resources/2.93/python/bin/python3.9 -m pip"
```

下記のようにしてfireをインストールします。

```bash
blender_pip install -U fire
```

※ Windowsで、`blender_pip`でインストールできるのに`import`でエラーになる場合は、一旦アンインストールしてから、管理者権限のコマンドプロンプトでインストールし直すとうまくいくかもしれません。

# 実行

下記のようにしてシェルで実行します。

```
blender -b -P background_job.py -- 'Hello Blender!' img
```

- `-b`は、バックグラウンド実行の指定です。
- `-P Pythonファイル`で、Pythonファイルを実行します。
- `--`以降に、Pythonファイル用のオプションを指定します。

下記のように`img.png`が作成されます。

![img.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/5852a93a-4cae-14ef-8c3f-940b164a70c9.png)

また、コマンドの最後にファイル名を指定すると、Blenderファイルとして保存できます。

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

# 補足

## 1つのblenderのファイルの内容をPythonで扱いたい場合

下記のようにすると、blenderのファイルを開いた状態でPythonを実行できます。

```
blender blenderのファイル -P Pythonファイル
```

オプションの順番通りに処理するので、注意が必要です。たとえば、`blender -P Pythonファイル blenderのファイル`とすると、ファイルを開く前にPythonを実行します。

## 複数のblenderのファイルの内容をPythonで扱いたい場合

Pythonのコードで、下記のようにすれば、blenderのファイルを開いて扱えます。

```py
bpy.ops.wm.open_mainfile(filepath=ファイル名)
```

以上



