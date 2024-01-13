title: BlenderのPythonにおけるアクティブオブジェクトについて
tags: Python 3DCG Blender
url: https://qiita.com/SaitoTsutomu/items/eb859dc41b7f585252cd
created_at: 2024-01-02 18:16:03+09:00
updated_at: 2024-01-02 19:14:39+09:00
body:

## アクティブオブジェクとは

Blenderのアクティブオブジェクトは、処理対象あるいは処理結果のオブジェクトです。
Pythonでは、現在のコンテキスト（`bpy.context`）を使って、通常、下記の3通りの方法で取得できます。

| コード                                | 意味                       |
| :------------------------------------ | :------------------------- |
| bpy.context.active_object             | アクティブオブジェクト     |
| bpy.context.object                    | コンテキストのオブジェクト |
| bpy.context.view_layer.objects.active | アクティブオブジェクト     |

ここでは、この3つの違いを紹介します。

## 準備

Blenderを起動して、立方体（Cube）とUV球（Sphere）を作成し、Sphereを選択してください。
ワークスペースをScriptingにして、右下のプロパティ画面を「オブジェクトプロパティ」（オレンジの四角）にして、右上のピンをチェックしてください。
ピン止めすると、選択を変えてもプロパティ画面の対象のオブジェクトが固定されます。

![a](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/0e564f8d-e008-91bb-a65e-0a93c62e132b.jpeg)


## アクティブオブジェクトの設定

`context`をコンテキストとします。
アクティブオブジェクトを設定するには、`context.view_layer.objects.active`を使います。
他の方法では設定できません。下記で確認できます。

```python
import bpy

obj = bpy.data.objects["Cube"]

context = bpy.context
# アクティブオブジェクトの設定
context.view_layer.objects.active = obj

# 失敗することを確認
try:
    context.active_object = obj
except AttributeError as e:
    print(e)

try:
    context.object = obj
except AttributeError as e:
    print(e)
```

**出力**

```
bpy_struct: Context property "active_object" is read-only
bpy_struct: Context property "object" is read-only
```


出力から、`active_object`と`object`が、read-onlyということがわかります。
`context.view_layer.objects.active`はエラーになっていないので、アクティブオブジェクトはCubeになっています。

## コンテキストを変えて確認

厳密に言うと、`context.object`はコンテキストのオブジェクトです。コンテキストはパネルなどの画面ごとに異なるので、特殊な場合に`context.object`はアクティブオブジェクトではありません。
下記を実行して確認してみましょう。下記では一時的にコンテキストを変更しています。

```python
import bpy

# プロパティ画面の取得
area = [area for area in bpy.context.screen.areas if area.ui_type == "PROPERTIES"][0]
# プロパティ画面での3通りの方法の確認
with bpy.context.temp_override(area=area):
    context = bpy.context
    print(f"{context.active_object = }")
    print(f"{context.object = }")
    print(f"{context.view_layer.objects.active = }")
```

**出力**

```
context.active_object = bpy.data.objects['Cube']
context.object = bpy.data.objects['Sphere']
context.view_layer.objects.active = bpy.data.objects['Cube']
```

アクティブオブジェクトはCubeですが、`context.object`はSphereです。
理由は、`context`が、プロパティ画面のコンテキストだからです。
プロパティ画面は、準備でSphereをピン止めしたので、コンテキストのオブジェクトがSphereになっています。
Sphereはアクティブオブジェクトではありませんが、コンテキストのオブジェクトなのでこのようになります。

アドオン開発では、`bpy.context`ではなく、メソッドの引数である`context`を使うことが推奨されています。そして、`context`を使うと`context.object`がアクティブオブジェクトでない可能性があります。したがってアクティブオブジェクトを取得するには、`context.active_object`を使うのが無難です。

## まとめ

`context`を現在のコンテキストとします。

- アクティブオブジェクトの取得は、`context.active_object`を使う。
- アクティブオブジェクトの設定は、`context.view_layer.objects.active`を使う。

## 参考

https://blender.stackexchange.com/questions/204074/python-bpy-context-object-vs-bpy-context-active-object

以上

