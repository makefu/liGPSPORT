"""pytest fixtures shared across the test suite.

The two key fixtures are ``sim`` (a default-configured simulator over a
LoopbackTransport pair) and ``sim_factory`` (parameterised). Both will
fill in once :mod:`ligpsport.simulator` and :mod:`ligpsport.transport`
land. For now this file just keeps pytest happy and reserves the
fixture names.
"""

from __future__ import annotations
