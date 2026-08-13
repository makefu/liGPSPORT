# AGENTS.md

Instructions for AI assistants and human contributors working on
`ligpsport`. Read this before touching code.

## 1. The protocol is a reverse-engineered hostile target

The iGPSPORT BLE protocol is undocumented and not stable across
firmware generations. Every byte value, service index, header offset,
and CRC table cell in this repo was derived from one of:

* the iGPSPORT Android APK in `reference/` (extracted, plus a jadx
  decompile of `classes*.dex`),
* the protobuf `.proto` files shipped inside the APK,
* live BLE captures (btsnoop, Wireshark) against a real BSC200.

[`docs/PROTOCOL.md`](docs/PROTOCOL.md) is the **source of truth**.
When code reality differs from the doc, fix the doc — don't paper
over the code. Numbers there are observed, not guessed; if a
behaviour surprises you, suspect a firmware difference first.

The 20-byte header layout and CRC8 polynomial were transcribed from
`com.igpsport.blelib.pbfactory.CommonHead20Bytes` and
`com.igpsport.blelib.utils.CRC8` respectively. Both classes live in
the jadx output at `tmp/jadx-out/sources/com/igpsport/blelib/...`.
Cite those Java sources in commit messages when you adjust framing.

## 2. Destructive commands can lose data on the device

These operations alter persistent state on the bike computer —
erasing recorded activities, overwriting configuration that the user
spent time entering, or interrupting an in-progress flash:

* `FACTORY` service reset / RTC overwrite
* `FIRMWARE` / `PERIPHERAL_FIRMWARE` upgrade flows
* `CYCLING_DATA` file deletion
* `CONFIG` / `USER_CONFIG` / `SENSOR` mass writes
* `WIFI` SSID/key overwrites

Hard rules:

* **Never invoke a destructive operation against a real device "to
  see what happens".** Use the simulator first.
* **`ligpsport.commands.DESTRUCTIVE_PREFIXES` is the canonical list.**
  The simulator, the runtime gate, and any raw-payload escape hatch
  all read from it.
* **The simulator refuses destructive prefixes by default.** A test
  that needs to exercise the wire path must opt in with
  `allow_destructive=True`.
* **`run_named(..., allow_destructive=False)` is the default.** The
  CLI exposes the same gate as `--allow-destructive-commands`.
* **Speculative wire-format probes against the real device count as
  destructive even when the op itself isn't in `DESTRUCTIVE_PREFIXES`.**
  In particular: never send a non-default `file_tag` (offset 3 of the
  20-byte head — see `framing.FILE_TAG_*`) on a service it wasn't
  designed for. The BSC200 firmware classifies certain `file_tag`
  values as upload-stream markers (`0xAA` for FILE_OPERATION ADD,
  `0x55` for CYCLING_DATA FILE_GET transmit-complete) and will park
  its parser waiting for the rest of an upload that never arrives;
  the only recovery is a power-cycle. Verified the hard way 2026-05-15:
  a probe combining `op = FILE_DEL (5)` with `file_tag = 0xAA` on the
  third UART wedged the device for ~1 h. Always test new wire-format
  variants in the simulator first; if you must try them live, use
  the read-only services (DEV_VER_INFO / DEV_STATUS) and stick to
  the default `file_tag = 0xFF`.

When adding a new destructive command:

1. Mark `CommandSpec(destructive=True, danger="...")` with a danger
   string that explains *what* the command changes on the device AND
   *how to recover* if it bites (re-pair, re-flash, irreversible —
   be specific).
2. Add it to the parametrised list in `tests/test_commands.py` so
   both gating paths get exercised.

## 3. Tests use a real simulator over LoopbackTransport, not mocks

The `ligpsport.simulator` module is a real wire peer — it imports
the same `framing.py`, `envelope.py`, and protobuf modules the client
uses, so any encoding/decoding regression breaks both halves of the
suite at once. Connecting the two halves is `LoopbackTransport`, an
`asyncio.Queue` pair that delivers frame-shaped bytes (not parsed
messages) end-to-end.

Don't add `unittest.mock` or monkey-patches. If a behaviour can't be
expressed in the simulator (rare), extend the simulator itself.

