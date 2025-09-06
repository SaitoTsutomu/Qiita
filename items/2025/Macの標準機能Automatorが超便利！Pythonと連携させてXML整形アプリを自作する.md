title: Macの標準機能Automatorが超便利！Pythonと連携させてXML整形アプリを自作する
tags: Python ShellScript Mac XML Automator
url: https://qiita.com/SaitoTsutomu/items/30cd85cff5b2b56ce5b7
created_at: 2025-08-21 18:34:24+09:00
updated_at: 2025-08-21 18:34:24+09:00
body:

## はじめに

XMLファイルの差分を確認する必要が出てきたものの、いざVS Codeの比較機能（`code -d 1.xml 2.xml`）を使ってみると、ファイルが一行にまとまっていて、どこが違うのかさっぱり分からない…。

こんな経験はありませんか？

この問題を解決するのが、XMLを人間が読みやすいようにインデントや改行を加えて整形する「**プリティプリント**」です。

本記事では、**XMLファイルをドラッグ＆ドロップするだけで、簡単にプリティプリントできるMac用ツールを作成する方法**を紹介します。

**整形のイメージ**

```
整形前:                整形後:
<root><a>1</a>...      <root>
                          <a>1</a>
                          <b>2</b>
                       </root>
```

**対象読者**

* XMLファイルの中身を見やすくしたい方
* Macで簡単な自作ツールに挑戦してみたい方

**前提知識**

* ターミナルの基本的な使い方
* Pythonスクリプトを実行した経験
* uv（Pythonの高速なパッケージ管理・実行ツール）の基本的な使い方

## ツールの作成

Macに標準でインストールされている`Automator.app`を使えば、ドラッグ＆ドロップで動作するツールを驚くほど簡単に作成できます。

1. **Automatorを起動する**
   `アプリケーション`フォルダから`Automator.app`を探して開きます。書類の種類を聞かれたら「**アプリケーション**」を選択してください

2. **アクションを追加する**
   下図のように、左のアクション一覧から「**シェルスクリプトを実行**」を探し、右のワークフローエリアへドラッグ＆ドロップします

    <img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/13261383-0ba1-4b7e-9a5a-48bdb6e40fc0.jpeg" width="700px">

3. **パラメーターを設定する**
   追加したアクションの右上で、以下の2点を設定します
    * シェル：`/bin/zsh`（デフォルトのままでOK）
    * 入力の引き渡し方法：**`引数として`**
    ※この設定が、ドラッグ＆ドロップしたファイルの情報をスクリプトに渡すための重要なポイントです。

4. **スクリプトを記述する**
   テキストエリアに、以下のシェルスクリプトを貼り付けます。

   ```shell
   # Pythonスクリプトを実行し、結果（標準出力/エラー）をRES変数に格納
   RES=$(uv run --with lxml ~/tools/XmlPrettyPrint.py $* 2>&1)
   
   # 実行結果をダイアログで表示
   osascript -e "display dialog \"${RES}\" with title \"確認\" buttons {\"OK\"}"
   ```

   このスクリプトは、ドロップされたファイルパス（`$*`）を引数としてPythonスクリプトを呼び出し、その実行結果をMacのダイアログで表示する、というシンプルな処理です。実際の整形処理は次のステップで作成するPythonに任せます。

5. **アプリケーションを保存する**
  メニューから「ファイル」>「保存」を選びます。名前を「`XmlPrettyPrint.app`」など分かりやすいものにして、普段アクセスしやすいアプリケーションフォルダなどに保存しましょう。

## Pythonスクリプトの実装

次に、XMLを整形する心臓部となるPythonスクリプトを作成します。

`~/tools/XmlPrettyPrint.py`というパスで、以下の内容のファイルを作成してください。（`~/tools`の部分はご自身の好きなディレクトリで構いませんが、その場合はAutomatorのスクリプトパスも合わせて変更してください。）

```python
import sys
from lxml import etree

if len(sys.argv) <= 1:
    print("XMLファイルをドラッグしてください")
    sys.exit(0)

in_file = sys.argv[1]
out_file = f"{in_file[:-4]}_pretty.xml"
tree = etree.parse(in_file, etree.XMLParser())
tree.write(
    out_file,
    pretty_print=True,
    xml_declaration=True,
    encoding="utf-8",
)
print(f"{out_file}を出力しました")
```

このスクリプトは、渡されたXMLファイルを`lxml`ライブラリで読み込み、`pretty_print=True`オプションを付けて書き出すことで整形を実現しています。

## 使い方

使い方は簡単です。

作成した`XmlPrettyPrint.app`のアイコンに、整形したいXMLファイルをドラッグ＆ドロップするだけです。

処理が完了するとダイアログが表示され、元のファイルと同じ場所に`*_pretty.xml`という名前で整形済みのファイルが出力されます。

## 最後に

今回はAutomatorとPythonを組み合わせて、日々の作業を少しだけ効率化するツールを作成しました。これで一行に圧縮されたXMLファイルも、整形してから比較すれば、VS Codeでの差分確認が格段にはかどります。

このように、普段の「ちょっと不便だな」をプログラミングで解決するのは、とても楽しいものです。ぜひ、皆さんも自分だけの便利ツール作りに挑戦してみてください。

