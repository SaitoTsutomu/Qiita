title: Blender 4.2のアドオン事情
tags: addon Blender extension
url: https://qiita.com/SaitoTsutomu/items/20ce443d0b0675716705
created_at: 2024-06-23 16:08:02+09:00
updated_at: 2024-07-17 22:12:40+09:00
body:

# Blender 4.2のアドオンについて

2024/07/16リリースのBlender 4.2 LTSからアドオン周りが変わるようです。

https://code.blender.org/2024/05/extensions-platform-beta-release/

実際に確認してみた結果を紹介します。

## エクステンション

4.2では、**エクステンション**という機能でサイト上のアドオンやテーマをインストールできるようになります。

https://extensions.blender.org/

エクステンション（Extensions）は、プリファレンスから使うことができます。
実際に使うには、オンラインアクセスを許可する必要があります。

![スクリーンショット 2024-07-17 6.41.11.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/06172f8b-b487-f8fd-6310-ce50b0fa982e.png)

以下は日本語表示です。「オンラインアクセスを許可」を押すと使えるようになります。
なお、「オンラインアクセスを許可」を押したあとに戻したい場合は、システムタブのネットワークの「オンラインアクセスを許可」をオフにします。

![スクリーンショット 2024-07-17 6.41.45.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/02e1a66b-05e6-040b-1e17-6651a1201b0c.png)

エクステンションをインストールするには、検索で絞り込んで「Install」を押します。あるいは、下記のようにドラッグ＆ドロップでもインストールできます。

https://extensions.blender.org/about/

## 従来のアドオン

従来のアドオンも引き続き使えました。

![スクリーンショット 2024-07-17 6.42.22.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a26ecc0f-b96e-8677-3ca7-ee01846805b9.png)

- 4.1で有効にしていた公式アドオンのいくつかは「ビルトインアドオンが行方不明」になっていました。行方不明になったアドオンは、手動で再インストールが必要なようです
- アドオンをファイルからインストールするには、右上の「`v`」の「ディスクからインストール…」で可能です
- 4.1で表示されていた「公式、コミュニティ」などのカテゴリはなくなっています。そのかわり「Testing」のアドオンも表示されるようになっています。公式のものはBlenderのアイコンに、コミュニティのものは人のアイコンに、以前のバージョンから引き継いだものはフォルダのアイコンのようです
- 参考までに、4.1のアドオンは下記のようになっています

**4.1のアドオンの画面**

![スクリーンショット 2024-06-23 15.27.37.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0e842626-5420-2ca8-2549-e66807c1f5fb.png)

## エクステンションの作り方

エクステンションの作り方は下記を参照してください。

https://docs.blender.org/manual/ja/4.2/extensions/getting_started.html

エクステンションでは、`blender_manifest.toml`が必要です。
`blender_manifest.toml`の書き方については、下記を参照してください

https://docs.blender.org/manual/ja/4.2/extensions/getting_started.html#manifest

また、`blender_manifest.toml`があると、たとえば、下記のようにしてエクステンションの要件を満たしているか確認できます。

```
blender --command extension validate ZIPファイル
```

自作のエクステンションを公式サイトにアップロードできるようです（下記は**ログインが必要**です）。

https://extensions.blender.org/submit/

ただし、公開されるためには審査が必要なようです。詳しくは、上記リンク先のguidelinesやterms of serviceを確認してください（ライセンスを下記から選ぶことなどが書いてあります）。

https://docs.blender.org/manual/ja/4.2/extensions/licenses.html

## アドオンとエクステンションに必要なもの

アドオンからインストール、あるいは、エクステンションからインストールするのに必要なものは、下記のようです。

|  | bl_info（辞書） | blender_manifest.toml（ファイル） |
|:-:|:-:|:-:|
| アドオンに必要なもの | ◯ | ― |
| エクステンションに必要なもの | ― | ◯ |

※ bl_infoとblender_manifest.tomlがあるとどちらからもインストールできました。

## インストール先

アドオンとエクステンションではインストール先が違います。下記はディスクからインストールしたときのmacOSの例です。

* アドオン：`~/Library/Application Support/Blender/4.2/scripts/addons/`
* エクステンション：`~/Library/Application Support/Blender/4.2/extensions/`

## まとめ

* Blender 4.2ではエクステンションという機能により、Blender上からアドオンを検索してインストールが可能
* エクステンション用のアドオン作成では`blender_manifest.toml`が必要
* 従来のアドオンも引き続き使用可能

以上

