"""Student-facing MovieLens conversion -> diagnosis runner.

Automatically discovers its companion scripts by searching upward from this
file for a ``code/`` directory that contains the required scripts.  An explicit
``--code-dir`` override is also supported so the pipeline works from any
directory layout or working directory.

Each run writes **all 7 required deliverables** into the output directory:

1. ``movielens_edges.csv``
2. ``movielens_users.csv``
3. ``movielens_metadata.json``
4. ``movielens_q2.json``
5. ``run_log.md``               — command + full terminal output
6. ``threshold_data_card.md``   — key metrics for this threshold
7. ``semantic_note.md``         — affiliation-context rationale
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# These two scripts must live together in the same code directory.
# ---------------------------------------------------------------------------
_REQUIRED_SCRIPTS = ("convert_movielens_100k.py", "generic_affiliation_diagnostic.py")

# ---------------------------------------------------------------------------
# Item 7 — semantic note (constant, same for every threshold)
# ---------------------------------------------------------------------------
_SEMANTIC_NOTE = """\
# 语义说明：电影是共同属性语境，不是同时群体事件

## 为什么这个区分至关重要

本实验的核心数据结构是「用户—电影」二分网络：每个用户与若干电影之间存在
评分连线。**这些连线代表的是属性归属（用户与该电影有交互记录），而不是
群体事件中的同时参与。**

### 1. 共同语境 vs 同时事件

- **共同属性语境 (affiliation context)**：两个用户都评分了同一部电影，意味着
  他们共享了这部电影作为「共同属性」。但这两人可能相隔十年分别打分，从未
  「同时」出现在任何场景中。
- **同时群体事件 (simultaneous group event)**：典型例子是同一艘船上的船员、
  同一场会议的参会者——个体在某个时间窗口中真实共存于同一事件中。

MovieLens 属于前者。**电影是静态的信息载体，而不是动态的社会容器。**

### 2. 为什么不能使用投影网络来推断社交结构

- **零值不携带信息**：两个用户都没评分某部电影，不意味着他们有任何社会意义上的
  「共同不在场」。
- **共享量的可膨胀性**：添加更多电影（共同零）可以任意提高两个用户的伪相关度——
  本实验中的零节点敏感性测试精确展示了这一问题。

### 3. 方法论的约束条件

- 用户间的相关程度反映的是品味相似度，不是社会交往强度。
- 零值代表信息缺失——我们不知道用户是否「会选择看」那部电影。
- 随着评分阈值升高，是属性空间变得更稀疏，而非用户变得「更少联系」。

### 4. 与联名发表、船舶网络等场景的关键区别

| 场景 | 数据类型 | 语境性质 | 零值含义 |
|------|---------|----------|---------|
| 船舶船员网络 | 同时群体事件 | 船员同时同船 = 有社交接触 | 不上船 = 确实不共处 |
| 学术合著网络 | 同时群体事件 | 合著者同时撰文 = 有合作 | 不署名 = 确实不合作 |
| **MovieLens** | **共同属性** | **共享品味交集** | **未评分 ≠ 不会选择** |

