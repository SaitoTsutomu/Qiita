title: Blenderのマテリアルノードメモ
tags: 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/f509adeaabd0b8302608
created_at: 2022-12-31 16:59:01+09:00
updated_at: 2023-01-05 18:03:30+09:00
body:

# はじめに

Blenderのマテリアルノードのメモです。Eeveeを対象とします。
適宜更新

### 参考

- https://docs.blender.org/manual/ja/latest/render/shader_nodes/

# Input(入力)
## Ambient Occlusion(アンビエントオクルージョン(AO))

- レンダープロパティのアンビエントオクルージョン（AO)をオンにしないと効かない。
- AOが強調される。ガンマで調整できる。
- AO（出力）は、カラー（出力）の色なし版。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/ca1c924b-4c62-e133-5b5a-557ab70321c3.png)

## Attribute (属性)ノード

- タイプをジオメトリに、名前を`.select_poly`にすると、選択面が白になる。
- タイプをオブジェクトに、名前を`["カスタムプロパティ名"]`にすると、カスタムプロパティの値を取得できる。

### 参考

- 「[Blenderのカスタムプロパティの使い方](https://qiita.com/SaitoTsutomu/items/b6cfd5aeb760d49ea657)」

## Bevel(ベベル)ノード

- ベベルをかける。よくわからない。

## Camera Data (カメラデータ)ノード

- カメラとの距離など。よくわからない。

## カラー属性

- カラーの属性。

## カーブ情報

- カーブの情報。

## Fresnel (フレネル)ノード

- 透過せずに反射するところ。

<table><tr>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/e035479a-0559-e3d7-bcdf-f9233e3137a3.png"></td>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/c7713193-9097-4af5-39f8-c32518578585.png"></td>
</tr></table>

## Geometry (ジオメトリ)ノード

- ジオメトリの情報。
- 下記は裏表でX方向が変わる例。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/26a26425-4078-6e73-ea00-fe65b6d13fbc.png" width="600">

## Layer Weight (レイヤーウェイト) ノード

- よくわからない

## Light Path (ライトパス)ノード

- ライトパスの情報。デフォルトではCyclesのみ。調整をすればEeveeも可。
- 下記は、透明な板を通して黄色になっている。

<table><tr>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/46a5e1e3-ef7c-8937-85ad-8c13714a53c6.png"></td>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3aa74002-2894-0bd3-b737-c82fc6bfed9f.png"></td>
</tr></table>

## Object Info(オブジェクト情報)ノード

- オブジェクトの情報。

### 参考

- 「[Blnderでステンドグラス](https://qiita.com/SaitoTsutomu/items/7acee5298cd25c80a757)」

## Particle Info (パーティクル情報)ノード

- パーティクルの情報。

## Point Info

- よくわからない。

## RGBノード

- RGBを生成。

## Tangent (タンジェント)ノード

- 異方性BSDFのための接線を生成。

## Texture Coordinate (テクスチャ座標)ノード

- 画像テクスチャなどのテクスチャの座標を指定する。Node Wranglerの`Ctrl +T`や`Ctrl + Shift + T`で出てくる。

## UV Map (UVマップ) ノード

- UVマップを指定する。

### 参考

- 「[Blenderで別の画像を重ね合わせる方法](https://qiita.com/SaitoTsutomu/items/5464233bc9dfebd93307)」

## Value(値)ノード

- 値を生成する。
- 変数のように使える（1つの値を複数箇所に反映）。

## Volume Info ノード

- ボリュームの情報。

## Wireframe (ワイヤーフレーム)ノード

- ワイヤーフレームの情報。

### 参考

- 「[Blnderでステンドグラス](https://qiita.com/SaitoTsutomu/items/7acee5298cd25c80a757)」

# Output(出力)

## AOV Output ノード

- よくわからない。

## Material(マテリアル)出力ノード

- 最後に指定するノード。自動生成されそのまま使うことが多い。
- ディスプレイスメントはここにつなぐ。

### 参考

- 「[Blenderで月を作ろう](https://qiita.com/SaitoTsutomu/items/01034a271e7814718937)」

# Shader (シェーダー)

Blender以外のツールなどで、マテリアル出力ノードにプリンシプルBSDFがつながっていると処理してくれるものがあるため、基本的にプリンシプルBSDFを使った方が汎用性が高い。

## Add Shader (シェーダー加算)

- 係数固定のシェーダーミックスか？

## Diffuse BSDF(ディフューズBSDF)

- カラーと粗さとノーマルだけのシェーダー。
- マテリアル出力ノードに接続するならばプリンシプルBSDFを使った方が良い。しかし、セルルック（トゥーンシェーダー）風にしたい場合、シェーダーの出力を使うため、ディフューズBSDFを使うこともある。下記はガンマを設定する例。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/bc5550f3-be5d-aa34-8977-baec322bd3fd.png)

## Emission(放射)

- プリンシプルBSDFの放射と放射の強さを使うべき。
- 発光させる。Eeveeなら、レンダープロパティのブルームをチェックすると発光しているように見える（Cyclesならコンポジターで、グレア）。

## Glass (グラス) BSDF

- プリンシプルBSDFのIORと伝播を使うべき。アルファは1のままで良い。
- ガラスのように透過させる。透明にするには粗さを0にする。Eeveeではスクリーンスペース反射などを設定しないと後ろのものが表示されない。また設定したとしてもうまく表示されないことが多い。

### 参考

- 「[プリンシプルBSDFで宝石の作り方 - Blenderであそんでみた](https://hainarashi.hatenablog.com/entry/2020/09/03/114014)」物質ごとのIORの例。

## Glossy BSDF(光沢BSDF)

- プリンシプルBSDFの粗さを使うべき。
- 粗さを指定できる。

### 参考

- 「[プリンシプルBSDFのスペキュラーについて - Blenderであそんでみた](https://hainarashi.hatenablog.com/entry/2020/09/18/134134)」スペキュラーは、そんなに変えなくても良さそう。

## Holdout(ホールドアウト)

- 透明の色でレンダリングする。
    - 後ろが見える（透ける）のではなく、物体のレンダリング結果のアルファが０になる。

## Mix Shader (シェーダーミックス)

- シェーダーをミックスする。
- Node Wranglerでは、`Ctrl + Shift + 右ドラッグ`で作成できる。

## Principled BSDF(プリンシプルBSDF)

- ベースカラーと粗さとアルファとノーマルをよく使う。たまに、メタリック、IOR、放射。
- サブサーフェスは、人肌みたいな効果（[サブサーフェス・スキャタリング](https://ja.wikipedia.org/wiki/サブサーフェス・スキャタリング)、SSS）がある。
- メタリックは、金属のときに1にする。
- クリアコートは、自動車のワックスの表現に使う。
- テクスチャからノーマルにつなぐには、下記の2種類がある。どちらも、色空間は非カラーにした方が正確。
    - ノーマルテクスチャ：紫っぽい画像。ノーマルマップのカラーにつなぐ。
    - 高さのテクスチャ：グレースケールの画像。バンプの高さにつなぐ。

### 参考

- [各数値の実例](https://docs.blender.org/manual/ja/latest/render/shader_nodes/shader/principled.html#examples)
- 「[プリンシプルBSDFで金属の作り方 - Blenderであそんでみた](https://hainarashi.hatenablog.com/entry/2020/07/11/153838)」金属ごとのカラー。
- 「[プリンシプルBSDFで宝石の作り方 - Blenderであそんでみた](https://hainarashi.hatenablog.com/entry/2020/09/03/114014)」物質ごとのIORの例。

## Principled Volume(プリンシプルボリューム)

- ボリューム用

## Refraction (屈折) BSDF

- グラスBSDFにフレネルをあわせたもの？

## Specular BSDF(スペキュラーBSDF)

- よくわからない。

## Subsurface Scattering(SSS)

- プリンシプルBSDFを使うべき。

## Translucent BSDF(半透明BSDF)

- プリンシプルBSDFを使うべき。

## Transparent BSDF(透過BSDF)

- プリンシプルBSDFを使うべき。

## Volume Absorption(ボリュームの吸収)

- ボリューム用。

## Volume Scatter(ボリュームの散乱)

- ボリューム用。

# Texture(テクスチャ)

## Brick Texture (レンガテクスチャ) ノード

- レンガやビルの窓など。

## Checker Texture (チェッカーテクスチャ) ノード

- 市松模様。

## Environment Texture (環境テクスチャ) ノード

- ワールド用。

## Gradient Texture (グラデーションテクスチャ) ノード

- グラデーション。

## IES Texture (IESテクスチャ) ノード

- IESファイルに基づいた実世界のライト

## Image Texture (画像テクスチャ) ノード

- 画像を指定する。画像自体は別管理される。

## Magic Texture (マジックテクスチャ) ノード

- サイケデリックなカラーテクスチャ

## Musgrave Texture (マスグレイブテクスチャ) ノード

- ノイズ用。
- 下記は金属のサビの例。

<table><tr>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/b3324995-96ab-a2ea-217b-fb4a48020a41.png"></td>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a80890cb-fa76-058c-e9c5-19b2882bb765.png"></td>
</tr></table>

### 参考

- 「[マスグレイブテクスチャを分かりやすく説明してみる／使い方編 - Blenderであそんでみた](https://hainarashi.hatenablog.com/entry/20220212/1644635403)」
- 「[マスグレイブテクスチャを分かりやすく説明してみる／仕組み編 - Blenderであそんでみた](https://hainarashi.hatenablog.com/entry/20220212/1644635408)」

## Noise Texture (ノイズテクスチャ)ノード

- ノイズ用。
- 下記は、[アイスクリーム](https://sketchfab.com/3d-models/ice-cream-5cadf4e715834d1a9b8772591ddd1e63)のコーンの例。

<table><tr>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/47489568-c38b-9ecc-c4d8-0f7c2782441b.png"></td>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/36a75f73-699a-d404-7bec-fd57542723b5.png"></td>
</tr></table>

### 参考

- 「[ノイズテクスチャでいろいろな模様の作り方 - Blenderであそんでみた](https://hainarashi.hatenablog.com/entry/2020/09/07/121022)」

## Point Density (点密度)ノード

- よくわからない。

## Sky Texture (大気テクスチャ)ノード

- ワールドの空の作成用。
- ワールドプロパティで調整する方が見やすい。

## Voronoi Texture (ボロノイテクスチャ)ノード

- ボロノイ図のテクスチャ。石畳や石垣など。
- Dimensionsを4Dにすると、Wを乱数シードのように使える。
- FeatureをN球面半径にすると水玉を作れる。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3ffc93a8-c157-92bf-51e0-c031c3f91112.png)

### 参考

- [各プロパティ](https://docs.blender.org/manual/ja/latest/render/shader_nodes/textures/voronoi.html#properties)

## Wave Texture (波テクスチャ)ノード

- 波のテクスチャ。
- 下記は、[バームクーヘン](https://sketchfab.com/3d-models/baumkuchen-284cedb962b24e76ab4d1bef6ad63f08)の例。

<table><tr>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a7a0a1ae-03d8-1cca-0521-003c75049d5d.png"></td>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/38466e26-4d85-b674-b377-72dc6c6149a0.png"></td>
</tr></table>

## White Noise Texture ノード

- ホワイトノイズは正規乱数で生成することが多いが、一様乱数の気がする。

<table><tr>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a2e65bd6-a2bc-d2f5-596e-cf83e8944a25.png"></td>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/d1ed2dcf-f784-2fd8-0bd6-22b254d779f3.png"></td>
</tr></table>

# Color(カラー)

## Bright/Contrast(輝度/コントラスト)ノード

- 輝度とコントラストを設定。

## Gamma(ガンマ)ノード

- ガンマ補正。

## Hue Saturation Value(HSV(色相/彩度/輝度))ノード

- 色相、彩度、輝度を設定。画像の色合いを変更するのに便利。

## Invert(反転)ノード

- 反転。

## Light Falloff (光の減衰)ノード

- よくわからない。

## Mix(ミックス)ノード

- カラーの合成。合成方法は、いろいろ選べる。
- Node Wranglerでは、`Ctrl + Shift + 右ドラッグ`で作成できる。
- Blender3.4から互換性がないらしい。

## RGB Curves(RGBカーブ)ノード

- RGBカーブの設定。

# Vector(ベクトル)

## Bump (バンプ)ノード

- バンプでノーマルを作成する。
- 高さのテクスチャ（グレースケールの画像）をバンプの高さにつなぐ。

## Displacement (ディスプレイスメント)ノード

- マテリアル出力ノードのディスプレイスメントに接続するためのノード。
- Eeveeではノーマルのせいで効いているように見えるが、Cyclesのみ可能。
- マテリアルの設定のディスプレイスメントで「ディスプレイスメントとバンプ」にすること。
- ノーマルはメッシュを変えずに法線で凸凹を表現するが、ディスプレイスメントはメッシュ自体を変更する。したがって、メッシュの細かさに依存する。ただし、レンダープロパティの機能セットを実験的にし、サブディビジョンサーフェスで適応サブディビジョンにすると、メッシュに依らず細かく反映される（参考「[Blenderで月を作ろう](https://qiita.com/SaitoTsutomu/items/01034a271e7814718937#%E8%A3%9C%E8%B6%B3)」）。

### 参考

- https://docs.blender.org/manual/ja/latest/render/materials/components/displacement.html

## Mapping (マッピング)ノード

- ベクトルの変換。

## Normal(ノーマル)ノード

- ノーマルの方向を変える？

## Normal Map ノード

- ノーマルマップでノーマルを作成する。
- ノーマルテクスチャ（紫っぽい画像）をノーマルマップのカラーにつなぐ。

## Vector Curves(ベクターカーブ)ノード

- ベクトルカーブの設定。

## Vector Displacement (ベクトルディスプレイスメント)ノード

- ベクトルからディスプレイスメント生成。

## Vector Rotate (ベクトル回転)ノード

- ベクトルの回転。

## Vector Transform (ベクトル変換)ノード

- ベクトルの変換。

# Converter (コンバーター)

## Blackbody (黒体)ノード

- 黒い物体の温度の色を生成。

## Clamp (範囲制限)ノード

- 最小と最大の間に変換
    - input <= 最小 → output = 最小
    - 最小 <= input <= 最大 → output = input
    - 最大 <= input → output = 最大

<table><tr>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/71eed894-6438-6c1a-4b2d-6ba783beb227.png"></td>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/45e475e6-a024-71b2-d8bc-928a98aecc27.png" width=150"></td>
</tr></table>

## Color Ramp(カラーランプ)ノード

- スカラーから自在にカラーを生成する。応用範囲が広い。
- 「[Blenderで花火を打ち上げるアドオン](https://qiita.com/SaitoTsutomu/items/9c7aae103bf13d72dd5c)」では、Pythonで生成している。

## Combine Color（カラー合成） ノード

- 個別の属性からカラーを作成。

## Combine XYZ(XYZ合成) ノード

- XYZを合成。

## Float Curve

- スカラーのカーブを設定。

## Map Range(範囲マッピング)ノード

- inputが最小からのとき、outputは最小へ
- inputが最大からのとき、outputは最大へ
- 範囲制限オフでは直線

<table><tr>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/058d4c7d-eb09-3336-052f-fd09b758d398.png"></td>
<td><img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/302556b2-b34a-9538-4779-f7c610b9bf68.png" width=150"></td>
</tr></table>

## Math(数式)ノード

- いろいろな数式で計算。

## Mix(ミックス)ノード

- ベクトルなどの合成。
- Blender3.4から互換性がないらしい。

## RGB to BW(RGBからBWへ)ノード

- カラーをグレースケールに。

## Separate Color（カラー分離） ノード

- カラーを属性に分離。

## Separate XYZ(XYZ分離) ノード

- ベクトルをXYZに分離。

## Shader To RGB (シェーダーからRGBへ)

- シェーダーをカラーに。

## Vector Math (ベクトル演算)ノード

- いろいろなベクトルの演算。

## Wavelength (波長)ノード

- 波長をカラーに。

# マテリアル関連のテクニック

## アルファ

- 画像でアルファを設定して、Cyclesで透過になるのにEeveeでならない場合は、マテリアルの設定のブレンドモードを不透明以外にする。

## 輪郭線

- マテリアルを2つ用意し、2つ目を黒にし設定の裏面を非表示に。モディファイアのソリッド化で、ノーマルを反転、マテリアルのマテリアルインデックスオフセットを1。
- レンダリング時だけでよいなら、レンダープロパティのFreestyleをチェック。

## 画像の重ね合わせ

「[Blenderで別の画像を重ね合わせる方法](https://qiita.com/SaitoTsutomu/items/5464233bc9dfebd93307)」

## ノードの位置調整

「[Blenderでシェーダーのノード位置の調整](https://qiita.com/SaitoTsutomu/items/ae71dd62aa3fa0067c94)」

## 自動ベイク

「[Blenderで自動ベイク](https://qiita.com/SaitoTsutomu/items/f95fcc7b58f22b872bcf)」

以上

