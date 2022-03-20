title: Blenderで六面図の自動作成
tags: Python Blender
url: https://qiita.com/SaitoTsutomu/items/c2ce94e711751217f760
created_at: 2021-10-20 12:11:31+09:00
updated_at: 2021-10-20 12:11:31+09:00
body:

# 目的

Blender2.93で六面図を自動作成するコマンドを紹介します。
macOSの例ですが、適宜直せばWindowsでも動くはずです。

## 作成するコマンドの内容

Blenderファイルを入力として、六面図を追加した新たなBlenderファイルを作成します。

# コード

下記を`make_image.py`として作成してください。

```py:make_image.py
import sys

import bpy
import fire
from mathutils import Euler


def make_image(save_path=None):
    """6方向からレンダリングして背景化"""
    import math

    CAMERA_NAME = "MyCam"
    LIGHT_NAME = "MyLight"
    IMG_NAMES = "top", "btm", "lft", "rgt", "frt", "bck"

    scene = bpy.context.scene
    scene.render.resolution_x = scene.render.resolution_y = 1000
    render = scene.render
    render.use_file_extension = True

    # すでに存在したときは、前のデータを削除する
    for name in IMG_NAMES:
        if obj := bpy.data.objects.get(f"img_{name}"):
            bpy.data.images.remove(obj.data)
            bpy.data.objects.remove(obj)
    if obj := bpy.data.collections.get("img"):
        bpy.data.collections.remove(obj)

    # Light
    light_data = bpy.data.lights.new(LIGHT_NAME, "SUN")
    light_data.energy = 2
    light_ob = bpy.data.objects.new(name=LIGHT_NAME, object_data=light_data)
    bpy.context.collection.objects.link(light_ob)

    # Camera
    cam_data = bpy.data.cameras.new(CAMERA_NAME)
    cam_data.type = "ORTHO"  # 平行投影
    cam_data.ortho_scale = 10  # 平行投影のスケール
    cam_ob = bpy.data.objects.new(name=CAMERA_NAME, object_data=cam_data)
    bpy.context.collection.objects.link(cam_ob)
    scene.camera = cam_ob

    new_col = bpy.data.collections.new("img")
    bpy.context.collection.children.link(new_col)
    r90 = math.pi / 2
    lst = [
        ((0, 0, 10), (0, 0, 0)),
        ((0, 0, -10), (2 * r90, 0, 0)),
        ((-10, 0, 0), (r90, 0, -r90)),
        ((10, 0, 0), (r90, 0, r90)),
        ((0, -10, 0), (r90, 0, 0)),
        ((0, 10, 0), (-r90, 2 * r90, 0)),
    ]
    for name, (loc, rot) in zip(IMG_NAMES, lst):
        fn = f"img_{name}"
        cam_ob.location = loc
        cam_ob.rotation_euler = light_ob.rotation_euler = Euler(rot, "XYZ")
        render.filepath = f"/tmp/{fn}"
        bpy.ops.render.render(write_still=True)
        bpy.ops.object.load_reference_image(filepath=f"/tmp/{fn}.png", view_align=False)
        img_ob = bpy.context.active_object
        img_ob.name = fn
        img_ob.location = [-i for i in loc]
        img_ob.rotation_euler = Euler(rot, "XYZ")
        img_ob.scale = 2, 2, 2
        img_ob.empty_image_side = img_ob.empty_image_depth = "FRONT"
        img_ob.use_empty_image_alpha = True
        img_ob.color[3] = 0.5
        img_ob.show_empty_image_perspective = False
        for col in img_ob.users_collection:
            col.objects.unlink(img_ob)
        new_col.objects.link(img_ob)
    # cameraとlightは消しておく
    bpy.data.cameras.remove(bpy.data.cameras[CAMERA_NAME])
    bpy.data.lights.remove(bpy.data.lights[LIGHT_NAME])
    bpy.context.view_layer.update()
    if save_path:
        bpy.ops.wm.save_as_mainfile(filepath=save_path)


if __name__ == "__main__":
    sys.argv = sys.argv[:1] + sys.argv[(sys.argv + ["--"]).index("--") + 1 :]
    fire.Fire(make_image)
```

## 準備

「[Blenderのコマンドサンプル](https://qiita.com/SaitoTsutomu/items/6b70367455f843a979b1)」を参考にFireをインストールしてください。
またBlenderは、`blender`コマンドで実行できるものとします。

# 実行

下記のようにしてシェルで実行します。

```
blender -b input.blend -P make_image.py -- out.blend
```

input.blendは、下記のような入力ファイルです。

![input.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/cf79fc59-4b8a-c095-91ad-f5ecbf585196.jpeg)


実行すると、out.blendという出力ファイルが作成されます。
out.blendには、`img`という新規のコレクションに、下記のように6枚の画像が追加されます。

![out.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3c93f2d5-2be7-91ae-1012-fe08e6eea9c6.jpeg)

下記の左側は正面から見た図です。右側はオリジナルのオブジェクトを非表示にしたものです。
六面図は不透明度を0.5にしているので右側が少し薄くなっていますが、同じ表示になっていることがわかります。

![change.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/87cb27a6-3afe-2b8a-b7b4-9af0ea3aa3ca.png)

以上



