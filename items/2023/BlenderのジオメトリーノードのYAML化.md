title: BlenderのジオメトリーノードのYAML化
tags: Python 3DCG addon Blender
url: https://qiita.com/SaitoTsutomu/items/7213552baf9b65de3df6
created_at: 2023-01-24 07:51:00+09:00
updated_at: 2023-01-28 00:30:55+09:00
body:

## これなに

Blender3.4のジオメトリーノードで下記のようなことができるといいなと思って作ってみたアドオンの紹介です。

- ビジュアルでなくテキストで読みたい。
- Pythonでジオメトリーノードを作成するのではなく、テキストからジオメトリーノードを作成したい。

とりあえず、サンプルが動く状態になったので紹介します。
ジオメトリーノードはテキストにしても読むのは大変でした。

## 不具合

一部のノードでしか動作確認していませんが、下記の不具合があります。

- Join Geometryノードの入力の順番が取得不可なので、順番が正しくないです。
- 非表示の入力ソケットの判別ができないので、inputsに不要なものが出ます。
- ShaderNodeFloatCurveの曲線が再描画されません。
- Undoなどをすると、落ちることがあり不安定です。

## 使い方

下記のアドオンをインストールします（テスト中に表示されます）。

https://github.com/SaitoTsutomu/GeometryTools

機能は、ジオメトリーノードエディタのサイドバーの編集タブの「Copy」と「Paste」ボタンで提供されます。
このボタンでYAML形式でコピペできます。

### コピー

適当なオブジェクトのジオメトリーノードを作成して「Copy」を押すと、YAML形式でクリップボードにコピーします。

コピー対象は、オブジェクトの`modifiers`の該当モディファイアーの`node_group`の`inputs`、`outputs`、`nodes`です。

### ペースト

変更したいオブジェクトを選択して「Paste」でクリップボードから貼り付けます。
元のノードは削除されるので注意してください。

## サンプル

### 卵のサンプル

下記をコピーしてペーストしてください。

```yaml
Geometry Nodes:
  Inputs:
    Input_0: Geometry/NodeSocketGeometry
  Outputs:
    Output_1: Geometry/NodeSocketGeometry
  Position:
    location: [-600, 183]
  Separate XYZ:
    location: [-595, 118]
    inputs:
      0: ~Position
  Map Range:
    location: [-463, 127]
    inputs:
      0: ~Separate XYZ/2
      1: -1.0
  Float Curve:
    location: [-311, 196]
    mapping:
    - AUTO, 0.0, 0.8
    - AUTO_CLAMPED, 0.2, 0.85
    - AUTO, 1.0, 0.7
    inputs:
      1: ~Map Range/0
  Combine XYZ:
    location: [-77, 191]
    inputs:
      X: ~Float Curve
      Y: ~Float Curve
      Z: 1.0
  Vector Math:
    location: [-74, 43]
    operation: MULTIPLY
    inputs:
      0: ~Position
      1: ~Combine XYZ
  UV Sphere:
    location: [83, 195]
  Set Position:
    location: [88, 65]
    inputs:
      Geometry: ~UV Sphere
      Position: ~Vector Math/0
  Set Shade Smooth:
    location: [235, 196]
    inputs:
      Geometry: ~Set Position
  Group Output:
    location: [395, 192]
    inputs:
      Geometry: ~Set Shade Smooth
```

