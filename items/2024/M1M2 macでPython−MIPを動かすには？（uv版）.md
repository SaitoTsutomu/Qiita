title: M1/M2 macでPython−MIPを動かすには？（uv版）
tags: Python Mac UV 最適化 python-mip
url: https://qiita.com/SaitoTsutomu/items/9dab25767e0df7cbd8a0
created_at: 2024-09-03 19:10:03+09:00
updated_at: 2024-09-04 12:17:29+09:00
body:

この記事は、次の2記事の続編です。M1/M2 macでPython−MIPを動かす方法を説明します。

https://qiita.com/SaitoTsutomu/items/fbc33299e1906a238f53

https://qiita.com/SaitoTsutomu/items/aabb94db3f20cce3dc82

Python−MIPに付属するソルバーCBCは、x86_64用であるため、そのままでは動きません。
また、Python-MIPはCFFIでソルバーを動かすため、Python自身がx86_64上で動く必要があります。

ここでは、uvを使って動かす方法を紹介します。

https://github.com/astral-sh/uv

## 準備

Rosetta2とuvが必要です。
Rosetta2を有効にするには、一度だけ次のようにします。

```zsh
/usr/sbin/softwareupdate --install-rosetta --agree-to-license
```

macOSやLinuxでuvをインストールするには、次のようにします。

```zsh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

さらに、次のようにコマンドの補完設定用のファイルを作成します。
※ zshを想定しています。

```zsh
~/.cargo/bin/uv generate-shell-completion zsh > ~/.uv_completion.sh
```

uvを使うために次を`~/.zprofile`に追加し、`source ~/.zprofile`としてください。

```zsh
source $HOME/.cargo/env
source $HOME/.uv_completion.sh
```

## X86_64用Pythonのインストール

次のようにすると、インストール可能なPythonのバージョンを確認できます。

```zsh
uv python list --all-platforms
```

`macos-x86_64`を含むものを探してください。今回は、次のように`cpython-3.12.5-macos-x86_64-none`を使います。

```zsh
uv python install cpython-3.12.5-macos-x86_64-none
```

## 仮想環境の構築

次のようにして、新しいプロジェクトを作成して仮想環境を構築しましょう。

```zsh
uv init mip-sample
cd mip-sample
uv python pin cpython-3.12.5-macos-x86_64-none
```

`.python-version`というファイルが作成され、`pin`で指定したバージョンが入ります。

※ `warning: No interpreter found for cpython-3.12.5-macos-x86_64-none in managed installations or system path`と出ますが、使えるようです。

次のようにして、Python-MIPをインストールします。

```zsh
uv add mip
```

## サンプルの実行

カレントディレクトリの`hello.py`を次のように修正してみましょう。

```python
from mip import Model, maximize, minimize, xsum

m = Model()  # 数理モデル
# 変数
x = m.add_var("x")
y = m.add_var("y")
# 目的関数
m.objective = maximize(100 * x + 100 * y)
# 制約条件
m += x + 2 * y <= 16  # 材料Aの上限
m += 3 * x + y <= 18  # 材料Bの上限
m.optimize()  # ソルバーの実行
print(x.x, y.x)  # 4.0 6.0
```

次を実行してCBCが動くことを確認できます。

```zsh
uv run hello.py
```

uvの詳細については、ドキュメントを参考にしてください。

https://docs.astral.sh/uv/

## まとめ

* arm64アーキテクチャでも、uvを使うことで`x86_64`のPythonやパッケージをインストールして実行できる

以上

