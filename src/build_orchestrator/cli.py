from __future__ import annotations

import argparse
import json

from .graph import load_graph
from .planner import plan_build


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a deterministic build plan.")
    parser.add_argument("graph", help="Path to a JSON build graph.")
    args = parser.parse_args()

    graph = load_graph(args.graph)
    plan = plan_build(graph)
    print(
        json.dumps(
            {
                "targets": plan.target_count,
                "stages": plan.stage_count,
                "plan": [list(stage) for stage in plan.stages],
                "cache_keys": plan.cache_keys,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

