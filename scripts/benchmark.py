from __future__ import annotations

from pathlib import Path
import json
import statistics
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from build_orchestrator.graph import BuildGraph, Target
from build_orchestrator.planner import plan_build


def synthetic_graph(layers: int = 10, width: int = 100) -> BuildGraph:
    graph: dict[str, Target] = {}
    for layer in range(layers):
        for index in range(width):
            name = f"target-{layer}-{index}"
            deps = []
            if layer > 0:
                deps.append(f"target-{layer - 1}-{index}")
                deps.append(f"target-{layer - 1}-{(index + 1) % width}")
            graph[name] = Target(
                name=name,
                command=f"compile {name}",
                deps=tuple(deps),
                inputs=(f"src/{layer}/{index}.cc",),
                outputs=(f"build/{layer}/{index}.o",),
            )
    return BuildGraph(graph)


def main() -> None:
    graph = synthetic_graph()
    samples = []
    last_plan = None
    for _ in range(50):
        start = time.perf_counter()
        last_plan = plan_build(graph)
        samples.append((time.perf_counter() - start) * 1000)

    result = {
        "targets": graph.target_count(),
        "edges": graph.edge_count(),
        "stages": last_plan.stage_count if last_plan else 0,
        "median_ms": round(statistics.median(samples), 3),
        "p95_ms": round(sorted(samples)[int(len(samples) * 0.95) - 1], 3),
        "runs": len(samples),
    }
    out_dir = ROOT / "benchmarks" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "latest.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
