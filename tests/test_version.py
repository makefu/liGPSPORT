"""Sanity test that the package imports and exposes its version."""

from __future__ import annotations

import ligpsport


def test_version_is_a_string() -> None:
    assert isinstance(ligpsport.__version__, str)
    assert ligpsport.__version__.count(".") >= 1
