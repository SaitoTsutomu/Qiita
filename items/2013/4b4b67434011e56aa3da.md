title: 複数タブ内でのSplitContainerの名前のつけ方
tags: VisualStudio
url: https://qiita.com/SaitoTsutomu/items/4b4b67434011e56aa3da
created_at: 2013-01-06 08:06:22+09:00
updated_at: 2013-01-06 08:06:22+09:00
body:

N枚目のタブのM個めのSplitContainerの名前を`splitContainerN_M`とします。
このようにして、一度つけた名前は、変更しないようにします。

理由：SplitContainerの名前を後から変えると、VisualStudioのデザイナがおかしくなるため。(バグと思われます)
