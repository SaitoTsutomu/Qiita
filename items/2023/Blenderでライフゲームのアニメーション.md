title: Blenderでライフゲームのアニメーション
tags: Python 3DCG animation Blender lifegame
url: https://qiita.com/SaitoTsutomu/items/711989ba3e5ebcb78730
created_at: 2023-01-28 14:37:28+09:00
updated_at: 2023-02-03 20:50:47+09:00
body:

## これなに

Blenderでライフゲームのアニメーションを作成してみました。

https://ja.wikipedia.org/wiki/%E3%83%A9%E3%82%A4%E3%83%95%E3%82%B2%E3%83%BC%E3%83%A0

### 完成物

![lifegame.gif](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2a0afd99-2b60-95a6-c310-a5530e848f3d.gif)

配置は銀河です。

https://ja.wikipedia.org/wiki/%E9%8A%80%E6%B2%B3_(%E3%83%A9%E3%82%A4%E3%83%95%E3%82%B2%E3%83%BC%E3%83%A0)

## 手順

- Blender3.4を起動する。
- Scriptingワークスペースを開く
- 新規テキストを作成、以下をコピペし実行する。

```python
# ライフゲームのアニメーションを作成
from itertools import product

import bpy
import numpy as np


def galaxy() -> tuple[np.ndarray, int]:
    """銀河の配置と周期を返す"""
    # https://conwaylife.com/wiki/Kok's_galaxy
    cells = np.zeros((17, 17), bool)
    cells[4:6, 4:10] = cells[11:13, 7:13] = 1
    cells[7:13, 4:6] = cells[4:10, 11:13] = 1
    return cells, 8


def add_geometry(obj: bpy.types.Object) -> None:
    """ライフゲーム用のジオメトリーノード作成

    :param obj: 対象オブジェクト
    """
    modifier = obj.modifiers.new("GeometryNodes", "NODES")
    node_group = bpy.data.node_groups.new("Geometry Nodes", "GeometryNodeTree")
    modifier.node_group = node_group
    node_group.inputs.new("NodeSocketGeometry", "Geometry")
    node_group.outputs.new("NodeSocketGeometry", "Geometry")
    ndgi = node_group.nodes.new("NodeGroupInput")
    ndgo = node_group.nodes.new("NodeGroupOutput")
    ndip = node_group.nodes.new("GeometryNodeInstanceOnPoints")
    ndpo = node_group.nodes.new("GeometryNodeInputPosition")
    ndsx = node_group.nodes.new("ShaderNodeSeparateXYZ")
    ndcm = node_group.nodes.new("FunctionNodeCompare")
    ndcb = node_group.nodes.new("GeometryNodeMeshCube")
    node_group.links.new(ndgi.outputs[0], ndip.inputs[0])
    node_group.links.new(ndip.outputs[0], ndgo.inputs[0])
    node_group.links.new(ndpo.outputs[0], ndsx.inputs[0])
    node_group.links.new(ndsx.outputs[2], ndcm.inputs[0])
    node_group.links.new(ndcm.outputs[0], ndip.inputs[1])
    node_group.links.new(ndcb.outputs[0], ndip.inputs[2])
    node_group.links.new(ndip.outputs[0], ndgo.inputs[0])
    nds = [ndgi, ndgo, ndip, ndpo, ndsx, ndcm, ndcb]
    poss = [[80, 40], [410, 40], [250, 40], [-240, -99], [-80, -99], [80, -99], [-400, -28]]
    for nd, pos in zip(nds, poss):
        nd.location = pos


def main(cells: np.ndarray, ncycle: int, unit: int = 5) -> None:
    """ライフゲームのアニメーションを作成

    :param cells: 初期配置
    :param ncycle: 周期
    :param unit: フレーム数／周期, defaults to 5
    """
    nx, ny = cells.shape
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=nx - 1, y_subdivisions=ny - 1, size=nx)
    vtx = np.array(bpy.context.object.data.vertices).reshape(nx, ny)
    for x, y in product(range(nx), range(ny)):
        vtx[x, y].co.z = cells[x, y] * 0.5
    ss = [slice(None, -2), slice(1, -1), slice(2, None)]  # 前中後用のスライス
    sc = ss[1]  # 中央用のスライス
    bpy.context.scene.frame_end = ncycle * unit + 1
    for tm in range(ncycle + 1):
        bpy.context.scene.frame_current = tm * unit + 1
        for v in vtx.flat:
            v.keyframe_insert("co")
        new = np.sum([cells[s1, s2] for s1 in ss for s2 in ss if s1 != sc or s2 != sc], 0)
        n2, n3 = new == 2, new == 3
        cells[sc, sc] = cells[sc, sc] & n2 | n3
        for x, y in product(range(nx), range(ny)):
            vtx[x, y].co.z = cells[x, y] * 0.5
    bpy.context.scene.frame_current = 1
    add_geometry(bpy.context.object)


main(*galaxy())
```

