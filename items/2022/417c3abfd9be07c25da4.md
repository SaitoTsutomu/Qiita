title: Blenderで数理最適化による分割の復元
tags: Python 3DCG Blender 最適化 数理最適化
url: https://qiita.com/SaitoTsutomu/items/417c3abfd9be07c25da4
created_at: 2022-05-01 22:13:29+09:00
updated_at: 2023-11-24 07:41:47+09:00
body:

## 概要

メッシュの**細分化を戻す**処理を数理最適化で試してみたので紹介します。

## 方針

細分化では三角面と四角面を分割します。ここでは、四角面のみ対象にします。
分割により追加された点の多くは、4辺と4面に接続しています。
この点を溶解対象候補とします。また、1つの四角面で1点までしか溶解できないとします。
さらに、溶解した点がなるべくつながるようにします。

## 準備

### PuLPのインストール

数理最適化のパッケージを使うので、インストールが必要です。
普段は、[Python-MIP](https://www.python-mip.com/)を使うのですが、Blenderでは動かないので、代わりに[PuLP](https://github.com/coin-or/pulp)を使います。
PuLPのインストール方法は、「[Blenderで可能な限り三角面を四角面に変換する（数理最適化）](https://qiita.com/SaitoTsutomu/items/b608c80d70a54718ec78)」を参照してください。

### コードの準備

Scriptingワークスペースで新規を押し、下記をコピペしてください。

```py
import bpy
import bmesh
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

obj = bpy.context.edit_object
bm = bmesh.from_edit_mesh(obj.data)
bm.verts.ensure_lookup_table()
vs = {vert for vert in bm.verts if len(vert.link_faces) == len(vert.link_edges) == 4}

m = LpProblem(sense=LpMaximize)
vx = {vert: LpVariable(f"x{vert.index:03}", cat="Binary") for vert in vs}
vy = {vert: LpVariable(f"y{vert.index:03}", cat="Binary") for vert in vs}
m.setObjective(lpSum(vx.values()) + lpSum(vy.values()))
for face in bm.faces:
    ss = {vert for vert in face.verts} & vs
    if len(ss) >= 2:
        m += lpSum(vx[vert] for vert in ss) <= 1
for vert, va in vy.items():
    ss = [vx[v] for edge in vert.link_edges
          if (v := edge.other_vert(vert)) in vx]
    if len(ss) >= 2:
        m += va <= lpSum(ss) / 2
    m += va + vx[vert] <= 1
m.verbose = 0
m.solve()
if m.status != 1:
    print("Not solved.")
else:
    bpy.ops.mesh.select_all(action="DESELECT")
    for vv in [vx, vy]:
        n = 0
        for vert, va in vv.items():
            if value(va) > 0.5:
                vert.select_set(True)
                n += 1
        if n:
            bpy.ops.mesh.dissolve_verts()
        print(f"{n} vertices are dissolved.")
bm.free()
del bm
```

参考：[BlenderでPythonを実行する方法](https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377)

## グリッドの例

Layoutワークスペースのオブジェクトモードで追加のメッシュのグリッドを選びます。
編集モードに入ってください（下図の分割前）。
細分化を選んでください（下図の分割後）。
Scriptingワークスペースでスクリプト実行してください。
Layoutワークスペースで確認します（下図の復元後）。

|分割前|分割後|復元後|
|--|--|--|
|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/d3196764-c2a3-bd91-41b3-ceb9edf275ad.png)|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/331c87c2-c69b-e96c-587b-6f38094eb338.png)|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/f549e954-9ad8-8db7-7078-8f553287bc9a.png)|

概ね復元されています。4辺と4面に接続する点のみ溶解対象候補にしたので、外周の点が残っています。

## モンキーの例

Layoutワークスペースのオブジェクトモードで追加のメッシュのモンキーを選びます。
編集モードに入ってください（下図の分割前）。
細分化を選んでください（下図の分割後）。
Scriptingワークスペースでスクリプト実行してください。
Layoutワークスペースで確認します（下図の復元後）。

|分割前|分割後|復元後|
|--|--|--|
|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2943d8f7-9dd0-79ee-f0e0-f51d611b1d01.png)|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/234480e9-6b0b-a910-f693-9e7fd9ae96a2.png)|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2309c334-020f-9b3c-0e03-26fec3b72f05.png)|

概ね復元されています。三角面は対象外なので、分割されたままになっています。

## トーラスの例

Layoutワークスペースのオブジェクトモードで追加のメッシュのトーラスを選びます。
左下のオペレーターパネルで、大セグメント数を12に、小セグメント数を4にします。
トーラスは、数理最適化モデルの変数が多くなるので、ローポリにします。
編集モードに入ってください（下図の分割前）。
細分化を選んでください（下図の分割後）。
Scriptingワークスペースでスクリプト実行してください。
Layoutワークスペースで確認します（下図の復元後）。

|分割前|分割後|復元後|
|--|--|--|
|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/330900a1-c77d-22a8-3ead-c6436aa18ced.png)|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/73e13d6b-5662-84e4-1529-4bff68ee8de3.png)|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/ef81ec5d-35f3-7db3-39e6-9db7a25ae54b.png)|

トーラスは、すべての点が溶解対象の候補なので、水平面と垂直面で、復元方法がそれぞれ2パターンあります。復元後は分割前と同じにはなってないですが、数理モデルで想定した通りの結果になっています。

## 分割の復元との比較

細分化を戻す処理は、編集モードの辺メニューの分割の復元でもできます。
グリッドとトーラスは期待した通りに復元されますが、複雑なメッシュでは元に戻らないことがあります。
下図はモンキーの例です。

|分割前|分割後|分割の復元|最適化による復元|
|--|--|--|--|
|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/f9e88d30-f64a-2523-6f66-c22f09f143dc.png)|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/54c4b41d-1ebe-eaa6-deef-e0e6f1f66179.png)|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3991aa00-b431-e9c9-a5ce-8b03a7839526.png)|![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/e830c947-be4c-7030-32ea-822fd6bbfcaa.png)|

以上











