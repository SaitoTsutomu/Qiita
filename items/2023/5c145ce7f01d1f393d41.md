title: Blenderのシミュレーションノード
tags: Blender Simulation GeometryNode
url: https://qiita.com/SaitoTsutomu/items/5c145ce7f01d1f393d41
created_at: 2023-07-16 10:54:16+09:00
updated_at: 2023-07-20 18:43:46+09:00
body:

## 概要

[Blender 3.6 LTS](https://www.blender.org/download/releases/3-6/)のGeometry NodesのSimulation Nodeを紹介します。

- Simulation Nodeとは
- 簡単な使い方
- 入力で指定する方法
- バウンドするボール

以降では、英語モードとします（Prefernces → Inteface → Translation → Language → English）。
下記も参考にしてみてください。

https://qiita.com/SaitoTsutomu/items/39eb1f022218c647c323

## Simulation Nodeとは

Simulation Nodeを使うと、1つ前のフレームのジオメトリーを元に、新しいジオメトリーを作れます。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2385e320-aa18-e8ac-6a58-e638d764fd7b.png)

上図のSimulation Inputから1つ前のフレームのジオメトリーを受け取り、ジオメトリーを更新し、更新したジオメトリーをSimulation Outputに渡します。
つまり、フレームごとに、枠内の処理がジオメトリーに反映されます。

## 簡単な使い方

ボールが移動するだけのシミュレーションを作ってみましょう。

### 手順

- すべてのオブジェクトを削除する（`ax`、`[Enter]`）。
- MeshのUV Sphereを追加する（`Amu`）。
- ワークスペースをGeometry Nodesにする。
- Sphereを選択したまま、Geometry Node EditorでNewを押す。
- Simulation Zoneを追加する（`Assim`、`[Enter]`、適当な位置でクリック）。
  - 以降では、「`[Enter]`、適当な位置でクリック」を省略します。
- Transform Geometryを追加する（`Astra`）。
  - TranslationのXを0.1にする。
- 下図のように接続する。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/bfcd89f2-e58a-8985-c310-229a6b4e8eed.png)

スペースでアニメーションしてみましょう。ボールが移動していきます。
これは、毎フレームごとにXに0.1が加算されるからです。

TranslationのXを変更して速度が変わるのを確認してみてください。
Geometry Nodesを変更したら、`[Shift + 左矢印]`で時刻を0にしてからスペースで開始してください。

## 入力で速度を指定する方法

速度を変更できるように、速度をシミュレーションの入力にしてみましょう。
Simulation Inputノードを選択し、ViewメニューのSidebar（`N`）でサイドバーを出し、Nodeタブを選びます。Simulation Stateで「`+`」を押し、追加された項目をダブルクリックし、名前をVelocityに変更します。また、Socket TypeをVectorにします。
下図のようにSimulationノードにVelocityが追加されます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/68e2170d-8ab9-ffdb-db54-0c08bedb4e3e.png" width="240">

Simulation InputのVelocityのXを0.1にし、下図のように接続します。わかりやすいように接続を曲げていますが、そのまま接続して構いません。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/8448ae64-1b22-680c-b6a5-8e0752ba57c1.png)

アニメーションしてみて、動きが変わらないことを確認しましょう。

もし、Simulation InputのVelocityをSimulation OutputのVelocityに接続しないと、動かなくなります。これは、Simulation OutputのVelocityが`0, 0, 0`のままで、その値が次のフレームのSimulation InputのVelocityになるからです。

## バウンドするボール

Vector Math（`Asvem`）、Compare（`Ascmp`）、Mix（`Asmx`）を追加します。
下図のように接続し、パラメータを設定します。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/946fad04-ca48-d29c-c1e6-3edb717aca68.png)

アニメーションすると、地面でバウンドするように動きます。

前回から次のようにVelocityを変化させているため、バウンドするように見えます。

- Zから0.05を引く（重力に相当）。
- Velocityの平均が-0.25以下なら、Velocityを初期値（`0.3, 0, 1`）に変更する。

以上

