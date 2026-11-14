title: asyncioを使ったPuLPの並列処理
tags: Python 最適化 並列処理 pulp asyncio
url: https://qiita.com/SaitoTsutomu/items/1b28dd4f7e1e0792b98e
created_at: 2024-09-17 21:56:12+09:00
updated_at: 2024-09-21 19:34:53+09:00
body:

## 概要

数理最適化のモデラーであるPuLPで並列実行して、高速に解を求めてみましょう。

多くの数理最適化ソルバーでは、変数の順番を変更すると解が得られるまでの計算時間が変化します。
そこで、本記事では**変数の順番を変えたモデルを複数作成して並列で実行します**。
並列実行のうちの1つでも解が得られたら、すべての処理を終了することで、通常より速く解ける可能性があります[^1]。

[^1]: 有料ソルバーで使われるテクニックです。

## 並列実行の方法

ソルバーとして**CBC**を使います。PuLPのソルバークラスでは、`subprocess`モジュールを使ってCBCを呼び出しています。
本記事では、`asyncio.create_subprocess_exec`関数を使ってCBCの呼び出しを並列に実行します。

## サンプルモデルで実行

最初に大枠の実行方法を確認します。次のようにPuLPをインストールしてください。ソルバーのCBCも一緒にインストールされます。

```sh
pip install pulp
```

サンプルのモデルを作成し、`parallel_solve`関数（実装は後述）で並列実行し、結果を表示してみましょう。
次のように`main.py`を作成します。

```python:main.py
import asyncio

import pulp as pl
from async_pulp import parallel_solve


async def main():
    m = pl.LpProblem(sense=-1)
    x = pl.LpVariable("x", 0)
    y = pl.LpVariable("y", 0)
    m.setObjective(x + y)
    m += x + 2 * y <= 16
    m += 3 * x + y <= 18
    m = await parallel_solve(m, 4, msg=False)
    dct = m.variablesDict()
    print(pl.LpStatus[m.status], pl.value(dct["x"]), pl.value(dct["y"]))


asyncio.run(main())
```

`python main.py`で実行してみましょう。次のように最適解が出力されます[^2]。

[^2]: 本サンプルモデルは小さいので並列実行する意味はないです。効果を確認するには、もっと大きなモデルで試してみてください。

```
Optimal 4.0 6.0
```

`parallel_solve`ではモデルを複製して実行しています。そして、最適解が得られたモデルを戻り値にしています。
つまり、入力の`m`と出力の`m`では異なるオブジェクトになっていることがあります。
そのため、変数は、`x`ではなく`dct["x"]`を使う必要があります。

## async_pulpモジュール

`parallel_solve`関数を完成させるには、モデルとソルバーを次のように修正する必要があります。

* モデルの全変数を取得するときに、変数をソートしないように修正（`variables`メソッド）
* モデルの複製時に、変数をソートしないモデルを作成するように修正（`deepcopy`メソッド）
* ソルバーの実行時に、asyncioで非同期処理をするように修正（`solve_CBC`）

PuLPの元々のモデルクラスでは、全変数の取得時に変数名順にソートしています。
本記事では、変数の順序を変えて実行するので、ソートしないようにする必要があります。

`async_pulp`モジュールは、次のようになります。

