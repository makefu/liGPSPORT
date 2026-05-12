"""Smoke tests for the generated protobuf modules.

These don't exercise the BLE protocol; they only confirm that the
``nix run .#gen-proto`` output works as a Python package and that
the service-type indices line up with ``reference/common.proto``.
"""

from __future__ import annotations

from ligpsport.proto import ble_pb2, common_pb2, dev_ver_info_pb2


def test_service_type_indices_match_proto_file() -> None:
    # Spot-check a few well-known indices against common.proto. If the
    # protoc output drifts (e.g. someone reorders the enum), this test
    # catches it before the codec tries to dispatch on a wrong value.
    assert common_pb2.enum_SERVICE_TYPE_INDEX_BLE == 10
    assert common_pb2.enum_SERVICE_TYPE_INDEX_DEV_STATUS == 13
    assert common_pb2.enum_SERVICE_TYPE_INDEX_DEV_VER_INFO == 17
    assert common_pb2.enum_SERVICE_TYPE_INDEX_FILE_OPERATION == 21
    assert common_pb2.enum_SERVICE_TYPE_INDEX_ROUTE_BOOK == 23


def test_ble_msg_round_trip() -> None:
    msg = ble_pb2.ble_msg()
    msg.service_type = common_pb2.enum_SERVICE_TYPE_INDEX_BLE
    msg.ble_operate_type = ble_pb2.enum_BLE_OPERATE_TYPE_BOND_INFO
    blob = msg.SerializeToString()

    back = ble_pb2.ble_msg()
    back.ParseFromString(blob)
    assert back.service_type == common_pb2.enum_SERVICE_TYPE_INDEX_BLE
    assert back.ble_operate_type == ble_pb2.enum_BLE_OPERATE_TYPE_BOND_INFO


def test_dev_ver_info_default_protocol_version() -> None:
    # `version_msg.protocol_ver` defaults to 101 (cited as "V1.01" in
    # dev_ver_info.proto). The library treats this as a sanity floor;
    # anything that round-trips through the BSC200 should report >= 101.
    v = dev_ver_info_pb2.version_msg()
    assert v.protocol_ver == 101
