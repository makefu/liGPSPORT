"""Python BLE interface for iGPSPORT cycling computers (BSC200 family).

Reverse-engineered from the iGPSPORT Android APK. Layered as:

* :mod:`ligpsport.framing`     -- 20-byte header + CRC8 codec used at the
  byte level on top of BLE. Self-symmetric, shared by client and the
  in-tree simulator so encoding regressions surface on both halves.
* :mod:`ligpsport.envelope`    -- routes each service_type_index to its
  protobuf message class; serialises/deserialises the payload that goes
  inside the framing header.
* :mod:`ligpsport.transport`   -- ``TransportInterface`` ABC plus
  ``BleakTransport`` (real device) and ``LoopbackTransport`` (in-process
  peer the simulator uses).
* :mod:`ligpsport.discovery`   -- BLE scan filtered to the iGS/BSC/iGPSPORT
  advertising-name prefixes.
* :mod:`ligpsport.client`      -- ``IgpsportClient`` async API: connect,
  pair, structured request/response, notification stream.
* :mod:`ligpsport.commands`    -- named-command registry; the entry point
  for ``ligpsport command info`` and library callers alike.
* :mod:`ligpsport.simulator`   -- in-process peer over LoopbackTransport;
  used by the test suite to exercise the client end-to-end without a
  physical device.
* :mod:`ligpsport.credentials` -- XDG-compliant JSON store of pairing
  state.
"""

__version__ = "1.0.0"
