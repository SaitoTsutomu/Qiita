title: Blender 3.5/3.6で、addonにTestingを復活させる方法
tags: Python addon Blender
url: https://qiita.com/SaitoTsutomu/items/5872c5e0358394360697
created_at: 2023-05-28 10:47:52+09:00
updated_at: 2023-07-30 21:04:18+09:00
body:

Blender 3.4まで表示されていたのに 3.5あるいは3.6になったらaddonにTestingが表示されなくなっていました。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/e84975f7-0b0a-f952-a47d-5c4d46b507ee.png)

下記などで議論されていますが、仕様のようです。

https://projects.blender.org/blender/blender/issues/106306

ところで、Blender 3.4まで導入していたTestingのaddonは使えますが、無効化など制御不能になっています。困りました。
調べたところ、下記に解決策がありました。

https://blenderartists.org/t/blender-3-5-and-addons-folder/1457584/11

Blenderのコードを直接編集する方法です。
macOSの例だと、下記のようになります。

```python:/Applications/Blender.app/Contents/Resources/3.5/scripts/startup/bl_ui/__init__.pyの149行目
-    if bpy.app.version_cycle == "alpha":
+    if bpy.app.version_cycle == "release":
```

起動し直すと、復活できました。

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/30f1fbd1-21ee-2c8b-2bc5-24ae12be8bf7.png)

修正は自己責任でお願いします。

以上

