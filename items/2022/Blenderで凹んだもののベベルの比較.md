title: Blenderで凹んだもののベベルの比較
tags: 3DCG Blender ベベル
url: https://qiita.com/SaitoTsutomu/items/a8ab2d4f327f9b5893f7
created_at: 2022-04-16 19:48:44+09:00
updated_at: 2022-04-16 19:57:04+09:00
body:

## 概要

下記のオブジェクトの3通りのベベルの方法の比較です。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/389d9699-9065-e8c8-1001-7f523e1dc397.jpeg" width="260">

## 方法1

下図のようにすべての面を四角面にしてからベベルし、限定的溶解する方法。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/bdac0582-607b-bea9-5939-9ff09854c85f.jpeg" width="260">

<table>
<tr>
<td>
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a502c322-9689-bc04-a71d-01df698d2676.jpeg" width="260">
</td>
<td>
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/da8dbe90-4a9b-6cd1-43dd-e9c3c36f2e44.jpeg" width="260">
</td>
</tr>
</table>

## 方法2

下図のようにL字の面を多角面にしてベベルする方法。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/358d037a-bdf0-92d4-583f-02097fde18b7.jpeg" width="260">

<table>
<tr>
<td>
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/e4498439-5cf1-1c38-6760-5f8b1f000b10.jpeg" width="260">
</td>
<td>
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/ee40e402-7efb-5ff0-f9c9-8d15e582e45b.jpeg" width="260">
</td>
</tr>
</table>

## 方法3

下図のようにL字の面を多角面にして、２段階でベベルする方法。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0d8e13e8-eeae-7d4d-f057-0019c17cb20b.jpeg" width="260">

１段階目は、上記のように選択してベベル。２段階目は、ベベルされなかった部分を選択してベベル。下図の左側は、２段階目直後。

<table>
<tr>
<td>
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/7394157b-efb0-a771-37a3-267a1287461d.jpeg" width="260">
</td>
<td>
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3e8f7a80-4739-a238-ecbd-bb2468f5c44e.jpeg" width="260">
</td>
</tr>
</table>

## ベベルモディファイアーを使う方法

ベベルモディファイアーのジオメトリの留め継ぎ外側とこれらの方法は、下記のように対応します。

| 方法 | 留め継ぎ外側 |
|:-:|:-:|
| 方法１ | バッチ |
| 方法2 | シャープ |
| 方法3 | 弧 |

※ 厳密には、方法３と弧は、微妙に違います。

以上

