{
  description = "ligpsport — Python BLE interface for iGPSPORT cycling computers (BSC200 and family)";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python313;
        # The package's check phase runs ruff (lint + format) and the
        # pytest suite. mypy lives in a separate `checks.mypy` derivation
        # (below) because buildPythonPackage populates PYTHONPATH with
        # site-packages dirs that mask the source tree, breaking
        # relative-import resolution inside the package — running mypy
        # standalone, outside that env, sidesteps the issue.
        package = python.pkgs.buildPythonPackage {
          pname = "ligpsport";
          version = "1.0.0";
          src = ./.;
          pyproject = true;
          build-system = [ python.pkgs.setuptools ];
          dependencies = [
            python.pkgs.bleak
            python.pkgs.protobuf
            # dbus-fast is the BlueZ-direct backend's only runtime
            # dependency. It's also a transitive dep of bleak on Linux,
            # so this only widens the wheel metadata, not the runtime
            # closure.
            python.pkgs.dbus-fast
          ];
          nativeBuildInputs = [ pkgs.ruff ];
          nativeCheckInputs = [
            python.pkgs.pytestCheckHook
            python.pkgs.pytest-asyncio
            # fitparse is read-only — used by tests to verify our FIT
            # course encoder round-trips. Not a runtime dependency.
            python.pkgs.fitparse
          ];
          enabledTestPaths = [ "tests" ];
          pytestFlags = [ "-q" ];
          preBuild = ''
            echo "==> ruff check"
            ruff check ligpsport/ tests/
            echo "==> ruff format --check"
            ruff format --check ligpsport/ tests/
          '';
          doCheck = true;
          meta = {
            description = "Python BLE interface for iGPSPORT cycling computers (BSC200 family)";
            mainProgram = "ligpsport";
          };
        };
        # mypy on the library. Runs outside the buildPythonPackage env so
        # its PYTHONPATH manipulation doesn't mask the source tree.
        mypyCheck = pkgs.runCommand "ligpsport-mypy"
          {
            nativeBuildInputs = [
              (python.withPackages (ps: [
                ps.mypy
                ps.bleak
                ps.protobuf
                ps.types-protobuf
                ps.dbus-fast
              ]))
            ];
            src = ./.;
          } ''
            cp -R "$src" workdir
            chmod -R u+w workdir
            cd workdir
            mypy --strict ligpsport/
            touch $out
          '';
        # Helper script for regenerating the protobuf modules from
        # `reference/*.proto`. Run via `nix run .#gen-proto`. After
        # invoking protoc we rewrite the generated absolute imports
        # (`import common_pb2 as ...`) into package-relative form
        # (`from . import common_pb2 as ...`) so the modules are usable
        # under the `ligpsport.proto` namespace.
        genProto = pkgs.writeShellApplication {
          name = "ligpsport-gen-proto";
          runtimeInputs = [ pkgs.protobuf pkgs.gnused ];
          text = ''
            set -euo pipefail
            REPO_ROOT="''${REPO_ROOT:-$(pwd)}"
            OUT_DIR="$REPO_ROOT/ligpsport/proto"
            REF_DIR="$REPO_ROOT/reference"
            mkdir -p "$OUT_DIR"
            (
              cd "$REF_DIR"
              # shellcheck disable=SC2046
              protoc --proto_path=. --python_out="$OUT_DIR" $(ls ./*.proto)
            )
            for f in "$OUT_DIR"/*_pb2.py; do
              sed -i -E 's/^import (.+_pb2)( as .+)?$/from . import \1\2/' "$f"
            done
            echo "Generated protobuf modules into $OUT_DIR"
          '';
        };
      in {
        packages.default = package;
        packages.ligpsport = package;
        apps.default = flake-utils.lib.mkApp { drv = package; };
        apps.gen-proto = flake-utils.lib.mkApp { drv = genProto; };
        # `nix flake check` builds the package (ruff + pytest) AND the
        # standalone mypy derivation. Together they exercise the full
        # QA gate that CI runs.
        checks.default = package;
        checks.mypy = mypyCheck;
        devShells.default = pkgs.mkShell {
          packages = [
            (python.withPackages (ps: [
              ps.pytest
              ps.pytest-asyncio
              ps.bleak
              ps.protobuf
              ps.types-protobuf
              ps.dbus-fast
              ps.fitparse
              ps.mypy
            ]))
            pkgs.ruff
            pkgs.protobuf
            # Useful for live debugging
            pkgs.bluez
          ];
        };
      });
}
