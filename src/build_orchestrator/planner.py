from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass

from .graph import BuildGraph


@dataclass(frozen=True)
class BuildPlan:
    stages: tuple[tuple[str, ...], ...]
    cache_keys: dict[str, str]

    @property
    def target_count(self) -> int:
        return sum(len(stage) for stage in self.stages)

    @property
    def stage_count(self) -> int:
        return len(self.stages)


def plan_build(graph: BuildGraph, source_fingerprints: dict[str, str] | None = None) -> BuildPlan:
    missing = sorted(
        (target.name, dep)
        for target in graph.targets.values()
        for dep in target.deps
        if dep not in graph.targets
    )
    if missing:
        target, dep = missing[0]
        raise ValueError(f"target {target} depends on unknown target {dep}")

    indegree = {name: len(target.deps) for name, target in graph.targets.items()}
    children: dict[str, list[str]] = defaultdict(list)
    for target in graph.targets.values():
        for dep in target.deps:
            children[dep].append(target.name)

    ready = deque(sorted(name for name, degree in indegree.items() if degree == 0))
    stages: list[tuple[str, ...]] = []
    visited = 0

    while ready:
        stage = tuple(ready)
        ready.clear()
        stages.append(stage)
        visited += len(stage)

        next_ready: list[str] = []
        for name in stage:
            for child in children[name]:
                indegree[child] -= 1
                if indegree[child] == 0:
                    next_ready.append(child)
        ready.extend(sorted(next_ready))

    if visited != len(graph.targets):
        blocked = sorted(name for name, degree in indegree.items() if degree > 0)
        raise ValueError(f"cycle detected involving: {', '.join(blocked[:5])}")

    return BuildPlan(
        stages=tuple(stages),
        cache_keys={
            name: target.cache_key(source_fingerprints)
            for name, target in sorted(graph.targets.items())
        },
    )

