title: NiceGUIで三目並べ
tags: Python Webアプリケーション nicegui
url: https://qiita.com/SaitoTsutomu/items/8a22b5e892ae1b7b0a09
created_at: 2024-11-13 21:16:55+09:00
updated_at: 2024-11-13 21:16:55+09:00
body:

NiceGUIで**三目並べ**を作ったので紹介します。
次のように実行できます。

```zsh
pip install -U nicegui-tic-tac-toe
tic-tac-toe
```

## 遊び方

* 3 x 3の場所に、`X`と`O`を交互に置いていきます
* 先手は`X`を置きます
* 同じものが3つ並んだら勝ちです
* 置く場所がなくなったら引き分けです
* RESETを押すと初期状態に戻ります

![main.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/13955/781c2301-62b4-a826-23fa-02048ca264b0.png)

## コードの説明

置く場所用のFieldクラスと全体用のMainクラスがあります。
Fieldは、置く前はボタンで、置くとアイコンに変わります。
それぞれ、次の属性を持ちます。

| クラス | 属性            | 意味                        |
| :----- | :-------------- | :-------------------------- |
| Field  | `click`         | ボタンのクリック用          |
| Field  | `index`         | ボタンの番号                |
| Field  | `value`         | アイコンに表示するFieldの値 |
| Field  | `icon`          | アイコン                    |
| Field  | `__init__()`    | メンバーの初期化            |
| Field  | `build()`       | 構成要素の作成              |
| Main   | `fields`        | 9つのFieldのリスト          |
| Main   | `message`       | 上部に表示するテキスト      |
| Main   | `player`        | Fieldの値の元               |
| Main   | `__init__()`    | 構成要素の作成              |
| Main   | `reset()`       | 画面の初期化                |
| Main   | `click()`       | Fieldのクリック用           |
| Main   | `set_message()` | 勝者を求めテキストを設定    |

## クラスの実装

各クラスの実装は次のように、わりとシンプルです。

```python
class Field(ui.element):
    def __init__(self, click, index: int):
        super().__init__("div")
        self.click = click  # ボタンのクリック用
        self.index = index  # ボタンの番号

    def build(self, value: t.Literal["X", "O", ""]):
        self.clear()  # 子要素をクリア
        self.value = value
        with self:
            # 値があるときはアイコンを、ないときはボタンを表示
            if self.value:
                name = "close" if self.value == "X" else "radio_button_unchecked"
                color = "red" if self.value == "X" else "indigo-4"
                self.icon = ui.icon(name, size="3em", color=color).classes("size-10")
            else:
                ui.button(str(self.index), on_click=self.click).classes("rounded-xl size-10 bg-cyan-2")


class Main:
    def __init__(self):
        with ui.column().style("margin: 0 auto"):
            self.fields = []  # 9つのFieldのリスト
            # メッセージ(self.messageにバインド)
            ui.label("").bind_text(self, "message").classes("text-4xl")
            with ui.card().classes("bg-cyan-1"):
                for i in range(3):
                    with ui.row():
                        self.fields.extend([Field(self.click, i * 3 + j) for j in range(3)])
            ui.button("reset", icon="refresh", on_click=self.reset).props("flat")
            self.reset()  # 画面の初期化

    def reset(self):
        self.player: t.Literal["X", "O", ""] = "X"
        self.message = f"{self.player}'s turn"
        for field in self.fields:
            field.build("")  # Fieldの再作成

    def click(self, event):
        if "won" not in self.message:
            self.fields[int(event.sender.text)].build(self.player)
            self.player = "X" if self.player == "O" else "O"
            self.set_message()

    def set_message(self):
        for combination in [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}]:
            values = "".join(self.fields[i].value for i in combination)
            if values in {"OOO", "XXX"}:
                self.message = f"{values[0]} has won!"
                for i in range(9):
                    if i not in combination and hasattr(self.fields[i], "icon"):
                        self.fields[i].icon.classes("opacity-20")  # 揃ってないアイコンを薄くする
                break
        else:
            if all(field.value for field in self.fields):
                self.message = "draw"
            else:
                self.message = f"{self.player}'s turn"

```

## 実装の説明

* NiceGUIでUIコンポーネントを作成するには、`ui.element`から派生します
    * タグの種類は、`super().__init__("div")`のように指定します
    * コンポーネント内に構成要素を作成するには、`with self`内に書きます
    * コンポーネント内の構成要素は`self.clear()`でクリアできます
* ラベルのテキストなどをクラスの属性にバインドするには、`bind_text(self, 属性名)`とします
* クリックされたオブジェクトの属性は、イベントハンドラ内で`event.sender.属性名`とします
* 構成要素は任意の時点で`classes("opacity-20")`などのようにクラスを付加できます

## プロジェクト一式

全体については、次のプロジェクト一式を参照してください。

https://github.com/SaitoTsutomu/nicegui-tic_tac_toe

## 題材

RioのTic-Tac-Toeを題材にしました。

https://rio.dev/examples/tic-tac-toe

以上

