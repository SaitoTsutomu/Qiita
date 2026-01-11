title: MacのJupyterLab + Python-MIPでHiGHSを使う方法
tags: Python Jupyter python-mip HighS taskipy
url: https://qiita.com/SaitoTsutomu/items/60ddf4a72137d715e775
created_at: 2025-12-31 15:04:12+09:00
updated_at: 2025-12-31 15:36:08+09:00
body:

本記事では、macOS上でJupyterLabを使い、Python-MIPによる数理最適化モデルを**HiGHS ソルバー**で実行するための、手順を説明します。

## 想定環境と前提

- **macOS + Homebrew**
  - HiGHSを簡単にインストールするため
- **Python 3.12以上**
  - 3.12非対応のPython-MIPへの対処法の説明のため
- **uv**
  - 仮想環境管理と`.env`ファイル読み込みを簡潔にするため
- **taskipy（任意）**
  - 環境変数付きでJupyterLabを短いコマンドで起動するため

※ taskipyは必須ではありません。利便性のために使用します。

## Python-MIPのバージョン選択について

- **安定版**: `1.15.0`（2023年1月4日リリース）
  - Python 3.11まで対応
- **Release Candidate**: `1.16rc0`（2024年2月18日リリース）
  - Python 3.12 / 3.13 / 3.14に対応
  - 本記事ではこちらを使用

Python 3.12以降では、`1.16rc0`を使うのが簡単です。

Python-MIPはCBCソルバーが同梱されていますが、HiGHSは同梱されていません。
そのため、別途HiGHSを用意し、Python-MIPに場所を教える必要があります。

## 手順概要

1. uvでPython仮想環境の作成
2. Python-MIPとJupyterLabのインストール
3. HomebrewでHiGHSのインストール
4. 環境変数`PMIP_HIGHS_LIBRARY`の設定
5. taskipy（任意）の設定
6. JupyterLabで動作確認

## 1. uvでPython仮想環境の作成

```sh
uv init sample -p 3.12
cd sample
```

※ Python 3.13や3.14でも同様に動作します。

## 2. Python-MIPとJupyterLabのインストール

```sh
uv add "mip[numpy]==1.16rc0" jupyter
```

- `numpy`は多くの最適化モデルで必要になるためextras指定

## 3. HomebrewでHiGHSのインストール

```sh
brew install highs
```

インストール後、以下で実行ファイルの場所を確認できます。

```sh
which highs
```

出力例:

```output
/opt/homebrew/bin/highs
```

## 4. 環境変数`PMIP_HIGHS_LIBRARY`の設定

Python-MIPは、HiGHSを呼び出す際に環境変数を参照します。変数名は`PMIP_HIGHS_LIBRARY`ですが、指定すべきパスは共有ライブラリ（`.dylib`や`.so`）ではなく、Homebrewでインストールしたhighs実行ファイルです。

```sh
echo PMIP_HIGHS_LIBRARY=$(which highs) > .env
```

`.env`ファイルは以下の形式になります。

```file
# .env
PMIP_HIGHS_LIBRARY=/opt/homebrew/bin/highs
```

## 5. taskipy（任意）の設定

taskipyは`uv tool install taskipy`でインストールできます。taskipyをインストールするとtaskコマンドが使えます。taskコマンドは、`pyproject.toml`に登録します。
本記事では、`.env`を読み込んだ状態でJupyterLabを起動するため、`jupyter`というtaskコマンドを追加します。

```sh
echo '[tool.taskipy.tasks]\njupyter = "uv run --env-file .env jupyter lab -y"' >> pyproject.toml
```

### `-y`オプションについて

taskipy経由で起動すると、JupyterLabの仕様上、Ctrl+CでJupyterLabが終了しません。
`-y`を付けることで、**1回の Ctrl+Cで終了**できるようになります。

### JupyterLab起動

```sh
task jupyter
```

taskipyを使わない場合は以下のようにします。

```sh
uv run --env-file .env jupyter lab
```

## 6. JupyterLabで動作確認

以下のコードをJupyterLabで実行してください。
**HiGHS が使われていれば、標準出力にHiGHSのバージョンが表示されます**。

```python
import numpy as np
from mip import HIGHS, Model, minimize, xsum

rng = np.random.default_rng(0)
nw = 3  # 倉庫数
nf = 4  # 工場数

供給 = rng.integers(30, 50, nw)
需要 = rng.integers(20, 40, nf)
輸送費 = rng.integers(10, 20, (nw, nf))

m = Model(solver_name=HIGHS)
x = m.add_var_tensor((nw, nf), name="x")

m.objective = minimize(
    xsum(輸送費[i, j] * x[i, j] for i in range(nw) for j in range(nf))
)

for i in range(nw):
    m += xsum(x[i, :]) <= 供給[i]

for j in range(nf):
    m += xsum(x[:, j]) >= 需要[j]

m.optimize()
x.astype(float)
```

## まとめ

- Python 3.12以降ではPython-MIP **1.16rc0**を使用
- HiGHSをHomebrewで別途用意
- `PMIP_HIGHS_LIBRARY`にHiGHSの実行ファイルのパスを指定
- uv + `.env`により、再現性の高い環境構築が可能

Python 3.12以降の環境でPython-MIP + HiGHSを使う構成として活用してください。