> Harper, F. M., & Konstan, J. A. (2015). The MovieLens Datasets:
> History and Context. DOI: `10.1145/2827872`
"""

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class _OutputPaths:
    output_dir: Path
    edges: Path
    users: Path
    metadata: Path
    result: Path
    run_log: Path
    data_card: Path
    semantic_note: Path


def _find_code_dir() -> Path:
    """Search upward from this file (max 5 levels) for a ``code/`` directory
    containing both required scripts."""
    current = Path(__file__).resolve().parent
    for _ in range(5):
        candidate = current / "code"
        if all(
            (candidate / script).is_file() for script in _REQUIRED_SCRIPTS
        ):
            return candidate
        if current.parent == current:  # filesystem root — stop
            break
        current = current.parent

    raise FileNotFoundError(
        "Could not auto-detect the code directory containing "
        + ", ".join(_REQUIRED_SCRIPTS)
        + ". Use --code-dir to specify the path explicitly."
    )


def _run_script(arguments: list[str], timeout: int = 300) -> str:
    """Run a Python script, stream + capture stdout, handle errors.
    Returns the captured stdout text.
    """
    cmd_line = f"{sys.executable} {' '.join(arguments)}"
    print(f"[pipeline] {cmd_line}")
    try:
        result = subprocess.run(
            [sys.executable, *arguments],
            check=True,
            timeout=timeout,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        print(
            f"[pipeline] FAILED — script returned exit code {exc.returncode}",
            file=sys.stderr,
        )
        if exc.stdout:
            print(exc.stdout)
        if exc.stderr:
            print(exc.stderr, file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(
            f"[pipeline] FAILED — script timed out after {timeout}s",
            file=sys.stderr,
        )
        sys.exit(1)
    # stream captured output to terminal as well
    sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.stdout


def _validate_rating_min(parser: argparse.ArgumentParser, value: float) -> None:
    """Ensure rating_min is within the valid range."""
    if not 1.0 <= value <= 5.0:
        parser.error(
            f"--rating-min must be between 1.0 and 5.0, got {value}"
        )


def _resolve_code_dir(
    parser: argparse.ArgumentParser, explicit: Path | None,
) -> Path:
    """Return the code directory, validating that both scripts are present."""
    if explicit is not None:
        code_dir = explicit.resolve()
        for script in _REQUIRED_SCRIPTS:
            if not (code_dir / script).is_file():
                parser.error(
                    f"Required script not found in --code-dir: "
                    f"{code_dir / script}"
                )
    else:
        try:
            code_dir = _find_code_dir()
        except FileNotFoundError as exc:
            parser.error(str(exc))
    print(f"[pipeline] code directory : {code_dir}")
    return code_dir


def _validate_input(
    parser: argparse.ArgumentParser, data_dir: Path, *,
    source_name: str = "ml-100k.zip",
) -> Path:
    """Validate data directory and return the resolved source zip path."""
    if not data_dir.is_dir():
        parser.error(
            f"--data-dir does not exist or is not a directory: {data_dir}"
        )
    source = data_dir / source_name
    if not source.is_file():
        parser.error(f"Input file not found: {source}")
    return source


def _compute_paths(data_dir: Path, rating_min: float) -> _OutputPaths:
    """Build all output paths from data directory and rating threshold."""
    label = str(rating_min).replace(".", "p")
    output_dir = data_dir / f"rating_min_{label}"
    return _OutputPaths(
        output_dir=output_dir,
        edges=output_dir / "movielens_edges.csv",
        users=output_dir / "movielens_users.csv",
        metadata=output_dir / "movielens_metadata.json",
        result=output_dir / "movielens_q2.json",
        run_log=output_dir / "run_log.md",
        data_card=output_dir / "threshold_data_card.md",
        semantic_note=output_dir / "semantic_note.md",
    )


# ---------------------------------------------------------------------------
# Item 5 — run log
# ---------------------------------------------------------------------------
def _write_run_log(
    paths: _OutputPaths,
    cmd_convert: str,
    cmd_diagnosis: str,
    output_convert: str,
    output_diagnosis: str,
    rating_min: float,
) -> None:
    """Write run_log.md with command lines and full terminal output."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    content = f"""\
# 运行命令与终端日志

**阈值**: rating_min = {rating_min}
**运行时间**: {timestamp}

## 阶段 1 — 数据转换

命令:

```powershell
python {cmd_convert}
```

终端输出:

```json
{output_convert.strip()}
```

## 阶段 2 — 属性诊断

命令:

```powershell
python {cmd_diagnosis}
```

终端输出:

```json
{output_diagnosis.strip()}
```
"""
    paths.run_log.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Item 6 — per-threshold data card
# ---------------------------------------------------------------------------
def _write_data_card(paths: _OutputPaths, rating_min: float) -> None:
    """Extract key metrics from the JSON outputs and write a data card."""
    metadata = json.loads(paths.metadata.read_text(encoding="utf-8"))
    q2 = json.loads(paths.result.read_text(encoding="utf-8"))

    counts = metadata["counts"]
    all_nodes = q2["all_nodes_k_vs_P_q"]
    active_nodes = q2["active_nodes_k_vs_P_q"]
    zero_sensitivity = q2["zero_node_sensitivity"]
    zero_baseline = zero_sensitivity[0]
    zero_1000 = zero_sensitivity[-1]

    def _fmt(v: float, digits: int = 3) -> str:
        return f"{v:.{digits}f}"

    content = f"""\
# 阈值数据卡 — rating_min = {rating_min}

## 规模

| 指标 | 值 |
|------|-----|
| 输入评分 | {counts["input_ratings"]:,} |
| 保留边 | {counts["retained_edges"]:,} |
| 活跃用户 | {counts["active_users"]} / {counts["universe_users"]} |
| 非活跃用户 | {counts["inactive_users"]} ({counts["inactive_users"] / counts["universe_users"]:.2%}) |
| 保留电影 | {counts["retained_movies"]:,} |
| q=2 有效上下文 | {q2["input_audit"]["contexts_eligible_for_q"]:,} |

## 全体用户 k vs P_q

| 指标 | 值 |
|------|-----|
| Spearman ρ | {_fmt(all_nodes["spearman"])} |
| Kendall τb | {_fmt(all_nodes["kendall_tau_b"])} |
| Pearson r | {_fmt(all_nodes["pearson"])} |
| 逆序数 | {all_nodes["strict_inversions"]["count"]:,} |
| 可比对数 | {all_nodes["strict_inversions"]["comparable"]:,} |
| 逆序率 | {_fmt(all_nodes["strict_inversions"]["rate"] * 100, 1)}% |