Live-device tests (`tests/test_bsc200_live.py`) are marked
`@pytest.mark.bsc200` and skip unless `LIGPSPORT_DEVICE_ADDRESS` is
set. They cover non-destructive read paths only.

## 4. Library does the work; CLI is a thin shell

* Every result dataclass exposes `format()` (human pretty-print)
  and `to_dict()` (JSON-serialisable). The CLI calls these and
  prints — it never composes the output itself.
* The named-command registry (`ligpsport.commands`) is the single
  source of truth for what commands exist. The CLI and library
  consumers both go through `run_named(client, name, args)`.
* New CLI flags that imply business logic belong in the library
  first: add the kwarg to `run_named` and the data type's
  `to_dict`, then wire the flag in `__main__.py`.

## 5. `nix build .#default` is the single QA gate

The package's build derivation runs lint + tests as one pipeline,
and `nix flake check` adds the standalone mypy derivation:

1. `ruff check ligpsport/ tests/`
2. `ruff format --check ligpsport/ tests/`
3. `mypy --strict ligpsport/` (separate derivation, library only)
4. `pytest tests/ -q -m "not bsc200"`

Run `nix build .#default --print-build-logs` before every commit.
CI (`.github/workflows/ci.yml`) runs exactly those two commands on
every push to `main`, every tag and every PR.

Fix lint and type errors at the root, never with `# type: ignore`
or silencing. Generated protobuf modules under `ligpsport/proto/`
have an `ignore_errors` override in `pyproject.toml`; nothing else
gets a pass.

`nix run .#gen-proto` emits both `*_pb2.py` and `*_pb2.pyi`, and
**both are committed**. The stubs are what makes the rest of the
tree type-check: the runtime modules build their message classes
through the protobuf builder, so without stubs mypy reports every
message and enum as `Module has no attribute`. Never hand-edit
either — change the `.proto` and regenerate.

Protobuf enum fields are typed as their generated enum class (e.g.
`ROUTE_PLAN_FILE_TYPE`), which is an `int` subclass. Assigning a
bare `int` to one is a type error. Use the generated constant
(`route_plan_pb2.enum_ROUTE_PLAN_FILE_TYPE_CNX`) rather than a
literal; the enum wrappers are *not* callable at runtime, so
`ROUTE_PLAN_FILE_TYPE(2)` raises `TypeError`.

## 6. Naming, versioning, releases

* The project, the GitHub repo, the Nix flake attribute, the CLI
  script, and the credentials directory are all `ligpsport`.
* The Python module is also `ligpsport`.
* The version lives in **three** places. Bump in lockstep:
  * `ligpsport/__init__.py` (`__version__`)
  * `pyproject.toml` (`project.version`)
  * `flake.nix` (`buildPythonPackage.version`)
* SemVer. Breaking changes get a minor (0.X.0) bump while we're 0.y.
* Every release gets a CHANGELOG entry **before** tagging, in
  Keep-A-Changelog format with absolute dates.

## 7. Commit & changelog style

* Kernel-mailing style: subject in imperative, body explains
  **why** not what. The diff already shows what.
* Prefix subjects with `ligpsport: ` (or `README:`, `docs:`,
  `tests:` for narrow changes).
* One logical chunk per commit. Feature commits and release commits
  are separate.
* When risk is non-obvious, mention it in the commit message
  (destructive commands, breaking renames, file deletions).

## 8. Acting safely

* Don't run destructive commands against the real BSC200 to "test"
  — use the simulator.
* Don't push tags or create GitHub releases without explicit
  authorisation in the current turn.
* Don't commit the decompiled APK tree, `result` symlinks, or
  `tmp/` scratch — `.gitignore` covers these.
* Don't add `# type: ignore`, `# noqa`, or skip-flags to silence
  diagnostics. Fix the source.

## 9. When in doubt

* The simulator + the loopback transport reproduce the wire path
  in-memory; lean on them.
* The jadx output at `tmp/jadx-out/sources/` is the original truth
  for any header bit, service routing, or characteristic lookup.
* The protobuf `.proto` files in `reference/` are the schema of
  every payload; never invent field numbers.
