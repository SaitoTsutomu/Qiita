title: NiceGUIでリバーシ（オセロ）
tags: Python Webアプリケーション オセロ リバーシ nicegui
url: https://qiita.com/SaitoTsutomu/items/6f45110c614730793779
created_at: 2025-01-14 22:41:27+09:00
updated_at: 2025-02-13 19:31:41+09:00
body:

## はじめに

「＃100日チャレンジ 毎日連続100本アプリを作ったら人生が変わった」を読みました。読みやすく面白かったです。

https://bookplus.nikkei.com/atcl/catalog/24/12/05/01757/

読んでたら、オセロを作りたくなったので作ってみました。

![](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/cb32ffa1-23ff-c5d6-21dd-2d8d60a1c62f.png)

`pip install nicegui-reversi`でインストールして、`reversi`で遊べます。

https://pypi.org/project/nicegui-reversi/

簡単に特徴を紹介します。

## 特徴

* フレームワークはNiceGUI
* 各マスはカスタムGUI部品
* 置けるところを「`・`」で表示
    * 置けるところがないとパスしかできません
    * 両者がパスだと終局します
* 盤面の保存と読込
* 盤面の内部データはNumPyの1次元配列

### フレームワークはNiceGUI

NiceGUIは、PythonでWebアプリケーションやWebAPIを作成するためのフレームワークです。

https://nicegui.io/

ゲームは`Game`クラスで処理します。`__init__`メソッドで画面を作成しています。部品の記述がシンプルです。

```python
from nicegui import app, elements, ui
(中略)

class Game:
    """リバーシゲーム"""

    player: State  # 手番
    board: np.ndarray  # 10*9+1個の1次元配列
    message: str  # 手番や勝敗の表示
    squares: list[Square]  # 64個のマス
    pass_button: elements.button.Button  # PASSボタン
    save_to_storage: bool  # 変更時にゲームの状態を保存するかどうか
    SAVE_FILE: ClassVar[str] = "reversi.toml"  # ファイル名

    def __init__(self, toml: str | None, *, save_to_storage: bool = True):
        self.board = np.zeros(91, dtype=np.int8)
        self.message = ""
        self.save_to_storage = save_to_storage
        ui.label().bind_text(self, "message").classes("text-3xl")
        with ui.grid(columns=8).classes("gap-0 bg-green"):
            self.squares = [Square(self, x + y * 9) for y in range(1, 9) for x in range(1, 9)]
        with ui.row():
            ui.button("reset", on_click=self.reset)
            self.pass_button = ui.button("pass", on_click=self.pass_)
            ui.button("load", on_click=self.load_file)
            ui.button("save", on_click=self.save_file)
        if toml:
            self.from_toml(toml)
        else:
            self.reset()

(中略)

@ui.page("/")
async def top_page():
    """トップページ"""
    await ui.context.client.connected()
    Game(app.storage.tab.get("game"))


def main(*, reload=False, port=8102):  # noqa: D103
    ui.run(title="Reversi", reload=reload, port=port)

```

`app.storage.tab`を使うことで、ブラウザのタブごとに個別にゲームができるようにしています。この`app.storage.tab`を使うには、asyncioでクライアントごとにコネクションを貼る必要があります。
NiceGUIのStorageには次のように5種類のタイプがあり、細かく制御可能です。

https://nicegui.io/documentation/storage

NiceGUIについては、次の記事も参考にしてください。

https://qiita.com/SaitoTsutomu/items/73c5f8b26f2d0238c3fb

### 各マスはカスタムGUI部品

各マスの状態は、`State`クラスあるいは整数です。そして、GUI部品としてのマスは、`Square`クラスです。`Square`クラスでは、状態（`self.game.board[self.index]`）に従って⚫️や⚪️が描画されます。こちらもUI作成がシンプルです。

```python
class State(IntEnum):
    """マスの状態または手番"""

    Empty = 0
    Black = 1
    White = 2
    OK = 3  # 手番で置けるか

    def opponent(self) -> "State":
        """Black <-> White"""
        return State.Black if self == State.White else State.White


class Square(ui.element):
    """GUI部品としてのマス"""

    def __init__(self, game: "Game", index: int):
        super().__init__("div")
        self.game = game
        self.index = index
        classes = "w-9 h-9 text-3xl text-center border border-black cursor-default"
        with self:
            ui.label().bind_text(self, "text").classes(classes).on(
                "click", lambda: game.click(index)
            )

    @property
    def text(self):
        """表示する文字"""
        chars = ["", "⚫️", "⚪️", "・"]
        return chars[self.game.board[self.index]]
```

### 置けるところを「`・`」で表示

`calc_last_and_diff`関数は、`index`に置いたとき、8方向ごとにどれだけひっくり返せるかを返します。`diff`が方向で、`last`が挟むための自分のディスクの位置です。

```python
    @classmethod
    def calc_last_and_diff(
        cls, index: int, player: State, board: np.ndarray
    ) -> Iterable[tuple[int, int]]:
        """indexに置いたとき、8方向ごとにどれだけひっくり返せるか

        :param index: boardの位置
        :param player: 手番
        :param board: 盤面
        :yield: 「挟むための自分のディスクの位置」と方向(差分)
        """
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

`set_ok`関数は、`calc_last_and_diff`関数を使って、置けるところを`State.OK`に設定します。

```python
    @classmethod
    def set_ok(cls, player: State, board: np.ndarray) -> bool:
        """置けるマスを設定し、置けるかを返す"""
        for y, x in product(range(1, 9), range(1, 9)):
            index = x + y * 9
            if not ok_to_empty(board[index]):  # Empty or OK
                can_place = any(cls.calc_last_and_diff(index, player, board))
                board[index] = State.OK if can_place else State.Empty
        return (board == State.OK).any()  # 置けるマスがあるかどうか
```

クラスメソッドにしているのは、相手の手番でも使えるようにするためです。

### 盤面の保存と読込

`Reversi`オブジェクトをサーバーにTOML形式で保存したり読込したりできます。
これにより、任意の場面を簡単に再現できます。
単体テストの`pytest`でも利用しています。

### 盤面の内部データはNumPyの1次元配列

NumPyの多次元配列（`board`）を使うことで処理がシンプルになります。
たとえば、置けるところがあるかどうかは、`(board == State.OK).any()`で判断できます。

## 参考

**本記事のリバーシのリポジトリ**

https://github.com/SaitoTsutomu/nicegui-reversi

**その他の私のNiceGUIのリポジトリ**

https://github.com/SaitoTsutomu?tab=repositories&q=topic%3Anicegui

以上