## 活跃用户 k vs P_q

| 指标 | 值 |
|------|-----|
| Spearman ρ | {_fmt(active_nodes["spearman"])} |
| Kendall τb | {_fmt(active_nodes["kendall_tau_b"])} |
| Pearson r | {_fmt(active_nodes["pearson"])} |
| 逆序率 | {_fmt(active_nodes["strict_inversions"]["rate"] * 100, 1)}% |

## Top-K Jaccard

| Top-K | Jaccard |
|-------|---------|
"""
    for k in ("5", "10", "20"):
        content += f"| Top-{k} | {_fmt(all_nodes['top_k'][k]['jaccard'])} |\n"

    content += f"""
## 零节点敏感性

| 添加共同零 | Spearman ρ |
|-----------|------------|
"""
    for entry in zero_sensitivity:
        content += (
            f"| {entry['added_common_zeros']} "
            f"| {_fmt(entry['spearman'])} |\n"
        )

    delta = zero_1000["spearman"] - zero_baseline["spearman"]
    content += f"""
**Δρ (+1000 zeros) = {_fmt(delta, 3)}**

---
> 完整四阈值对比请运行 `aggregate_thresholds.py --data-dir <目录>`。
"""
    paths.data_card.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# stage runners
# ---------------------------------------------------------------------------
def _run_convert(
    code_dir: Path, source: Path, paths: _OutputPaths, rating_min: float,
) -> tuple[str, str]:
    """Stage 1: convert MovieLens 100K → edge / user / metadata files.
    Returns (command_string, captured_output).
    """
    print(f"[pipeline] Stage 1 — convert (rating_min={rating_min})")
    args = [
        str(code_dir / "convert_movielens_100k.py"),
        "--input", str(source),
        "--edges-output", str(paths.edges),
        "--users-output", str(paths.users),
        "--metadata-output", str(paths.metadata),
        "--rating-min", str(rating_min),
    ]
    output = _run_script(args)
    return (" ".join(args), output)


def _run_diagnosis(code_dir: Path, paths: _OutputPaths) -> tuple[str, str]:
    """Stage 2: run q=2 affiliation diagnosis with skip-deduplicated.
    Returns (command_string, captured_output).
    """
    print("[pipeline] Stage 2 — affiliation diagnosis (q=2, skip-deduplicated)")
    args = [
        str(code_dir / "generic_affiliation_diagnostic.py"),
        "--edges", str(paths.edges),
        "--entity-column", "user_id",
        "--context-column", "movie_id",
        "--universe", str(paths.users),
        "--universe-id-column", "user_id",
        "--q", "2",
        "--skip-deduplicated",
        "--output", str(paths.result),
    ]
    output = _run_script(args)
    return (" ".join(args), output)


def _build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser."""
    parser = argparse.ArgumentParser(
        description="MovieLens 100K conversion -> q=2 affiliation diagnosis"
    )
    parser.add_argument(
        "--data-dir", type=Path, required=True,
        help="Directory containing ml-100k.zip",
    )
    parser.add_argument(
        "--rating-min", type=float, default=1.0,
        help="Minimum rating threshold (1.0 – 5.0, default: 1.0)",
    )
    parser.add_argument(
        "--code-dir", type=Path, default=None,
        help="Directory containing the two companion scripts "
             "(auto-detected if omitted)",
    )
    return parser


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> None:
    """Parse arguments, validate inputs, run both pipeline stages, then
    auto-generate the 7 required deliverables.

    Exits with status 1 on validation errors or subprocess failure.
    """
    parser = _build_parser()
    args = parser.parse_args()

    _validate_rating_min(parser, args.rating_min)
    code_dir = _resolve_code_dir(parser, args.code_dir)
    source = _validate_input(parser, args.data_dir)
    paths = _compute_paths(args.data_dir, args.rating_min)

    # ---- stage 1 & 2 --------------------------------------------------------
    cmd_convert, out_convert = _run_convert(
        code_dir, source, paths, args.rating_min,
    )
    cmd_diag, out_diag = _run_diagnosis(code_dir, paths)

    # ---- item 5: run log ----------------------------------------------------
    _write_run_log(paths, cmd_convert, cmd_diag, out_convert, out_diag,
                   args.rating_min)
    print("[pipeline]   [OK] run_log.md")

    # ---- item 6: data card --------------------------------------------------
    _write_data_card(paths, args.rating_min)
    print("[pipeline]   [OK] threshold_data_card.md")

    # ---- item 7: semantic note ----------------------------------------------
    paths.semantic_note.write_text(_SEMANTIC_NOTE, encoding="utf-8")
    print("[pipeline]   [OK] semantic_note.md")

    print(f"[pipeline] Done — 7 files in: {paths.output_dir}")


if __name__ == "__main__":
    main()
