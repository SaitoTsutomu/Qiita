title: asyncioを使ったPuLPで、複数ソルバーの並列処理
tags: Python 最適化 並列処理 pulp asyncio
url: https://qiita.com/SaitoTsutomu/items/7d1e458d0faf3c5e52c0
created_at: 2024-09-21 14:01:59+09:00
updated_at: 2024-09-21 16:46:15+09:00
body:

## 概要

数理最適化のモデラーであるPuLPで**異なるソルバーを並列実行**して、高速に解を求めてみましょう。

PuLPではさまざまなソルバーを扱うことができます。本記事では、CBCとHiGHSを使います。

* CBC: https://github.com/coin-or/Cbc
* HiGHS: https://github.com/ERGO-Code/HiGHS

並列実行のうちの1つでも解が得られたら、すべての処理を終了することで、別々に解くより速く解ける可能性があります。

## 準備

PuLPとCBCは、次のようにインストールできます。

```
pip install pulp
```

HiGHSのインストールは、[Installation](https://github.com/ERGO-Code/HiGHS?tab=readme-ov-file#installation)を参照してください。
私は、`brew install highs`でインストールしました。

## pulp_async.py

asyncioを使って並列実行します。asyncioはシングルスレッドですが、PuLPでは別プロセスでソルバーを実行するので、並列実行できます。

最初に、次の機能を実装します。

* `parallel_solve`: モデルと複数のソルバーを受け取って並列実行する関数
* `PULP_CBC_CMD_ASYNC`: ソルバーPULP_CBC_CMDの並列実行版
* `HiGHS_CMD_ASYNC`: ソルバーHiGHS_CMDの並列実行版

次の内容を`pulp_async.py`として保存してください。この内容は、PuLPの元々の実装を非同期処理用に少し書き換えたものです。

```python:pulp_async.py
import asyncio
import inspect
import sys
from asyncio.subprocess import DEVNULL, PIPE
from contextlib import suppress
from pathlib import Path

import pulp as pl


async def parallel_solve(m: pl.LpProblem, solvers: list[pl.LpSolver]) -> pl.LpProblem:
    for solver in solvers:
        assert inspect.iscoroutinefunction(solver.actualSolve), f"{solver.__class__}.actualSolve must be coroutine"
    tasks = [asyncio.create_task(_solve(m, solver)) for solver in solvers]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        with suppress(asyncio.exceptions.CancelledError):
            task.cancel()
    return next(iter(done)).result()


async def _solve(m: pl.LpProblem, solver: pl.LpSolver) -> pl.LpProblem:
    m = pl.LpProblem.deepcopy(m)
    m.solver = solver
    await solver.actualSolve(m)
    return m


class PULP_CBC_CMD_ASYNC(pl.PULP_CBC_CMD):
    async def actualSolve(self, lp, **kwargs):
        """Solve a well formulated lp problem"""
        return await self.solve_CBC(lp, **kwargs)

    async def solve_CBC(self, lp, use_mps=True):  # noqa: FBT002
        """Solve a MIP problem using CBC"""
        if not self.executable(self.path):
            _msg = f"Pulp: cannot execute {self.path} cwd: {Path.cwd()}"
            raise pl.PulpSolverError(_msg)
        tmpLp, tmpMps, tmpSol, tmpMst = self.create_tmp_files(lp.name, "lp", "mps", "sol", "mst")
        if use_mps:
            vs, variablesNames, constraintsNames, _ = lp.writeMPS(tmpMps, rename=1)
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
        process = await asyncio.create_subprocess_exec(*args, stdin=DEVNULL, stdout=PIPE, stderr=PIPE)
        stdout, stderr = await process.communicate()
        if self.msg and (_msg := stdout.decode()):
            print(_msg)
        if _msg := stderr.decode():
            print(_msg, file=sys.stderr)
        if process.returncode != 0:
            raise pl.PulpSolverError("Pulp: Error while trying to execute, use msg=True for more details" + self.path)
        if not Path(tmpSol).exists():
            raise pl.PulpSolverError("Pulp: Error while executing " + self.path)
        _mps = self.readsol_MPS(tmpSol, lp, vs, variablesNames, constraintsNames)
        status, values, reducedCosts, shadowPrices, slacks, sol_status = _mps
        lp.assignVarsVals(values)
        lp.assignVarsDj(reducedCosts)
        lp.assignConsPi(shadowPrices)
        lp.assignConsSlack(slacks, activity=True)
        lp.assignStatus(status, sol_status)
        self.delete_tmp_files(tmpMps, tmpLp, tmpSol, tmpMst)
        return status


class HiGHS_CMD_ASYNC(pl.HiGHS_CMD):
    async def actualSolve(self, lp):
        """Solve a well formulated lp problem"""
        if not self.executable(self.path):
            raise pl.PulpSolverError("PuLP: cannot execute " + self.path)
        lp.checkDuplicateVars()

        tmpMps, tmpSol, tmpOptions, tmpLog, tmpMst = self.create_tmp_files(
            lp.name,
            "mps",
            "sol",
            "HiGHS",
            "HiGHS_log",
            "mst",
        )
        lp.writeMPS(tmpMps, with_objsense=True)

        file_options = [
            f"solution_file={tmpSol}",
            "write_solution_to_file=true",
            f"write_solution_style={pl.HiGHS_CMD.SOLUTION_STYLE}",
        ]
        if not self.msg:
            file_options.append("log_to_console=false")
        if "threads" in self.optionsDict:
            file_options.append(f"threads={self.optionsDict['threads']}")
        if "gapRel" in self.optionsDict:
            file_options.append(f"mip_rel_gap={self.optionsDict['gapRel']}")
        if "gapAbs" in self.optionsDict:
            file_options.append(f"mip_abs_gap={self.optionsDict['gapAbs']}")
        highs_log_file = self.optionsDict.get("logPath", tmpLog)
        file_options.append(f"log_file={highs_log_file}")

        command = [self.path, tmpMps, f"--options_file={tmpOptions}"]
        if self.timeLimit is not None:
            command.append(f"--time_limit={self.timeLimit}")
        if not self.mip:
            command.append("--solver=simplex")
        if "threads" in self.optionsDict:
            command.append("--parallel=on")
        if self.optionsDict.get("warmStart", False):
            self.writesol(tmpMst, lp)
            command.append(f"--read_solution_file={tmpMst}")

        options = iter(self.options)
        for option_ in options:
            option = option_
            # assumption: all cli and file options require an argument which is provided after the equal sign (=)
            if "=" not in option:
                option += f"={next(options)}"

            # identify cli options by a leading dash (-) and treat other options as file options
            if option.startswith("-"):
                command.append(option)
            else:
                file_options.append(option)

        Path(tmpOptions).write_text("\n".join(file_options), encoding="utf-8")
        process = await asyncio.create_subprocess_exec(*command, stdin=DEVNULL, stdout=PIPE, stderr=PIPE)
        stdout, stderr = await process.communicate()
        if self.msg and (_msg := stdout.decode()):
            print(_msg)
        if _msg := stderr.decode():
            print(_msg, file=sys.stderr)
        # HiGHS return code semantics (see: https://github.com/ERGO-Code/HiGHS/issues/527#issuecomment-946575028)
        # - -1: error
        # -  0: success
        # -  1: warning
        # process = subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr)
        if process.returncode == -1:
            raise pl.PulpSolverError(
                "Pulp: Error while executing HiGHS, use msg=True for more details" + self.path,
            )
        lines = [line.strip().split() for line in Path(highs_log_file).read_text(encoding="utf-8").splitlines()]

        # LP
        model_line = [line for line in lines if line[:2] == ["Model", "status"]]
        if len(model_line) > 0:
            model_status = " ".join(model_line[0][3:])  # Model status: ...
        else:
            # ILP
            model_line = next(line for line in lines if "Status" in line)
            model_status = " ".join(model_line[1:])
        sol_line = [line for line in lines if line[:2] == ["Solution", "status"]]
        sol_line = sol_line[0] if len(sol_line) > 0 else ["Not solved"]
        sol_status = sol_line[-1]
        if model_status.lower() == "optimal":  # optimal
            status, status_sol = (
                pl.constants.LpStatusOptimal,
                pl.constants.LpSolutionOptimal,
            )
        elif sol_status.lower() == "feasible":  # feasible
            # Following the PuLP convention
            status, status_sol = (
                pl.constants.LpStatusOptimal,
                pl.constants.LpSolutionIntegerFeasible,
            )
        elif model_status.lower() == "infeasible":  # infeasible
            status, status_sol = (
                pl.constants.LpStatusInfeasible,
                pl.constants.LpSolutionInfeasible,
            )
        elif model_status.lower() == "unbounded":  # unbounded
            status, status_sol = (
                pl.constants.LpStatusUnbounded,
                pl.constants.LpSolutionUnbounded,
            )
        else:  # no solution
            status, status_sol = (
                pl.constants.LpStatusNotSolved,
                pl.constants.LpSolutionNoSolutionFound,
            )

        tmpSolPth = Path(tmpSol)
        if not tmpSolPth.exists() or tmpSolPth.stat().st_size == 0:
            status_sol = pl.constants.LpSolutionNoSolutionFound
            values = None
        elif status_sol in {
            pl.constants.LpSolutionNoSolutionFound,
            pl.constants.LpSolutionInfeasible,
            pl.constants.LpSolutionUnbounded,
        }:
            values = None
        else:
            values = self.readsol(str(tmpSolPth))

        self.delete_tmp_files(tmpMps, tmpSol, tmpOptions, tmpLog, tmpMst)
        lp.assignStatus(status, status_sol)

        if status == pl.constants.LpStatusOptimal:
            lp.assignVarsVals(values)

        return status
```

## 実験

MIPLIBから次の2つの問題を選びました。URL先からダウンロードして解凍しておいてください。

* `assign1-5-8`: https://miplib.zib.de/instance_details_assign1-5-8.html
* `markshare_4_0`: https://miplib.zib.de/instance_details_markshare_4_0.html

まずは、`assign1-5-8`で実行してみましょう。6秒ほどで終了します。

```python
import pulp as pl
from pulp_async import parallel_solve, PULP_CBC_CMD_ASYNC, HiGHS_CMD_ASYNC

options = {"gapRel": 0.06, "msg": False}
solvers = [PULP_CBC_CMD_ASYNC(**options), HiGHS_CMD_ASYNC(**options)]
m = pl.LpProblem.fromMPS("benchmark/assign1-5-8.mps")[1]
m = await parallel_solve(m, solvers)
print(m.solver.__class__.__name__, pl.LpStatus[m.status], pl.value(m.objective))
>>>
HiGHS_CMD_ASYNC Optimal 212.0
```

HiGHSで解が得られました。gapRelを指定していますが`Best Known Solution`が得られています。

続いて、`markshare_4_0`で実行してみましょう。10秒ほどで終了します。

```python
m = pl.LpProblem.fromMPS("benchmark/markshare_4_0.mps")[1]
m = await parallel_solve(m, solvers)
print(m.solver.__class__.__name__, pl.LpStatus[m.status], pl.value(m.objective))
>>>
PULP_CBC_CMD_ASYNC Optimal 1.0
```

CBCで解が得られました。こちらも`Best Known Solution`が得られています。

### 説明

`assign1-5-8`をCBCで解くと10分経っても答えは出ません。ここでは、HiGHSを使って6秒で答えが出ました。
`markshare_4_0`はHiGHSで2分ほどかかりますが、CBCでは10秒で答えが出ました。
このように、複数のソルバーが並列に実行されているのを確認できました。

## 補足

ここでは、1ソルバーあたり1回しか実行していませんが、次の記事のように複数回実行することでさらに速くなる可能性があります。

https://qiita.com/SaitoTsutomu/items/1b28dd4f7e1e0792b98e

## まとめ

複数のソルバーを並列に実行する方法を紹介しました。
PuLPではsubprocessでソルバーを呼び出しています。この呼び出しをasyncioに置き換えることで並列実行が可能になります。

なお、ここで紹介しているコードは、完璧ではありませんので、ご利用時は注意してください。

以上

