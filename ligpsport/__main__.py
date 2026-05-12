"""CLI entry point for ``ligpsport``.

The CLI is intentionally thin: it parses arguments, looks up the right
command in :mod:`ligpsport.commands`, and prints the result. All
business logic lives in the library; see ``AGENTS.md`` §4.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from typing import TYPE_CHECKING, Final

from . import __version__

if TYPE_CHECKING:
    from collections.abc import Sequence


EXIT_OK: Final[int] = 0
EXIT_USAGE: Final[int] = 2
EXIT_NOT_FOUND: Final[int] = 3
EXIT_DESTRUCTIVE_BLOCKED: Final[int] = 4


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ligpsport",
        description="BLE interface for iGPSPORT cycling computers (BSC200 family).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--store",
        help="credential JSON path (default: $XDG_DATA_HOME/ligpsport/credentials.json)",
    )
    sub = parser.add_subparsers(dest="cmd")
    sub.required = False

    disc = sub.add_parser("discover", help="scan for iGPSPORT devices over BLE")
    disc.add_argument("--timeout", type=float, default=6.0, help="scan length in seconds")
    disc.add_argument("--json", action="store_true", help="JSON output")

    pair = sub.add_parser("pair", help="persist credentials for a device")
    pair.add_argument("address", help="BLE address (MAC) of the device")
    pair.add_argument("--name", required=True, help="friendly name to store under")
    pair.add_argument("--device-name", default="", help="advertised device name (optional)")
    pair.add_argument("--member-id", default="", help="member_id for the BLE bond (optional)")

    creds = sub.add_parser("creds", help="list / remove stored credentials")
    creds.add_argument("--delete", help="remove the entry with this name")
    creds.add_argument("--json", action="store_true", help="JSON output")

    cmd = sub.add_parser("command", help="run a named library command against a stored device")
    cmd.add_argument("--name", help="stored credential name to target")
    cmd.add_argument("--address", help="bypass credentials; connect directly to this MAC")
    cmd.add_argument("--list", action="store_true", help="list available commands")
    cmd.add_argument("--json", action="store_true", help="emit result as JSON")
    cmd.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="per-request timeout (seconds); default 10",
    )
    cmd.add_argument(
        "--watch",
        type=float,
        default=None,
        metavar="SECS",
        help="for status: stream live updates for this many seconds (default 30)",
    )
    cmd.add_argument(
        "--allow-destructive-commands",
        action="store_true",
        help="run commands that mutate persistent device state (see AGENTS.md §2)",
    )
    cmd.add_argument("operation", nargs="?", help="command name (e.g. 'version')")
    cmd.add_argument("args", nargs=argparse.REMAINDER, help="command arguments")

    return parser


def _format_devices_text(devices: object) -> str:
    from .discovery import Device  # local import to keep CLI lightweight

    assert isinstance(devices, list)
    if not devices:
        return "no iGPSPORT devices found"
    lines = []
    for dev in devices:
        assert isinstance(dev, Device)
        rssi = f"  rssi={dev.rssi}" if dev.rssi is not None else ""
        lines.append(f"{dev.address}  {dev.name}{rssi}")
    return "\n".join(lines)


async def _cmd_discover(args: argparse.Namespace) -> int:
    from .discovery import discover

    devices = await discover(timeout=args.timeout)
    if args.json:
        print(json.dumps([d.to_dict() for d in devices], indent=2))
    else:
        print(_format_devices_text(devices))
    return EXIT_OK if devices else EXIT_NOT_FOUND


def _cmd_pair(args: argparse.Namespace) -> int:
    from .credentials import CredentialStore, DeviceCredentials

    store = CredentialStore(path=args.store)
    creds = DeviceCredentials(
        name=args.name,
        address=args.address,
        device_name=args.device_name,
        member_id=args.member_id,
    )
    store.put(creds)
    print(f"stored credentials for {args.name!r} -> {args.address}")
    return EXIT_OK


def _cmd_creds(args: argparse.Namespace) -> int:
    from .credentials import CredentialStore

    store = CredentialStore(path=args.store)
    if args.delete:
        removed = store.remove(args.delete)
        if not removed:
            print(f"no credential entry named {args.delete!r}", file=sys.stderr)
            return EXIT_NOT_FOUND
        print(f"removed {args.delete!r}")
        return EXIT_OK
    entries = store.entries()
    if args.json:
        print(json.dumps([{"name": c.name, **c.to_dict()} for c in entries], indent=2))
    else:
        if not entries:
            print("no stored credentials")
            return EXIT_NOT_FOUND
        for c in entries:
            fw = f" fw={c.last_firmware}" if c.last_firmware else ""
            print(f"{c.name}  {c.address}  {c.device_name}{fw}")
    return EXIT_OK


async def _cmd_command(args: argparse.Namespace) -> int:
    import asyncio as _asyncio

    from . import commands
    from .ble import BleakTransport
    from .client import IgpsportClient
    from .credentials import CredentialStore
    from .proto import common_pb2, dev_status_pb2

    if args.list:
        for spec in commands.list_commands():
            danger = "  [destructive]" if spec.destructive else ""
            print(f"{spec.name:<16}{spec.description}{danger}")
        return EXIT_OK

    if not args.operation:
        print("error: missing command name (try --list)", file=sys.stderr)
        return EXIT_USAGE

    # Refuse destructive commands BEFORE opening the BLE link so we
    # don't leak a connection just to print a refusal.
    try:
        spec = commands.get_command(args.operation)
    except commands.UnknownCommandError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_USAGE
    if spec.destructive and not args.allow_destructive_commands:
        print(
            f"error: command {args.operation!r} is destructive "
            f"({spec.danger}); pass --allow-destructive-commands",
            file=sys.stderr,
        )
        return EXIT_DESTRUCTIVE_BLOCKED

    address = args.address
    if address is None:
        if not args.name:
            print("error: pass --address or --name <stored>", file=sys.stderr)
            return EXIT_USAGE
        store = CredentialStore(path=args.store)
        creds = store.get(args.name)
        if creds is None:
            print(f"no stored credential for {args.name!r}", file=sys.stderr)
            return EXIT_NOT_FOUND
        address = creds.address

    try:
        async with BleakTransport(address) as transport, IgpsportClient(transport) as client:
            if args.watch is not None and args.operation == "status":
                # Stream DEV_STATUS notifications. The device sends them
                # unsolicited while a ride is active; otherwise we poll
                # explicitly every second.
                deadline = _asyncio.get_running_loop().time() + (args.watch or 30.0)
                while _asyncio.get_running_loop().time() < deadline:
                    result = await commands.run_named(
                        client,
                        args.operation,
                        args.args,
                        timeout=args.timeout,
                    )
                    if args.json:
                        print(json.dumps(result.to_dict()))
                    else:
                        print(result.format())
                        print("---")
                    await _asyncio.sleep(1.0)
                return EXIT_OK

            result = await commands.run_named(
                client,
                args.operation,
                args.args,
                timeout=args.timeout,
                allow_destructive=args.allow_destructive_commands,
            )
    except commands.DestructiveCommandError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_DESTRUCTIVE_BLOCKED

    _ = common_pb2  # silence imports when --watch is not used
    _ = dev_status_pb2
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(result.format())
    return EXIT_OK


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd is None:
        parser.print_help()
        return EXIT_OK
    if args.cmd == "discover":
        return asyncio.run(_cmd_discover(args))
    if args.cmd == "pair":
        return _cmd_pair(args)
    if args.cmd == "creds":
        return _cmd_creds(args)
    if args.cmd == "command":
        return asyncio.run(_cmd_command(args))
    parser.error(f"unknown subcommand: {args.cmd!r}")
    return EXIT_USAGE  # unreachable; argparse exits


if __name__ == "__main__":
    sys.exit(main())