https://qiita.com/SaitoTsutomu/items/cec67381a8789b40e377

- Layoutワークスペースに戻り、スペースでアニメーションを開始する。

## 説明

ライフゲームのセルを構成する格子は、Gridオブジェクトとします。ここで、1つのセルは、面ではなく**頂点**とします。このとき、頂点の生死は、**Z座標で判断する**ことにします。
時間ごとの生死を記録する必要があります。ここでは、頂点座標（`co`）にキーフレームを打ちます。
そして、Z座標の値による立方体の表示は、ジオメトリーノードを使うことにします（後述）。

### galaxy()関数

[銀河](https://ja.wikipedia.org/wiki/%E9%8A%80%E6%B2%B3_(%E3%83%A9%E3%82%A4%E3%83%95%E3%82%B2%E3%83%BC%E3%83%A0))の2次元配列を作成し、周期とともに返します。
周期は8なので、8回目に同じ配置に戻ります。

### add_geometry()関数

下記のジオメトリーノードを作成します。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/9d5ba44e-7cbe-b0f1-e637-c4b2f90d0c23.png)

対象のメッシュは格子（Grid）です。このポイントに立方体を出せばいいので、`Instance on Points`を挟んで、`Cube`を`Instance`に繋ぎます。
生きているセルだけ表示したいので、`Position`で座標をとり、`Separate XYZ`でZ座標だけにし、`Greater Than`で0以上を選択し、`Selection`につなぎます。

### main()関数

順番に説明します。

```python
    nx, ny = cells.shape
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=nx - 1, y_subdivisions=ny - 1, size=nx)
    vtx = np.array(bpy.context.object.data.vertices).reshape(nx, ny)
    for x, y in product(range(nx), range(ny)):
        vtx[x, y].co.z = cells[x, y] * 0.5
```

- `nx`、`ny`に縦のセル数、横のセル数を入れます。
- `primitive_grid_add`で格子を作成します。
- `vtx`に格子上の頂点を2次元配列として作成します。
- `vtx`の`co.z`に初期配置を設定します。生きていれば0.5に、そうでなければ0になります。

```python
    ss = [slice(None, -2), slice(1, -1), slice(2, None)]  # 前中後用のスライス
    sc = ss[1]  # 中央用のスライス
    bpy.context.scene.frame_end = ncycle * unit + 1
```

- `ss`、`sc`は、ライフゲームの計算用のスライスです。
- シーンの`frame_end`に`周期 * フレーム数 + 1`を設定します。

```python
   for tm in range(ncycle + 1):
```

- 周期数＋1回ループします。ループの最初と最後が同じ配置なので、アニメーションを繰り返し再生すると繋がります。

```python
        bpy.context.scene.frame_current = tm * unit + 1
        for v in vtx.flat:
            v.keyframe_insert("co")
```

- 時刻を進めます。
- 頂点座標（`co`）にキーフレームを打ちます。

```python
        new = np.sum([cells[s1, s2] for s1 in ss for s2 in ss if s1 != sc or s2 != sc], 0)
        n2, n3 = new == 2, new == 3
        cells[sc, sc] = cells[sc, sc] & n2 | n3
```

- 次の配置を計算します。`new`は、隣接8マスの生存数の和です。
- `n2`と`n3`が、「和が2か」と「和が3か」です。`n2`ならば現在生存⇛生存で、`n3`なら発生です。

```python
        for x, y in product(range(nx), range(ny)):
            vtx[x, y].co.z = cells[x, y] * 0.5
```

- 新しい配置で座標を更新します。

```python
    bpy.context.scene.frame_current = 1
    add_geometry(bpy.context.object)
```

- 時刻を1に戻します。
- ジオメトリーノードを作成します。

## 追記

アドオン化しました。

https://github.com/SaitoTsutomu/LifeGame

- インストールしたら「テスト中で」で有効化できます。有効化するとサイドバーの編集タブにパネルがでます。
- 銀河を作りたい場合は、「Make Sample」ボタンを押すだけで、メッシュ、キーフレームアニメーション、ジオメトリーノードを自動生成して、アニメーションが始まります。
- 任意のパターンを作成したい場合は、「Make Grid」で格子を作成したあと、初期配置に置きたいセルの頂点を選択して「Make Anim」を押すとアニメーションが始まります。

NX、NYが格子の横と縦の数で、NCycleが周期、Unitが1コマのキーフレーム数です。

## Selectionソケットについて

Z座標が正の頂点を選択するために、Compareノードで「Zが0以上」をSelectionにつないでましたが、Blenderでは0以上をTrueとみなすようです。そのため下記のようにCompareを使うことなく直接ZをSelectionにつなげられます。アドオンでは、そのようにしています。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2504af3b-423d-e291-4513-9edab183037f.png)


以上

