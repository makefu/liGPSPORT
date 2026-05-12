"""Generated protobuf modules for the iGPSPORT BLE protocol.

These are produced by ``nix run .#gen-proto`` from ``reference/*.proto``
and committed to the repo so the wheel build doesn't need ``protoc`` at
install time. Edit the ``.proto`` files in ``reference/`` and re-run the
generator rather than editing these modules by hand.

Each module corresponds to one ``service_type_index`` in
``common.proto`` (or to a shared message bundle like
``device_information``). The :mod:`ligpsport.envelope` module maps each
service index to its top-level message class here.
"""

from __future__ import annotations