下記のような[卵の形状](https://qiita.com/SaitoTsutomu/items/39eb1f022218c647c323#%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB---%E5%8D%B5)のノードが作成されます。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/71d9e6c7-f3c9-ac89-610b-68a62bf17d14.png)

### 植物のサンプル

下記の動画の植物の例です。

https://youtu.be/a6oHSwp-6_0

- 葉っぱを作って、元を原点にしてください。
- 茎用のマテリアルを設定してください。
- 下記をコピーしてペーストしてください。
- モディファイアーのLeafに葉っぱを、Materialに茎のマテリアルを設定し、Sizeを1に増やしてみてください。

```yaml
Geometry Nodes:
  Inputs:
    Input_0: Geometry/NodeSocketGeometry
    Input_2: Size/NodeSocketFloatFactor, 1.0, 0.0, 1.0
    Input_3: Leaf/NodeSocketObject
    Input_4: Material/NodeSocketMaterial
  Outputs:
    Output_1: Geometry/NodeSocketGeometry
  Group Input:
    location: [-575, 428]
  Quadratic Bezier:
    location: [-577, 289]
    inputs:
      0: 32
      1: [0.0, 0.0, 0.0]
      2: [0.0, 0.0, 0.5]
      3: [0.0, 0.0, 1.0]
  Map Range1:
    location: [-576, -28]
    inputs:
      0: ~Group Input/1
      4: 2.3
  Noise Texture:
    location: [-422, 427]
    noise_dimensions: 4D
    inputs:
      1: 0.2
      2: 1.1
  Curve Tangent:
    location: [-576, -269]
  Math1:
    location: [-409, 150]
    operation: MULTIPLY
    inputs:
      0: ~Map Range1/0
      1: 0.2
  Spline Parameter:
    location: [-407, -27]
  Object Info:
    location: [-402, -129]
    inputs:
      Object: ~Group Input/2
  Math2:
    location: [-257, 427]
    operation: SUBTRACT
    inputs:
      0: ~Noise Texture/1
      1: 0.5
  Map Range2:
    location: [-232, 268]
    inputs:
      0: ~Spline Parameter/0
      To Min: ~Map Range1/0
      To Max: ~Math1
  Math3:
    location: [-230, 12]
    operation: POWER
    inputs:
      0: ~Spline Parameter/0
      1: 2.0
  Set Position:
    location: [-93, 424]
    inputs:
      Geometry: ~Quadratic Bezier
      Offset: ~Math2
  Align Euler to Vector:
    location: [-215, -147]
    axis: Z
    inputs:
      Rotation: ~Object Info/1
      2: ~Curve Tangent
  Resample Curve:
    location: [-64, 254]
    inputs:
      Curve: ~Set Curve Radius
      2: 24
  Math4:
    location: [-67, 79]
    operation: MULTIPLY
    inputs:
      0: ~Math3
      1: ~Group Input/1
  Random Value:
    location: [-63, -93]
    data_type: BOOLEAN
    inputs:
      6: 0.262718
      8: 5
  Trim Curve:
    location: [67, 428]
    color: [0.2706, 0.0627, 0.0627]
    mode: FACTOR
    inputs:
      Curve: ~Set Position
      End: ~Group Input/1
  Instance on Points:
    location: [104, 156]
    color: [0.2706, 0.0627, 0.0627]
    inputs:
      Points: ~Resample Curve
      Selection: ~Random Value/3
      Instance: ~Object Info/3
      Rotation: ~Align Euler to Vector
      Scale: ~Math4
  Set Curve Radius:
    location: [222, 431]
    inputs:
      Curve: ~Trim Curve
      Radius: ~Map Range2/0
  Map Range3:
    location: [101, -63]
    inputs:
      0: ~Group Input/1
      3: -0.6
      4: 0.0
  Curve Circle:
    location: [226, 302]
    inputs:
      0: 8
      4: 0.01
  Combine XYZ:
    location: [273, 75]
    inputs:
      0: 0.0
      Y: ~Map Range3/0
      Z: ~Math5
  Curve to Mesh:
    location: [384, 433]
    inputs:
      Curve: ~Set Curve Radius
      Profile Curve: ~Curve Circle/0
  ID:
    location: [264, -74]
  Math5:
    location: [265, -143]
    operation: MULTIPLY
    inputs:
      0: ~ID
      1: 2.7
  Set Material:
    location: [385, 299]
    inputs:
      Geometry: ~Curve to Mesh
      Material: ~Group Input/3
  Rotate Instances:
    location: [390, 168]
    color: [0.2706, 0.0627, 0.0627]
    inputs:
      Instances: ~Instance on Points
      Rotation: ~Combine XYZ
  Join Geometry:
    location: [422, -68]
    inputs:
      Geometry: ~Rotate Instances;Set Material
  Group Output:
    location: [417, -178]
    inputs:
      Geometry: ~Join Geometry
```

## 補足

下記を使って、名前から「ノード作成時のクラス」を取得しています。

https://qiita.com/SaitoTsutomu/items/1bf451085f55bde21224

以上

