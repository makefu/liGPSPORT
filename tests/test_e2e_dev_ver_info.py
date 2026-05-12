"""End-to-end client ↔ simulator test over LoopbackTransport.

This is the no-mock proof-of-life: both halves traverse the real
framing codec, the real envelope router, and the real protobuf
modules. A regression in either direction surfaces here as a parse
error or a mismatched value — not as a mock-not-called assertion.
"""

from __future__ import annotations

from ligpsport.client import IgpsportClient
from ligpsport.proto import dev_ver_info_pb2
from ligpsport.simulator import Simulator, SimulatorState
from ligpsport.transport import make_loopback_pair


async def test_dev_ver_info_round_trip() -> None:
    client_t, peer_t = make_loopback_pair()
    state = SimulatorState(
        main_app_ver=0x07_45_03_00,
        ble_app_ver=0x03_02_01_00,
        protocol_ver=101,
        compile_time="2026-05-12 20:00:00",
    )
    async with Simulator(peer_t, state) as sim, IgpsportClient(client_t) as client:
        request = dev_ver_info_pb2.dev_ver_info_msg()
        request.operate_type = dev_ver_info_pb2.enum_OPERATE_TYPE_GET
        response = await client.request(request, timeout=2.0)

    # The simulator received exactly one frame.
    assert len(sim.state.received) == 1
    assert sim.state.received[0].service == 17  # DEV_VER_INFO
    assert sim.state.received[0].operation == 2  # OP_GET

    # The response decodes back to a populated version_msg.
    assert isinstance(response.message, dev_ver_info_pb2.dev_ver_info_msg)
    assert response.message.operate_type == dev_ver_info_pb2.enum_OPERATE_TYPE_SEND
    v = response.message.version_message
    assert v.main_app_ver == 0x07_45_03_00
    assert v.ble_app_ver == 0x03_02_01_00
    assert v.protocol_ver == 101
    assert v.compile_time == "2026-05-12 20:00:00"
