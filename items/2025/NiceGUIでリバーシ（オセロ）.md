title: NiceGUIでリバーシ（オセロ）
tags: Python Webアプリケーション オセロ リバーシ nicegui
url: https://qiita.com/SaitoTsutomu/items/6f45110c614730793779
created_at: 2025-01-14 22:41:27+09:00
updated_at: 2025-01-14 22:41:27+09:00
body:

## はじめに

「＃100日チャレンジ 毎日連続100本アプリを作ったら人生が変わった」を読みました。読みやすく面白かったです。

https://bookplus.nikkei.com/atcl/catalog/24/12/05/01757/

読んでたら、オセロを作りたくなったので作ってみました。

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/cb32ffa1-23ff-c5d6-21dd-2d8d60a1c62f.png)

`pip install nicegui-reversi`でインストールして、`reversi`で遊べます。

https://pypi.org/project/nicegui-reversi/

簡単に紹介します。

## 特徴

* NiceGUIで動きます
* 各マスをGUIの部品にしています
* 置けるところが「`・`」で表示されます
    * 置けるところがないとパスしかできません
    * 両者がパスだと終局します
* 盤面の保存と読込ができます
* 盤面の内部データは、NumPyの1次元配列にしています

### NiceGUIで動きます

NiceGUIは、PythonでWebアプリケーションやWebAPIを作成するためのフレームワークです。

https://nicegui.io/

ゲームは`Reversi`クラスで処理します。`__init__`メソッドで画面を作成しています。簡単ですね。

```python
from nicegui import elements, ui
中略

class Reversi:
    player: State = State.Black
    board: np.ndarray
    message: str = ""
    squares: list[Square]
    pass_button: elements.button.Button
    SAVE_FILE: ClassVar[str] = "reversi.toml"

    def __init__(self):
        with ui.card(align_items="center"):
            ui.label().bind_text(self, "message").classes("text-3xl")
            with ui.grid(columns=8).classes("gap-0 bg-green"):
                self.squares = [Square(self, x + y * 9) for y in range(1, 9) for x in range(1, 9)]
            with ui.row():
                ui.button("Reset", on_click=self.reset)
                self.pass_button = ui.button("Pass", on_click=self.pass_)
                self.pass_button.disable()
                ui.button("Load", on_click=self.load)
                ui.button("Save", on_click=self.save)
    以下略
```

下記の記事も参考にしてください。

https://qiita.com/SaitoTsutomu/items/73c5f8b26f2d0238c3fb

### 各マスをGUIの部品にしています

各マスの状態は、`State`クラスあるいは整数です。そして、GUI部品としてのマスは、`Square`クラスです。`Square`クラスでは、`State`に従って⚫️や⚪️が描画されます。こちらもシンプルです。

```python
class State(IntEnum):
    Empty = 0
    Black = 1
    White = 2
    OK = 3  # 手番で置けるところ

    def opponent(self) -> "State":
        """Black <-> White"""
        return State.Black if self == State.White else State.White


class Square(ui.element):
    chars: ClassVar[list[str]] = ["", "⚫️", "⚪️", "・"]

    def __init__(self, reversi: "Reversi", index: int):
        super().__init__("div")
        self.reversi = reversi
        self.index = index

    def build(self, value: State) -> None:
        self.clear()  # 子要素をクリア
        with self:
            classes = "w-9 h-9 text-3xl text-center border border-black"
            ui.label(self.chars[value]).classes(classes).on("click", lambda: self.reversi.click(self))
```

### 置けるところが「`・`」で表示されます

`calc_last_and_diff`関数は、`index`に置いたとき、8方向ごとにどれだけひっくり返せるかを返します。`diff`が方向で、`last`が挟むための自分のディスクの位置です。

```python
    @classmethod
    def calc_last_and_diff(cls, index: int, player: State, board: np.ndarray) -> Iterator[tuple[int, int]]:
        opponent = player.opponent()
        for diff in [-10, -9, -8, -1, 1, 8, 9, 10]:
            for cnt in range(1, 9):
                last = index + diff * cnt
                value = board[last]
                if value != opponent:
                    if cnt > 1 and value == player:
                        yield last, diff
                    break

```

`check_ok`関数は、`calc_last_and_diff`関数を使って、置けるところを`State.Ok`に設定します。

```python
    @classmethod
    def check_ok(cls, player: State, board: np.ndarray) -> bool:
        """置けるところをチェックし、置けるかを返す"""
        for y in range(1, 9):
            for x in range(1, 9):
                index = x + y * 9
                if not ok_to_empty(board[index]):  # Empty or Ok
                    last_and_diffs = list(cls.calc_last_and_diff(index, player, board))
                    board[index] = State.OK if last_and_diffs else State.Empty
        return (board == State.OK).any()  # 置けるところがあるかどうか
```

### 盤面の保存と読込ができます

`Reversi`オブジェクトをTOMLに保存したり読込したりできます。
これにより、任意の場面を簡単に再現できます。
`pytest`でも利用しています。

### 盤面の内部データは、NumPyの1次元配列にしています

NumPyの多次元配列（`board`）を使うことで処理がシンプルになります。
たとえば、置けるところがあるかどうかは、`(board == State.OK).any()`で判断できます。

## 参考

**リポジトリ**

https://github.com/SaitoTsutomu/nicegui-reversi

**三目並べ**

こちらも部品をクラスにしています。

https://qiita.com/SaitoTsutomu/items/8a22b5e892ae1b7b0a09

以上

