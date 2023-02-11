title: Blenderで星空を作る
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/1161fce06ade74be4d5d
created_at: 2023-02-11 17:29:42+09:00
updated_at: 2023-02-11 17:29:42+09:00
body:

# Blenderで星空を作る

## これなに

Blenderで下記のような星空を作る方法の紹介です。


<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3bd5cbb2-1f58-de8e-4fc8-ee5560eacc3b.jpeg" width="500">

## データ

星や星座の情報は、下記のヒッパルコス星表を使います。

http://astro.starfree.jp/commons/hip/

上記のサイトから下記の3つのファイルを使います（ダウンロードはプログラムから行います）。

- `hip_lite_major.csv`：3215個の星の情報です。この中のHIP番号と赤経と赤緯と視等級（明るさ）を使います。
- `hip_100.csv`：100個の星の情報です。星は上記のサブセットですが、B-V色指数が増えています。上記の表にマージします。B-V色指数は小さいと青っぽく、大きいと赤っぽく見えるそうなので、この値を使ってカラーランプで適当に色をつけます。
- `hip_constellation_line.csv`：星座の線の情報です。2点のHIP番号を使います。

これらのデータから表を2つ（`df`、`dfl`）を作成します。それぞれ**星**と**星座の線**です。

## 考え方

下記の4種類を作ります。

- データ：サイトからCSVをダウンロードし、星と星座の2つの表を作成します。
- マテリアル：星と星座の線の2種類のマテリアルを作成します。
- ジオメトリーノード：星と星座の線のジオメトリーを作成します。
- オブジェクト。星を頂点として、星座の線を辺として作成します。

### データ

データの座標は赤道座標系になってます。これをXYZ座標に変換します。
ダウンロードしたファイルはキャッシュします。

### マテリアル

**星座の線のマテリアル（line）**
放射だけ暗いグレーに設定しています。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/735561b0-a442-dac3-f187-146b06ce879b.png" width="400">

**星のマテリアル（star）**
放射と放射の強さを設定しています。それぞれ、**bv**と**lv**という属性の情報を使います。属性はオブジェクト作成時に作成しています。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3876b071-5f0b-f258-f513-f0763edb6d6f.png" width="600">

### ジオメトリーノード

「ポイントにインスタンス作成」でICO球を配置します。これが星を表します。
「メッシュのカーブ化」「カーブのメッシュ化」で辺を円柱にします。これが星座の線を表します。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/d591b75e-a319-0d77-72c9-3d010afee2d1.png)

### オブジェクト

オブジェクトは、頂点と辺からなるメッシュです。面はありません。通常、面のないメッシュは見えませんが、ジオメトリーノードによって可視化しています。
ここでは下記の頂点の属性も作成し、マテリアルから利用できるようにしています。

- `bv`：色指数というものです。カラーランプで使うために、0から0.94ぐらいになるようにしています。1は暗いグレーです。暗いグレーはB-V色指数を持たない星用です。
- `lv`：視等級から計算しています。放射の強さに使います。

## 作ってみよう

pandasのインストールが必要です（下記参考）。

https://qiita.com/SaitoTsutomu/items/6b70367455f843a979b1

以下をコピーしてScriptingワークスペースで実行してください。

