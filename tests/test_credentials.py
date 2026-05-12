"""Tests for the JSON-backed credential store."""

from __future__ import annotations

from pathlib import Path

import pytest

from ligpsport.credentials import CredentialStore, DeviceCredentials


@pytest.fixture
def store(tmp_path: Path) -> CredentialStore:
    return CredentialStore(path=tmp_path / "credentials.json")


def test_empty_store_returns_nothing(store: CredentialStore) -> None:
    assert store.entries() == []
    assert store.get("bike") is None
    assert "bike" not in store


def test_put_and_get(store: CredentialStore) -> None:
    creds = DeviceCredentials(
        name="bike",
        address="F7:11:62:07:1F:F5",
        device_name="BSC200",
        member_id="ligpsport-test",
    )
    store.put(creds)
    out = store.get("bike")
    assert out is not None
    assert out.address == "F7:11:62:07:1F:F5"
    assert out.device_name == "BSC200"
    assert out.member_id == "ligpsport-test"
    # paired_at is populated by put().
    assert out.paired_at is not None
    assert out.paired_at.endswith("Z")


def test_update_firmware(store: CredentialStore) -> None:
    store.put(DeviceCredentials(name="bike", address="aa:bb"))
    assert store.update_firmware("bike", "May 14 2024 11:07:51")
    assert store.get("bike").last_firmware == "May 14 2024 11:07:51"  # type: ignore[union-attr]


def test_remove(store: CredentialStore) -> None:
    store.put(DeviceCredentials(name="bike", address="aa:bb"))
    assert store.remove("bike")
    assert "bike" not in store
    assert not store.remove("bike")  # idempotent


def test_atomic_write_creates_secure_file(store: CredentialStore, tmp_path: Path) -> None:
    store.put(DeviceCredentials(name="bike", address="aa:bb"))
    mode = (store.path.stat().st_mode) & 0o777
    assert mode == 0o600  # auth_hash / member_id are secrets


def test_multiple_entries_persist(store: CredentialStore) -> None:
    store.put(DeviceCredentials(name="bike1", address="aa:01"))
    store.put(DeviceCredentials(name="bike2", address="aa:02"))
    names = [c.name for c in store.entries()]
    assert names == ["bike1", "bike2"]  # alphabetical
