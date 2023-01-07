title: SketchfabとUSDZとBlender
tags: Blender USD Sketchfab
url: https://qiita.com/SaitoTsutomu/items/3f87015123244bcc353a
created_at: 2022-11-12 16:22:14+09:00
updated_at: 2022-12-03 07:00:50+09:00
body:

# SketchfabとUSDZとBlender

SketchfabとUSDZとBlenderについての簡単な紹介です。

## Sketchfabとは

[Sketchfab](https://sketchfab.com/)は、3Dコンテンツの公開、共有、売買ができるプラットフォームです。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/d5d30028-9b63-4782-b465-7f35e804def3.png" width="500">



Sketchfabでは、`blend`など[いろいろなフォーマットでファイルをアップロードできます](https://help.sketchfab.com/hc/en-us/articles/202508396-3D-File-Formats)。
アップロードしたファイルは、[可能な限り`glTF`と`USDZ`に変換されます](https://help.sketchfab.com/hc/en-us/articles/360046421631-glTF-GLB-and-USDZ)。

下記は、`blend`のファイルをアップロードした場合のダウンロード画面です。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/051a202c-4321-ff27-d05c-01bba19d1243.png" width="400">

オリジナルの`blend`に加え、`USDZ`、`glTF`、`GLB`でダウンロード可能です。
`blend`ファイルは、`glTF`に変換され、`glTF`から`USDZ`に変換されます。`GLB`は、`glTF`のバイナリ版です。

## USDZとは

`USDZ`は、`usdc`をzipで圧縮したファイルです。
`USDZ`は、[いくつかの制限があります](https://help.sketchfab.com/hc/en-us/articles/360046421631-glTF-GLB-and-USDZ#usdz-limitations)。たとえば、アーマチュアや特定のアニメーションはデータに含まれません。

多くの場合、USDZのファイルはスリム（サイズが小さい）です。

## BlenderでUSDZを読み込む方法

Blenderは、（ブレンダー）は オープンソースの統合3DCGソフトウェアです。
3Dモデルの作成だけでなく、スカルプト、アニメーション、物理シミュレーション、合成、動画編集など多くの機能があります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a177700d-533f-19d5-1300-a52ed03365da.jpeg" width="500">

BlenderではUniversal Scene Description形式のファイル（usd, usdc, usda）のインポート／エクスポートができますが、拡張子がusdzのファイルは対応していないようです。

なぜ、対応していないのかわかりませんが、次のようにすると読み込むことができます。

- 拡張子をzipに変更
- zipを解凍
- 解凍したusdcをインポート

また、Blenderにはアドオンという機能拡張のしくみがあります。直接usdzをインポート可能なアドオンも存在するようです。

## まとめ

Sketchfabでは、USDZでサイズの小さいファイルをダウンロードできます。USDZは、ひと手間かけるとBlenderで読み込むことができます。