```py
"""
星表から星空を作る
"""
import time
from math import pi, tau
from pathlib import Path

import bpy
import numpy as np
import pandas as pd


def make_dataframe():
    tmp = Path("/tmp")
    if not tmp.is_dir():
        tmp = Path(".")
    hip_lite_major = tmp / "hip_lite_major.csv"
    if not hip_lite_major.exists():
        url = "http://astro.starfree.jp/commons/hip/hip_lite_major.csv"
        _df = pd.read_csv(url, header=None, index_col=0)
        _df.to_csv(hip_lite_major, header=None)
        time.sleep(0.1)
    df = pd.read_csv(hip_lite_major, header=None, index_col=0)
    df.columns = "赤経時 赤経分 赤経秒 赤緯符号 赤緯度 赤緯分 赤緯秒 視等級".split()

    hip_100 = tmp / "hip_100.csv"
    if not hip_100.exists():
        url = "http://astro.starfree.jp/commons/hip/hip_100.csv"
        _df = pd.read_csv(url, encoding="cp932", header=None, index_col=0)
        _df.to_csv(hip_100, encoding="cp932", header=None)
        time.sleep(0.1)
    usecols = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12]
    df100 = pd.read_csv(hip_100, encoding="cp932", header=None, index_col=0, usecols=usecols)
    df100.columns = "赤経時 赤経分 赤経秒 赤緯符号 赤緯度 赤緯分 赤緯秒 視等級 BV色指数".split()

    hip_constellation_line = tmp / "hip_constellation_line.csv"
    if not hip_constellation_line.exists():
        url = "http://astro.starfree.jp/commons/hip/hip_constellation_line.csv"
        _df = pd.read_csv(url, header=None)
        _df.to_csv(hip_constellation_line, header=None, index=False)
        time.sleep(0.1)
    dfl = pd.read_csv(hip_constellation_line, header=None)
    dfl.columns = "Abbr HIP1 HIP2".split()

    df = df.join(df100.BV色指数, how="left").fillna(2)
    df.insert(0, "ID", range(len(df)))
    df["Long"] = (df.赤経時 / 24 + df.赤経分 / 1440 + df.赤経秒 / 86400) * tau
    df["Lati"] = (df.赤緯度 / 90 + df.赤緯分 / 5400 + df.赤緯秒 / 324000) * pi
    df.Lati *= df.赤緯符号 - 0.5
    df["Z"] = np.sin(df.Lati)
    r = np.cos(df.Lati)
    df["X"] = r * np.cos(df.Long)
    df["Y"] = r * np.sin(df.Long)

    dfl = dfl[dfl.HIP1.isin(df.index) & dfl.HIP2.isin(df.index)]
    dfl = dfl.join(df.ID.rename("ID1"), "HIP1")
    dfl = dfl.join(df.ID.rename("ID2"), "HIP2")
    return df, dfl


def make_material(obj):
    mat = bpy.data.materials.new(name="line")
    mat.use_nodes = True
    ndpb = mat.node_tree.nodes["Principled BSDF"]
    ndpb.inputs[19].default_value = 0.05, 0.05, 0.05, 1

    mat = bpy.data.materials.new(name="star")
    obj.active_material = mat
    mat.use_nodes = True
    ndpb = mat.node_tree.nodes["Principled BSDF"]
    nda1 = mat.node_tree.nodes.new("ShaderNodeAttribute")
    nda1.attribute_name = "bv"
    nda1.attribute_type = "INSTANCER"
    nda2 = mat.node_tree.nodes.new("ShaderNodeAttribute")
    nda2.attribute_name = "lv"
    nda2.attribute_type = "INSTANCER"
    ndcr = mat.node_tree.nodes.new("ShaderNodeValToRGB")
    ndcr.color_ramp.color_mode = "HSV"
    ndcr.color_ramp.hue_interpolation = "CCW"
    ndcr.color_ramp.elements.new(0.95)
    ndcr.color_ramp.elements[0].color = 0, 0.1, 1, 1
    ndcr.color_ramp.elements[1].color = 1, 0, 0, 1
    ndcr.color_ramp.elements[2].color = 0.01, 0.01, 0.01, 1
    nda1.location = -450, -180
    nda2.location = -450, 5
    ndcr.location = -270, 5
    mat.node_tree.links.new(nda1.outputs[2], ndcr.inputs[0])
    mat.node_tree.links.new(ndcr.outputs[0], ndpb.inputs[19])
    mat.node_tree.links.new(nda2.outputs[2], ndpb.inputs[20])


def make_geometry_node(obj):
    modifier = obj.modifiers.new("GeometryNodes", "NODES")
    node_group = bpy.data.node_groups.new("Geometry Nodes", "GeometryNodeTree")
    modifier.node_group = node_group
    node_group.inputs.new("NodeSocketGeometry", "Geometry")
    node_group.outputs.new("NodeSocketGeometry", "Geometry")
    ndgi = node_group.nodes.new("NodeGroupInput")
    ndic = node_group.nodes.new("GeometryNodeMeshIcoSphere")
    ndic.inputs[0].default_value = 0.003
    ndio = node_group.nodes.new("GeometryNodeInstanceOnPoints")
    ndmc = node_group.nodes.new("GeometryNodeMeshToCurve")
    ndcc = node_group.nodes.new("GeometryNodeCurvePrimitiveCircle")
    ndcc.inputs[0].default_value = 6
    ndcc.inputs[4].default_value = 0.001
    ndcm = node_group.nodes.new("GeometryNodeCurveToMesh")
    ndsm = node_group.nodes.new("GeometryNodeSetMaterial")
    ndsm.inputs[2].default_value = bpy.data.materials["star"]
    ndsm2 = node_group.nodes.new("GeometryNodeSetMaterial")
    ndsm2.inputs[2].default_value = bpy.data.materials["line"]
    ndjo = node_group.nodes.new("GeometryNodeJoinGeometry")
    ndgo = node_group.nodes.new("NodeGroupOutput")

    node_group.links.new(ndgi.outputs[0], ndio.inputs[0])
    node_group.links.new(ndic.outputs[0], ndio.inputs[2])
    node_group.links.new(ndgi.outputs[0], ndmc.inputs[0])
    node_group.links.new(ndmc.outputs[0], ndcm.inputs[0])
    node_group.links.new(ndcc.outputs[0], ndcm.inputs[1])
    node_group.links.new(ndio.outputs[0], ndsm.inputs[0])
    node_group.links.new(ndcm.outputs[0], ndsm2.inputs[0])
    node_group.links.new(ndsm.outputs[0], ndjo.inputs[0])
    node_group.links.new(ndsm2.outputs[0], ndjo.inputs[0])
    node_group.links.new(ndjo.outputs[0], ndgo.inputs[0])

    nds = [ndgi, ndic, ndio, ndmc, ndcc, ndcm, ndsm, ndsm2, ndjo, ndgo]
    locs = [[-315, 116], [-315, -18], [-151, 116], [8, 116], [8, -18]]
    locs += [[170, 116], [170, -18], [325, 116], [325, -18], [482, 116]]
    for nd, loc in zip(nds, locs):
        nd.location = loc


def make_object():
    df, dfl = make_dataframe()
    verts = df[["X", "Y", "Z"]].values.tolist()
    edges = dfl[["ID1", "ID2"]].values.tolist()
    mesh = bpy.data.meshes.new(name="Star")
    mesh.from_pydata(verts, edges, [])
    obj = bpy.data.objects.new(mesh.name, mesh)
    bpy.context.layer_collection.collection.objects.link(obj)
    mesh.attributes.new("lv", "FLOAT", "POINT")
    mesh.attributes["lv"].data.foreach_set("value", ((4 - df["視等級"]) ** 2 * 5).to_list())
    mn, mx = df.BV色指数.min(), df.BV色指数.max()
    mesh.attributes.new("bv", "FLOAT", "POINT")
    mesh.attributes["bv"].data.foreach_set("value", ((df.BV色指数 - mn) / (mx - mn)).to_list())
    make_material(obj)
    make_geometry_node(obj)
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = 0, 0, 0, 1
    bpy.context.scene.eevee.use_bloom = True


make_object()
```

Layoutワークスペースで、３Dビューのシェーディングをレンダーにしてください。下記のように表示されます。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/739349c0-0712-8f1a-6390-9e68b8569995.png)

以上

