"""JSON-backed pairing-credential store.

One entry per device, keyed by a friendly name the user picks at
pair-time. Storing the BLE address plus an opaque ``member_id`` is
enough to reconnect to the same device without re-running discovery.

File format (pretty-printed; one entry per device)::

    {
      "version": 1,
      "devices": {
        "bike": {
          "address": "F7:11:62:07:1F:F5",
          "device_name": "BSC200",
          "member_id": "ligpsport-7f31a8c2",
          "paired_at": "2026-05-12T20:42:00Z",
          "last_firmware": "May 14 2024 11:07:51"
        }
      }
    }

The default path follows the XDG basedir spec
(``$XDG_DATA_HOME/ligpsport/credentials.json``) with a graceful
fall-back to ``~/.local/share/ligpsport/credentials.json``.
"""

from __future__ import annotations

import contextlib
import dataclasses
import datetime as _dt
import json
import os
import stat
import tempfile
from pathlib import Path

FORMAT_VERSION = 1


def default_path() -> Path:
    """Return the default credential-store path (XDG-compliant)."""
    base = os.environ.get("XDG_DATA_HOME") or os.path.join(
        os.path.expanduser("~"), ".local", "share"
    )
    return Path(base) / "ligpsport" / "credentials.json"


@dataclasses.dataclass(slots=True)
class DeviceCredentials:
    """One stored pairing entry."""

    name: str
    address: str
    device_name: str = ""
    member_id: str = ""
    paired_at: str | None = None
    last_firmware: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return {
            "address": self.address,
            "device_name": self.device_name,
            "member_id": self.member_id,
            "paired_at": self.paired_at,
            "last_firmware": self.last_firmware,
        }


class CredentialStore:
    """JSON credential store keyed by friendly device name (e.g. ``"bike"``).

    Reads tolerate a missing or empty file; writes use a write-and-
    rename pattern so the file is never observed half-written. File
    permissions are restricted to the user (0600) since the
    ``member_id`` is the device's binding key.
    """

    def __init__(self, path: str | os.PathLike[str] | None = None) -> None:
        self.path = Path(path) if path is not None else default_path()

    def _read(self) -> dict[str, dict[str, str | None]]:
        try:
            raw = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return {}
        if not raw.strip():
            return {}
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError(f"{self.path}: malformed credential file")
        devices = data.get("devices", {})
        if not isinstance(devices, dict):
            raise ValueError(f"{self.path}: 'devices' is not an object")
        return devices

    def _entry_to_creds(self, name: str, entry: dict[str, str | None]) -> DeviceCredentials:
        return DeviceCredentials(
            name=name,
            address=str(entry.get("address", "")),
            device_name=str(entry.get("device_name", "")),
            member_id=str(entry.get("member_id", "")),
            paired_at=entry.get("paired_at"),
            last_firmware=entry.get("last_firmware"),
        )

    def get(self, name: str) -> DeviceCredentials | None:
        entries = self._read()
        entry = entries.get(name)
        if entry is None:
            return None
        return self._entry_to_creds(name, entry)

    def entries(self) -> list[DeviceCredentials]:
        return [self._entry_to_creds(name, entry) for name, entry in sorted(self._read().items())]

    def put(self, creds: DeviceCredentials) -> None:
        entries = self._read()
        if creds.paired_at is None:
            creds.paired_at = (
                _dt.datetime.now(tz=_dt.UTC)
                .replace(microsecond=0)
                .isoformat()
                .replace("+00:00", "Z")
            )
        entries[creds.name] = creds.to_dict()
        self._write(entries)

    def remove(self, name: str) -> bool:
        entries = self._read()
        if name not in entries:
            return False
        del entries[name]
        self._write(entries)
        return True

    def update_firmware(self, name: str, firmware: str) -> bool:
        entries = self._read()
        if name not in entries:
            return False
        entries[name]["last_firmware"] = firmware
        self._write(entries)
        return True

    def _write(self, devices: dict[str, dict[str, str | None]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload: dict[str, object] = {"version": FORMAT_VERSION, "devices": devices}
        fd, tmp_name = tempfile.mkstemp(
            prefix=".credentials-", suffix=".json.tmp", dir=str(self.path.parent)
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, indent=2, sort_keys=True)
                fh.write("\n")
            with contextlib.suppress(OSError):
                os.chmod(tmp_name, stat.S_IRUSR | stat.S_IWUSR)
            os.replace(tmp_name, self.path)
        except Exception:
            with contextlib.suppress(OSError):
                os.unlink(tmp_name)
            raise

    def __contains__(self, name: object) -> bool:
        return isinstance(name, str) and name in self._read()
