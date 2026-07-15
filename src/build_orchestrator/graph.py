from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
import json
from typing import Any


@dataclass(frozen=True)
class Target:
    name: str
    command: str
    deps: tuple[str, ...] = ()
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    env: tuple[tuple[str, str], ...] = ()

    def cache_key(self, source_fingerprints: dict[str, str] | None = None) -> str:
        fingerprints = source_fingerprints or {}
        payload = {
            "name": self.name,
            "command": self.command,
            "deps": sorted(self.deps),
            "inputs": sorted(self.inputs),
            "outputs": sorted(self.outputs),
            "env": sorted(self.env),
            "fingerprints": {path: fingerprints.get(path, "") for path in sorted(self.inputs)},
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        return sha256(encoded).hexdigest()


@dataclass(frozen=True)
class BuildGraph:
    targets: dict[str, Target] = field(default_factory=dict)

    def target_count(self) -> int:
        return len(self.targets)

    def edge_count(self) -> int:
        return sum(len(target.deps) for target in self.targets.values())


def _tuple_of_strings(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{field_name} must be a list of strings")
    return tuple(value)


def load_graph(path: str | Path) -> BuildGraph:
    data = json.loads(Path(path).read_text())
    raw_targets = data.get("targets")
    if not isinstance(raw_targets, list):
        raise ValueError("graph file must contain a targets list")

    targets: dict[str, Target] = {}
    for raw in raw_targets:
        if not isinstance(raw, dict):
            raise ValueError("each target must be an object")
        name = raw.get("name")
        command = raw.get("command")
        if not isinstance(name, str) or not name:
            raise ValueError("target name must be a non-empty string")
        if name in targets:
            raise ValueError(f"duplicate target: {name}")
        if not isinstance(command, str) or not command:
            raise ValueError(f"target {name} command must be a non-empty string")

        env = raw.get("env") or {}
        if not isinstance(env, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in env.items()):
            raise ValueError(f"target {name} env must be a string map")

        targets[name] = Target(
            name=name,
            command=command,
            deps=_tuple_of_strings(raw.get("deps"), f"{name}.deps"),
            inputs=_tuple_of_strings(raw.get("inputs"), f"{name}.inputs"),
            outputs=_tuple_of_strings(raw.get("outputs"), f"{name}.outputs"),
            env=tuple(sorted(env.items())),
        )

    return BuildGraph(targets)

