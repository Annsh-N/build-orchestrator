# Build Orchestrator

Build Orchestrator is a small systems-infrastructure project for experimenting with deterministic build graph planning, cache-key design, and eventually distributed task execution.

Current status: **v0 scaffold with a real DAG planner and benchmark harness**. It does not yet claim remote execution. The current implementation validates a build graph, detects cycles and missing dependencies, computes parallel execution stages, and derives deterministic cache keys from commands, inputs, outputs, dependencies, and source fingerprints.

## Why this project

Build systems are a good compact version of distributed infrastructure: dependency graphs, cache invalidation, scheduling, retries, worker coordination, content-addressed storage, and observability all matter. This repo starts with the part that must be correct before distribution: the graph planner and cache-key model.

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
PYTHONPATH=src python -m unittest
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

## Roadmap

1. Add a local executor with task states, retries, structured logs, and failure propagation.
2. Add persistent cache metadata and artifact fingerprints.
3. Add worker protocol simulation over HTTP or gRPC.
4. Add scheduler benchmarks for fan-out, chain, and mixed DAG workloads.
5. Add observability: queue depth, task latency, cache-hit rate, and critical path length.

## Resume framing

Use this repo honestly as an in-progress systems project: deterministic DAG planner, cache-key design, validation, and benchmark harness. Do not claim distributed workers until the executor/protocol exists.
