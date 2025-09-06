title: BlenderのノードをPythonコードに変換！「Node To Python」アドオンの使い方
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/4c95679d416c2dec7214
created_at: 2025-09-02 22:41:53+09:00
updated_at: 2025-09-02 22:41:53+09:00
body:

## はじめに

[Blender](https://www.blender.org/)には、**ジオメトリノード**、**シェーダーノード**、**コンポジットノード**といった強力なノードベースの機能が備わっています。

これらは通常、GUIで直感的に作成し、`.blend`ファイル内に保存します。そのため、ノードの共有は`.blend`ファイルごと行うのが一般的です。
しかし、**テキストベースでノードを扱いたい**場合、例えばGitでバージョン管理をしたり、ドキュメントにコードとして埋め込んだりするには、少し工夫が必要でした。

この課題を解決してくれるのが、今回ご紹介する **Node To Python** アドオンです。

![image.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/5e5a04af-fd5c-4adf-a40a-55dab8db8bb1.jpeg)

---

## Node To Python とは？

Node To Pythonは、その名の通り、Blenderの各種ノードを**Pythonコードに変換**してくれる便利なアドオンです。

変換されたPythonコードはテキストファイルなので、次のような場面で非常に役立ちます。

* **Gitでのバージョン管理**: 変更履歴を追いやすくなります。
* **ドキュメントやブログ記事への埋め込み**: 手順をコードで明確に示せます。
* **他のスクリプトやアドオンからの再利用**: ノード設定をプログラムで呼び出せます。

関心を持った方は、以下の公式ページから入手できます。
👉 **公式ダウンロードページ:** [Node To Python - Blender Extensions](https://extensions.blender.org/add-ons/node-to-python/)

---

## インストール方法

Blender内で直接インストールできるため、手順はとても簡単です。

1.  メニューから **[編集] > [プリファレンス]** を開きます。
2.  **「エクステンションを入手」** (Get Extensions) タブを選択します。
3.  検索バーに `node to python` と入力します。
4.  検索結果に表示された「Node To Python」のインストールボタンをクリックします。

インストールが完了すると、アドオンは自動的に有効化されます。

---

## 使い方

アドオンの操作は、各ノードエディタの**サイドバー**（ショートカットキー: `N`）から行います。
サイドバーに新しく追加された **「Node To Python」** タブを開いてください。

![image.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/5dfdd6fa-fd2a-4b64-91b7-2c0166b85f57.jpeg)

### ジオメトリノード
1.  **「Geometry Nodes to Python」** セクションにある「**ジオメトリーノード**」ボタンをクリックします。
2.  ファイル内に存在するジオメトリノードの一覧が表示されます。
3.  変換したいノードを選択すると、対応するPythonコードが**自動的にクリップボードへコピー**されます。

### シェーダーノード
1.  **「Material to Python」** セクションにある「**マテリアル**」ボタンをクリックします。
2.  既存のマテリアル（シェーダーノード）の一覧が表示されます。
3.  対象のノードを選択すると、同様にコードがクリップボードにコピーされます。

### コンポジットノード
1.  **「Compositor to Python」** セクションにある「**Scene Compositor Nodes**」ボタンをクリックします。
2.  シーンに設定されたコンポジットノードがPythonコードに変換され、クリップボードにコピーされます。

---

## 出力されるコードの例

例えば、シェーダーノードからは、次のようなPythonコードが生成されます。このコードを実行すれば、GUIで作成したものと全く同じノード構成をスクリプトから再現できます。

```python
import bpy, mathutils

#initialize geometry_nodes node group
def geometry_nodes_node_group():
    geometry_nodes = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Geometry Nodes")
    ...
    以下略
```

## まとめ

* Blenderのノードは通常.blendファイルで共有しますが、テキストとして扱いたい場面も多くあります
* Node To Pythonアドオンを使えば、ノードを簡単にPythonコードに変換できます
* サイドバーから、ジオメトリ、シェーダー、コンポジットの各ノードに対応しています
* 生成されたコードは、Gitでのバージョン管理やドキュメント化に非常に便利です

Blenderのノードをより効率的に管理・共有したい方は、ぜひこのアドオンを試してみてください。

