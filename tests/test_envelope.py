"""Tests for the service_type → message class router."""

from __future__ import annotations

import pytest

from ligpsport.envelope import (
    SERVICE_MESSAGES,
    UnknownServiceError,
    decode_payload,
    encode_message,
    message_class_for,
    service_type_for,
)
from ligpsport.proto import ble_pb2, common_pb2, dev_ver_info_pb2


def test_every_service_index_resolves_to_a_unique_message_class() -> None:
    # Catches accidental duplicates if someone copy-pastes a row.
    classes = list(SERVICE_MESSAGES.values())
    assert len(set(classes)) == len(classes)


def test_message_class_lookup() -> None:
    assert message_class_for(common_pb2.enum_SERVICE_TYPE_INDEX_BLE) is ble_pb2.ble_msg
    assert (
        message_class_for(common_pb2.enum_SERVICE_TYPE_INDEX_DEV_VER_INFO)
        is dev_ver_info_pb2.dev_ver_info_msg
    )


def test_unknown_service_raises() -> None:
    with pytest.raises(UnknownServiceError):
        message_class_for(99)


def test_encode_auto_populates_service_type() -> None:
    msg = ble_pb2.ble_msg()
    msg.ble_operate_type = ble_pb2.enum_BLE_OPERATE_TYPE_BOND_INFO
    # service_type is unset here; encode_message fills it in based on
    # SERVICE_MESSAGES so callers don't need to know the magic enum.
    service_type, payload = encode_message(msg)
    assert service_type == common_pb2.enum_SERVICE_TYPE_INDEX_BLE
    # The on-wire payload carries the service_type field.
    assert payload.startswith(bytes([0x08, common_pb2.enum_SERVICE_TYPE_INDEX_BLE]))


def test_encode_rejects_mismatched_service_type() -> None:
    msg = ble_pb2.ble_msg()
    msg.service_type = common_pb2.enum_SERVICE_TYPE_INDEX_DEV_STATUS  # wrong
    with pytest.raises(ValueError):
        encode_message(msg)


def test_round_trip_decodes_to_the_same_class() -> None:
    msg = ble_pb2.ble_msg()
    msg.ble_operate_type = ble_pb2.enum_BLE_OPERATE_TYPE_BOND_REQ
    service_type, payload = encode_message(msg)
    back = decode_payload(service_type, payload)
    assert isinstance(back, ble_pb2.ble_msg)
    assert back.ble_operate_type == ble_pb2.enum_BLE_OPERATE_TYPE_BOND_REQ


def test_service_type_for_reverse_lookup() -> None:
    assert service_type_for(ble_pb2.ble_msg) == common_pb2.enum_SERVICE_TYPE_INDEX_BLE
