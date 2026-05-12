"""GATT service / characteristic UUIDs for the iGPSPORT BLE protocol.

The BSC200 (and the rest of the iGS / BSC family the iGPSPORT app
supports) expose four parallel Nordic-UART-style services. Each
service has a triple of RX (write, app→device), TX (notify,
device→app), and an enabling descriptor on the TX characteristic.
The trailing nibble of the UUID identifies which channel:

* **`8e`** — *Control* channel. The protobuf protocol documented in
  ``docs/PROTOCOL.md`` runs here. **This is the channel the library
  uses.** Mapped to ``ControlUARTManager`` in the app.
* `9e` — generic *Data* channel. Mapped to ``UARTManager``. Reserved
  for newer high-bandwidth flows; the BSC200 doesn't use it for
  control.
* `7e` — third channel (``ThirdUARTManager``); parallel file/firmware
  streams on newer models.
* `6e` — fourth channel (``FourthUARTManager``); same idea.

UUID values transcribed verbatim from
``com.igpsport.blelib.manager.{ControlUARTManager,UARTManager,
ThirdUARTManager,FourthUARTManager}`` in ``classes4.dex``.
"""

from __future__ import annotations

from typing import Final

# Primary control channel — the one the BSC200 needs for the
# documented protocol surface. Trailing nibble `8e`.
PRIMARY_SERVICE_UUID: Final[str] = "6e400001-b5a3-f393-e0a9-e50e24dcca8e"
PRIMARY_RX_UUID: Final[str] = "6e400002-b5a3-f393-e0a9-e50e24dcca8e"  # app -> device (write)
PRIMARY_TX_UUID: Final[str] = "6e400003-b5a3-f393-e0a9-e50e24dcca8e"  # device -> app (notify)

# Secondary data channel (UARTManager). Used by newer iGS models for
# generic data; the BSC200 advertises it but the library doesn't
# transit control traffic on it.
DATA_SERVICE_UUID: Final[str] = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
DATA_RX_UUID: Final[str] = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
DATA_TX_UUID: Final[str] = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

# Third channel (ThirdUARTManager). Parallel file/firmware streams.
THIRD_SERVICE_UUID: Final[str] = "6e400001-b5a3-f393-e0a9-e50e24dcca7e"
THIRD_RX_UUID: Final[str] = "6e400002-b5a3-f393-e0a9-e50e24dcca7e"
THIRD_TX_UUID: Final[str] = "6e400003-b5a3-f393-e0a9-e50e24dcca7e"

# Fourth channel (FourthUARTManager). Same purpose as Third.
FOURTH_SERVICE_UUID: Final[str] = "6e400001-b5a3-f393-e0a9-e50e24dcca6e"
FOURTH_RX_UUID: Final[str] = "6e400002-b5a3-f393-e0a9-e50e24dcca6e"
FOURTH_TX_UUID: Final[str] = "6e400003-b5a3-f393-e0a9-e50e24dcca6e"

# Advertising-name prefixes the BSC200/iGS family use. The library's
# scanner filters on these; the MAC is incidental.
NAME_PREFIXES: Final[tuple[str, ...]] = ("BSC", "iGS", "iGPSPORT")
