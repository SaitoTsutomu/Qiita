title: Blenderですれすれアニメーション
tags: 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/05bd6dc120bfc73587fa
created_at: 2022-12-11 11:53:15+09:00
updated_at: 2022-12-11 17:20:49+09:00
body:

# これなに

「[Blenderでの繰り返し作業をPythonで効率化する](https://qiita.com/xrxoxcxox/items/314a7f17ae1e6e643a8c)」のアレンジをしてみました。
下記のようなアニメーションが作成できます。

![anim.gif](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/f2ef0743-14a0-9021-17fd-d4fe42e85c89.gif)

[完成物をSketchfabで見る](https://sketchfab.com/3d-models/tight-animation-062c1670fc3142f288fdc9672fcfb75c)

斜めの棒が回転して板の穴をすれすれに通り抜けていきます。

# 手順

Blender3.4で確認していますが、他のバージョンでも動くと思います。Blenderは下記からダウンロードできます。

https://www.blender.org/

以降では日本語環境の画面になっています。日本語の設定は、EditメニューのPreferencesのInterfaceのTranslationを下記のようにします。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/557f5da1-c980-b87f-068f-9b25161798bd.png" width="480">

Blenderの操作方法については、「[Blender Debut! ステップ１:Blenderをはじめよう](https://vook.vc/n/3779)」を参考にしてみてください。

## 棒を作る

最初からあるCube（立方体）は不要なので削除します。Cubeを選択します。マウスカーソルを**3Dビューポート**（中央の一番広いエリア）に置いて、キーの`X`で削除を選びます。

※ Blenderの操作は、マウスカーソルの位置で処理内容が決まります。マウスカーソルが違うところにあると、異なる操作になったり何もおきなかったりするので注意しましょう。

3Dビューポートでキーの`Shift + A`からメッシュの円柱を選びます（追加メニューからもできます）。画面左下の「円柱を追加」をクリックして詳細設定画面を開いて下記のように入力してください。もし、画面が消えてしまったら`F9`で再表示できます。再表示できない場合は、`Ctrl + Z`で戻ってからやり直すといいでしょう。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/a774fd95-6803-19fb-b50a-a141dbecc214.png" width="360">

3Dビューポートで右クリックしてオブジェクトコンテキストメニューからスムーズシェードを選んでください。

画面右下の青いスパナのアイコンをクリックし、モディファイアープロパティを開いてください。モディファイアーを追加からベベルを追加し、下記のように設定してください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/3ce6ffd2-8542-c4a1-3ca6-a6ea96b28bc7.png" width="240">

マウスカーソルを上記画面に置いて`Ctrl + A`を押してください。モディファイアーが適用されて消えます。

青いスパナの１つ上のオレンジの四角のオブジェクトプロパティをクリックし、下記のように設定してください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/494dac31-a54b-a4d3-6e8a-15a998d86b68.png" width="160">

## 棒の軌跡を作る

板の穴をいい感じにくり抜くために、棒の軌跡をオブジェクト化します。
今回のメインの処理です。ちょっと難しいですが頑張りましょう。

最初に、正しい操作か確認しやすくするために、画面右上のビューポートオーバーレイの統計をチェックします。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/c327e516-6ae2-003c-5a43-19acd17e1639.png" width="200">

このようにすると画面左上に選択したオブジェクトなどの情報を確認できます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/db91fc95-0e47-b951-1d37-5c7a29870389.png" width="240">

棒（Cylinder）を選択して`Tab`を押して編集モードに入ります。

`7`を押してください。トップビューになります。下図のように見えるように表示を調整してください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/b5c90d56-7406-4bb3-015e-c64cf7b73e9c.png" width="500">

上図のように選択してみましょう。ちゃんと選択できると選択頂点と選択辺が26個ずつになります。
選択する辺は、垂直の線から時計回りに3つ回ったところです。`Alt`キー（macOSでは`Option`キー）を押しながら、辺をクリックすると半周選択できます。続けて、`Shift + Alt`を押しながらもう半周を選択します。

※ 選択頂点と選択辺が26個ずつになっていれば、多少、選択がずれても大丈夫です。

この選択した頂点と辺を別オブジェクトにします。まず`Shift + D`、`Enter`で複製します（このとき頂点数は412）。続いて`P`、`Enter`で分離の選択をします。この結果、頂点数は386に戻ります。

画面右上のアウトライナーを見てみましょう。Cylinder.001が増えています。これが複製して分離したオブジェクトです。アウトライナーのCylinder.001の左の「・」をクリックしてください。Cylinder.001が編集状態になります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2f6d5b98-8995-4903-cb9e-e072b1e32ccb.png" width="180">


※ 3Dビューポートで`Alt + Q`で編集対象を切り替えることもできます。しかし、今回の場合は、Cylinder.001が重なっているので難しいでしょう。

この状態で棒の先端を含む範囲を右ボタンでドラッグして下記のように選択してください。選択頂点数は13です。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/d90066bf-9a3e-960d-303c-9ff468e7275d.png" width="360">

ひねらないとうまくくり抜けないので、ちょっとひねります。13頂点を選択したまま、`RZZ-110`、`Enter`とします（下図）。
<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/65a2f198-910a-b8b2-c65c-00a2c1d8259c.png" width="300">

`Z`を２回打っているので、ローカル座標で回転します。デフォルトはグローバル座標ですが、グローバル座標で回転すると、選択頂点が棒の表面から離れるので注意してください。

ひねったことで、棒の真ん中付近がくびれてしまいました。真ん中を太くします。辺選択モードにします。棒の中央（オレンジの小さい丸がある場所）が表示されるようにして、中央付近を含むように範囲選択してください、`Shift + Z`で透過表示を切り替えると下図のようになります。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/75fd9b88-c387-92a4-fd74-38616cdb91fc.png" width="240">

右クリックして細分化します。点選択モードに戻し、再度中央付近を範囲選択します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/2137db3b-483f-6bc5-1494-0d88f3607c12.png" width="240">

`S2`、`Enter`で拡大します。`Shift + Z`で透過表示を戻しましょう。`Tab`でオブジェクトモードに戻ります。

ここで、オブジェクトのトランスフォームをリセットします。Cylinder.001を選択した状態で3Dビューポートで`Ctrl + A`（適用）の全トランスフォームを選んでください。オブジェクトの原点（オレンジの小さい丸）がワールドの原点に移動します。

モディファイアープロパティで、スクリューを選び下記のように設定します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/da6b9923-2037-17dc-3fed-94d8ed80b2f2.png" width="180">

## 壁の作成

3Dビューポートで、`Shift + A`のメッシュの平面を選び、下記のようにしてください。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/152497f5-f04c-24da-1504-1151c0c8fd5e.png" width="300">

モディファイアープロパティで、ブーリアンを選び下記のように設定します。オブジェクトには、Cylinder.001を選びます。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/4d0a69f2-fb28-711f-e7ec-99164b24962a.png" width="180">

モディファイアーのところで`Ctrl + A`で適用します。Cylinder.001はもういらないので、`X`で削除しましょう。

## アニメーション

Cylinderを選択した状態で3Dビューポートで`Ctrl + A`（適用）の全トランスフォームを選んでください。
オブジェクトプロパティのトランスフォームの回転Zに、`#frame/10`と入力します。

<img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/6b9ff4de-1a73-d3c5-1e06-727e54c5a299.png" width="180">

上図のように紫色になって、数字表示になります。フレームの1/10を角度Zに設定しています。デフォルトでは、1秒が24フレームになっています。

3Dビューポートでスペースを打つとアニメーションを開始／終了できます。

以上

