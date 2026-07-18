# Build Orchestrator

Build Orchestrator is a systems-infrastructure project for deterministic build graph planning and cache-key design.

The current implementation validates a build graph, detects cycles and missing dependencies, computes parallel execution stages, and derives deterministic cache keys from commands, inputs, outputs, dependencies, and source fingerprints.

## Why this project

Build systems are a compact version of infrastructure engineering: dependency graphs, cache invalidation, scheduling, retries, worker coordination, content-addressed storage, and observability all matter. This repo focuses first on the graph planner and cache-key model that later execution layers depend on.

## Current Features

- JSON build graph loader.
- DAG validation with duplicate, missing-dependency, and cycle detection.
- Deterministic topological staging for parallel execution.
- Stable SHA-256 cache keys per target.
- CLI for rendering a build plan from a graph file.
- Unit tests for planner correctness and cache-key stability.
- Benchmark script for synthetic DAG planning throughput.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
build-orchestrator examples/demo_graph.json
PYTHONPATH=src python -m unittest discover -s tests -p "test_*.py"
python scripts/benchmark.py
```

## Benchmark

Latest local result on the synthetic benchmark:

| Metric | Value |
| --- | ---: |
| Targets planned | 1,000 |
| Dependency edges | 1,800 |
| Parallel stages | 10 |
| Median planning time | 11.197 ms |
| p95 planning time | 12.976 ms |

Run `python scripts/benchmark.py` to regenerate exact machine-local timings.
