from __future__ import annotations

import unittest

from build_orchestrator.graph import BuildGraph, Target
from build_orchestrator.planner import plan_build


class PlannerTests(unittest.TestCase):
    def test_parallel_stages_are_deterministic(self) -> None:
        graph = BuildGraph(
            {
                "a": Target("a", "compile a"),
                "b": Target("b", "compile b"),
                "c": Target("c", "link", deps=("a", "b")),
            }
        )
        plan = plan_build(graph)
        self.assertEqual(plan.stages, (("a", "b"), ("c",)))

    def test_missing_dependency_fails(self) -> None:
        graph = BuildGraph({"a": Target("a", "compile", deps=("missing",))})
        with self.assertRaisesRegex(ValueError, "unknown target"):
            plan_build(graph)

    def test_cycle_fails(self) -> None:
        graph = BuildGraph(
            {
                "a": Target("a", "compile a", deps=("b",)),
                "b": Target("b", "compile b", deps=("a",)),
            }
        )
        with self.assertRaisesRegex(ValueError, "cycle detected"):
            plan_build(graph)

    def test_cache_key_changes_with_fingerprint(self) -> None:
        target = Target("a", "compile", inputs=("src/a.cc",))
        old = target.cache_key({"src/a.cc": "old"})
        new = target.cache_key({"src/a.cc": "new"})
        self.assertNotEqual(old, new)


if __name__ == "__main__":
    unittest.main()