```python:async_pulp.py
import asyncio
import os
import random
import sys

import pulp as pl


class LpProblemNoSort(pl.LpProblem):
    def deepcopy(self):
        """Make a copy of self. Expressions are copied by value"""
        lpcopy = LpProblemNoSort(name=self.name, sense=self.sense)
        if self.objective is not None:
            lpcopy.objective = self.objective.copy()
        lpcopy.constraints = {}
        for k, v in self.constraints.items():
            lpcopy.constraints[k] = v.copy()
        lpcopy.sos1 = self.sos1.copy()
        lpcopy.sos2 = self.sos2.copy()
        return lpcopy

    def variables(self):
        """
        Returns the problem variables

        :return: A list containing the problem variables
        :rtype: (list, :py:class:`LpVariable`)
        """
        if self.objective:
            self.addVariables(list(self.objective.keys()))
        for c in self.constraints.values():
            self.addVariables(list(c.keys()))
        # self._variables.sort(key=lambda v: v.name)
        return self._variables


class ASYNC_PULP_CBC_CMD(pl.PULP_CBC_CMD):
    async def solve_CBC(self, lp, use_mps=True):
        """Solve a MIP problem using CBC"""
        if not self.executable(self.path):
            raise pl.PulpSolverError(f"Pulp: cannot execute {self.path} cwd: {os.getcwd()}")
        tmpLp, tmpMps, tmpSol, tmpMst = self.create_tmp_files(lp.name, "lp", "mps", "sol", "mst")
        if use_mps:
            vs, variablesNames, constraintsNames, objectiveName = lp.writeMPS(tmpMps, rename=1)
            cmds = " " + tmpMps + " "
            if lp.sense == pl.constants.LpMaximize:
                cmds += "-max "
        else:
            vs = lp.writeLP(tmpLp)
            # In the Lp we do not create new variable or constraint names:
            variablesNames = {v.name: v.name for v in vs}
            constraintsNames = {c: c for c in lp.constraints}
            cmds = " " + tmpLp + " "
        if self.optionsDict.get("warmStart", False):
            self.writesol(tmpMst, lp, vs, variablesNames, constraintsNames)
            cmds += f"-mips {tmpMst} "
        if self.timeLimit is not None:
            cmds += f"-sec {self.timeLimit} "
        options = self.options + self.getOptions()
        for option in options:
            cmds += "-" + option + " "
        if self.mip:
            cmds += "-branch "
        else:
            cmds += "-initialSolve "
        cmds += "-printingOptions all "
        cmds += "-solution " + tmpSol + " "
        pl.log.debug(self.path + cmds)
        args = []
        args.append(self.path)
        args.extend(cmds[1:].split())
        process = await asyncio.create_subprocess_exec(
            *args, stdin=asyncio.subprocess.DEVNULL, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise pl.PulpSolverError("Pulp: Error while trying to execute, use msg=True for more details" + self.path)
        if not os.path.exists(tmpSol):
            raise pl.PulpSolverError("Pulp: Error while executing " + self.path)
        if self.msg:
            print(stdout.decode())
            print(stderr.decode(), file=sys.stderr)
        status, values, reducedCosts, shadowPrices, slacks, sol_status = self.readsol_MPS(
            tmpSol, lp, vs, variablesNames, constraintsNames
        )
        lp.assignVarsVals(values)
        lp.assignVarsDj(reducedCosts)
        lp.assignConsPi(shadowPrices)
        lp.assignConsSlack(slacks, activity=True)
        lp.assignStatus(status, sol_status)
        self.delete_tmp_files(tmpMps, tmpLp, tmpSol, tmpMst)
        return status


async def _solve(m: pl.LpProblem, msg: bool, *, shuffle: bool = False) -> pl.LpProblem:
    if shuffle:
        m = LpProblemNoSort.deepcopy(m)
        m._variables = m.variables()
        random.shuffle(m._variables)
    solver = ASYNC_PULP_CBC_CMD(msg=msg)
    await solver.solve_CBC(m)
    return m


async def parallel_solve(m: pl.LpProblem, num: int, *, msg: bool = True) -> pl.LpProblem:
    tasks = [asyncio.create_task(_solve(m, msg, shuffle=i > 0)) for i in range(num)]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    return next(iter(done)).result()
```

### 簡単な説明

`parallel_solve`関数では、下記のようにして非同期処理をしています。
`return_when=asyncio.FIRST_COMPLETED`とすることで、1つでも処理が終われば、`asyncio.wait`が処理を終了します。
ただし、`pending`のタスクは処理中なので、`task.cancel()`で処理を中断します（ここはtryを使った方が安全かもしれません）。

```python
done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
```

`_solve`では、変数をシャッフルしています。プライベートメンバを使っているので注意してください。

`solve_CBC`では、次のように非同期処理をしています。

```python
process = await asyncio.create_subprocess_exec(
    *args, stdin=asyncio.subprocess.DEVNULL, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
)
stdout, stderr = await process.communicate()
```

最初のawaitでCBCを起動し、次のawaitで標準出力などを取得しています。

## まとめ

ソルバーの並列実行方法を紹介しました。
PuLPでは`subprocess`でソルバーを呼び出しています。この呼び出しをasyncioに置き換えることで並列実行が可能になります。

変数順を変えることで計算時間が異なります。そのため、変数順をランダムシャッフルして複数実行することで速く解が得られるようになります。

なお、ここで紹介しているコードは、完璧ではありませんので、ご利用時は注意してください。

## 参考

https://qiita.com/SaitoTsutomu/items/7d1e458d0faf3c5e52c0

以上

