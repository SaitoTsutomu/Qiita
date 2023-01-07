title: Blenderファイルの分類方法メモ
tags: Python 3DCG addon Blender
url: https://qiita.com/SaitoTsutomu/items/dd116d1ca1212dcd448e
created_at: 2022-09-05 19:02:49+09:00
updated_at: 2022-09-10 18:21:37+09:00
body:

## 概要

Blenderファイルを特徴別に分類する方法のメモです。macOSで確認しています。Windowsでは、アドオンでos.symlinkを使うため、管理者で実行するか[ユーザーにSeCreateSymbolicLinkPrivilegeの権限を与える](https://kokufu.blogspot.com/2018/03/symbolic-link-privilege-not-held.html)必要があります。

### 要点

- 対象のBlenderのファイルは1つのフォルダに入れる。
- 各Blenderファイルに特徴などの情報をテキストで持たせる。
- テクスチャはパックする。
- 特徴別にツリー状のフォルダ構成でBlenderファイルのシンボリックリンクを管理し、ドリルダウンで絞り込みできるようにする。

## 実現方法

下記の機能を持つ[アドオン](https://github.com/SaitoTsutomu/EditTag)を試しに作ってみました。

- 情報追加（`Add Info`）
- URL表示（`Open URLs`）
- タグ追加（`Add Tag to other`）
- リンクツリー（`Link Tree`）

**アドオンのパネル**

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/de17b252-ff53-20be-0fa2-4fbe0e8f10a5.png" width="300">

### 情報追加（`Add Info`）

ボタンを押すと、下記のような情報を保持するTextオブジェクトを作成します。4行ほどのテキストのエリアをScriptingワークスペースに用意しておくと便利です。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/23d5f730-19d5-6fee-fbcb-ea042d61cf39.png" width="300">

- `url`には、httpで始まるクリップボードの文字列が入ります。
- `date`には実行日が入ります。
- `author`と`tag`は空で作成されるので、適宜編集します。
- `tag`はスペース区切りで複数書けます。

### URL表示（`Open URLs`）

情報の`url`にある全サイトをブラウザで開きます。URLはスペース区切りで複数書けます。

### タグ追加（`Add Tag to other`）

ファイルダイアログが開くので、設定したいファイルを複数選んで[^1]`Add Tag to other`を押すと、それらのファイルの情報の`tag`に`newtag`の内容を追加します。
また、`@`で始まるタグを書くと、`author`に設定します。

[^1]: 現在開いているファイルは選ばないでください。

### リンクツリー（`Link Tree`）

`input`にある全Blenderファイルを分類してリンクツリーというものを作ります。作成場所は、`input`の1つ上の`link_tree`です。

たとえば、`test.blend`の`tag`が、`food lowpoly asset`のときは、`link_tree`以下は下記の構成になります。

```
─ etc ┬ asset ┬ test.blend
      │       ├ food ┬ test.blend
      │       │      └ lowpoly ─ test.bend
      │       └ lowpoly ┬ test.blend
      │                 └ food ─ test.blend
      ├ food ┬ test.bend
      │      ├ asset ┬ test.blend
      │      │       └ lowpoly ─ test.bend
      │      └ lowpoly ┬ test.blend
      │                └ asset ─ test.blend
      └ lowpoly ┬ test.bend
                ├ asset ┬ test.blend
                │       └ food ─ test.bend
                └ food ┬ test.blend
                       └ asset ─ test.blend
```

- 最上位にetcフォルダがあります。
- etcの中は、各tagのフォルダがあります。
- etc/assetの中に、test.blendがあります。このファイルがassetというtagを持つからです。
- 複数のtagがあると、フォルダがネストしていきます。ネストはtagの全順列が現れます。ネストしているので、tagで絞り込みできます。
- 15個のtest.blendは、シンボリックリンクです。

### 設定ファイルなど

tag情報などは、`input`の1つ上の`.link_tree.cache`にTOML形式でキャッシュします。
また、`input`の1つ上の`.link_tree.setting`に下記の設定を記述できます。
- first_set：etcの1つ上に移動させるものを指定します。first_onlyも対象です。
- first_only：最上位以外のフォルダを作成しません。

### その他

- ファイルにアニメーションがあると、`anim`というtagが自動で付加されます。
- ファイルにリグがあると、`rig`というtagが自動で付加されます。
- `author`を指定していると、最上位に`author`というフォルダが作成され、その中の`author`の値のフォルダにも入ります。

### 補足

ファイル名をtest_asset_food_lowpoly.blendにすれば、ダイアログで絞り込みできます。しかし、今回の方法だと、絞り込み時にタグの可視化ができたり、タグ以外の情報の管理もできるようになります。

以上

