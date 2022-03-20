title: Blenderでハノイの塔を動かす
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/33b376c82a96434672d3
created_at: 2022-01-01 18:01:25+09:00
updated_at: 2022-01-04 09:50:11+09:00
body:

## Blenderでハノイの塔を動かす

「[k本のハノイの塔の動かし方（Python版）](https://qiita.com/SaitoTsutomu/items/a6d4aa081b70b7f7b784)」をBlenderで動かしてみました。

## 完成したアニメーション

![hanoi.gif](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/630029e4-5f82-47de-4e55-1a89badae6c7.gif)

## やり方

- Blenderを起動し、ワークスペースをScriptingにします。
- 「新規」を押し、下記をコピペし、テキストメニューの「スクリプト実行」をします。

```py
# Make an animation of Tower of Hanoi
import sys
from functools import lru_cache
from math import pi, sin
from typing import Any, Generator

import bpy


@lru_cache(maxsize=1024)
def nmove(m: int, n: int) -> float:
    """minimum number of moves

    :param m: number of disks
    :param n: number of rods
    :return: minimum number of moves
    """
    n = min(m + 1, n)
    if n == 2:
        return 1 if m == 1 else float("inf")
    elif n == 3:
        return 2 ** m - 1
    elif n == m + 1:
        return 2 * m - 1
    return min(nmove(i, n) * 2 + nmove(m - i, n - 1) for i in range(1, m))


def hanoi(m: int, pos: list[int]) -> Generator[tuple[int, int], None, None]:
    """Moves of Tower of Hanoi

    :param m: number of disks
    :param n: number of rods
    :return: from, to
    """
    if m == 1:
        yield pos[0], pos[-1]
        return
    n = len(pos)
    assert n > 2, "Too few len(pos)"
    mn = min((nmove(i, n) * 2 + nmove(m - i, n - 1), i) for i in range(1, m))[1]
    yield from hanoi(mn, [pos[0]] + pos[2:] + [pos[1]])
    yield from hanoi(m - mn, [pos[0]] + pos[2:-1] + [pos[-1]])
    yield from hanoi(mn, pos[1:-1] + [pos[0], pos[-1]])


def set_mat(material, color) -> None:
    """Set a material and smooth"""

    obj = bpy.context.selected_objects[0]
    bpy.ops.object.shade_smooth()
    obj.data.use_auto_smooth = True
    mat = bpy.data.materials.get(material) or bpy.data.materials.new(name=material)
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color
    obj.active_material = mat
    bpy.ops.object.modifier_add(type='BEVEL')
    mdf = obj.modifiers[0]
    mdf.width = 0.02
    mdf.segments = 3

def make_hanoi(m: int, n: int) -> None:
    """Make an animation of Tower of Hanoi

    :param m: number of disks
    :param n: number of rods
    """
    # Delete all objects.
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    # Add rods
    for i in range(n):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=12, radius=0.01, depth=0.5, location=(0, i, 0.2)
        )
        set_mat("M_rod", (0.5, 0.2, 0.1, 1))
    colors = [
        (0, 0.8, 0.1, 1),
        (1, 0.1, 0.1, 1),
        (0.8, 0.8, 0, 1),
        (0.1, 0.2, 1, 1),
        (0.8, 0.2, 0, 1),
    ]
    towers: list[list[Any]] = [[] for _ in range(n)]  # disks of rods
    # Add disks
    for i in range(m):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.1 * (m - i), depth=0.1, location=(0, 0, 0.1 * i)
        )
        towers[0] += bpy.context.selected_objects
        set_mat(f"M{i}", colors[i % len(colors)])
    # Set animation
    tm = 1
    for d in towers[0]:
        d.keyframe_insert(data_path="location", frame=tm)
    for fr, to in hanoi(m, list(range(n))):
        d = towers[fr].pop()
        frz = len(towers[fr]) * 0.1
        toz = len(towers[to]) * 0.1
        towers[to].append(d)
        for t in range(10):
            p = t / (10 - 1)
            y = (to - fr) * p + fr
            z = sin(pi * p) * 1 + (toz - frz) * p + frz
            d.location = [0, y, z]
            d.keyframe_insert(data_path="location", frame=tm + t + 1)
        tm += 10
    bpy.data.scenes[-1].frame_end = tm
    bpy.ops.screen.frame_jump(end=False)


if __name__ == "__main__":
    sys.argv = sys.argv[:1] + sys.argv[(sys.argv + ["--"]).index("--") + 1 :]
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    make_hanoi(m, n)
```

ちなみに、上記Pythonプログラムをファイルに保存し、下記のように実行することもできます。

```bash
blender -P Pythonのファイル -- ディスク数 塔の数
```

Blenderをコマンドラインから使う方法については、「[Blenderのコマンドサンプル](https://qiita.com/SaitoTsutomu/items/6b70367455f843a979b1)」も参考にしてください。

- [ディスク数4、塔の数4の例 - Sketchfab](https://skfb.ly/o88Lr)

以上

