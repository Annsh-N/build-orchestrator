# Architecture

## v0 boundary

The current repo implements graph planning and cache-key computation only. The executor, remote worker protocol, artifact cache, and retry engine are planned but intentionally not claimed as complete.

## Core model

- `Target`: command, dependencies, inputs, outputs, and environment.
- `BuildGraph`: named target map plus edge/target counters.
- `BuildPlan`: deterministic parallel stages plus per-target cache keys.

## Planning algorithm

The planner uses Kahn's algorithm:

1. validate that every dependency references a known target;
2. compute indegrees and reverse edges;
3. repeatedly emit sorted zero-indegree targets as one parallel stage;
4. fail if unvisited targets remain, which indicates a cycle.

This keeps output deterministic and makes test snapshots stable.

## Cache key model

Each target cache key hashes:

- target name;
- command;
- sorted dependencies;
- sorted inputs and outputs;
- sorted environment;
- source fingerprints for input paths.

This is only a local cache-key model. A production artifact cache would also need artifact metadata, platform/toolchain identity, remote CAS semantics, and invalidation policy.

