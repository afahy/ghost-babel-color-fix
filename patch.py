#!/usr/bin/env python3
"""Apply or rebuild Ghost Babel color correction patches."""

import argparse
import hashlib
import json
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHECKSUM = 0x14E


class Manifest(dict):
    """A manifest object that names its file when a key is missing."""

    path = None

    def __missing__(self, key):
        raise ValueError(f"Invalid manifest {self.path}: no {key!r} key.")


def hashes(data):
    return {
        "size": len(data),
        "crc32": f"{zlib.crc32(data):08x}",
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def manifest_dir(fix):
    return ROOT if fix == "apc" else ROOT / fix


def read_manifest(path):
    def named(data):
        manifest = Manifest(data)
        manifest.path = path
        return manifest

    return json.loads(path.read_text(encoding="utf-8"), object_hook=named)


def load_manifest(fix, actual):
    paths = sorted(manifest_dir(fix).glob("changes*.json"))
    if not paths:
        raise ValueError(
            f"No changes*.json manifest exists in {manifest_dir(fix)}. "
            "Use a complete copy of the repository."
        )
    for path in paths:
        manifest = read_manifest(path)
        if actual == manifest["source"]:
            if "combines" in manifest:
                manifest["edits"] = combined_edits(manifest)
            return manifest
    raise ValueError(
        "Unsupported source ROM. Use a clean, unheadered USA, Europe, or Japan release. "
        f"Received SHA-256 {actual['sha256']}."
    )


def combined_edits(manifest):
    """Merge the edits of the combined fixes and compute one global checksum."""

    def offset(edit):
        return int(edit["offset"], 16)

    edits = []
    for fix in manifest["combines"]:
        edits += load_manifest(fix, manifest["source"])["edits"]
    checksums = [edit for edit in edits if offset(edit) == CHECKSUM]
    if not checksums:
        raise ValueError(f"Invalid manifest {manifest.path}: no checksum edit to combine.")
    edits = [edit for edit in edits if offset(edit) != CHECKSUM]
    before = checksums[0]["before"]
    value = int(before, 16)
    for edit in edits:
        value += sum(bytes.fromhex(edit["after"])) - sum(bytes.fromhex(edit["before"]))
    edits.append(
        {
            "name": "Global checksum for the combined corrections",
            "offset": f"{CHECKSUM:06x}",
            "before": before,
            "after": f"{value & 65535:04x}",
        }
    )
    return sorted(edits, key=offset)


def patched(source, manifest):
    target = bytearray(source)
    previous_end = 0
    for edit in manifest["edits"]:
        offset = int(edit["offset"], 16)
        before = bytes.fromhex(edit["before"])
        after = bytes.fromhex(edit["after"])
        if len(before) != len(after) or not before:
            raise ValueError(f"Invalid edit length: {edit['name']}")
        if offset < previous_end or offset + len(before) > len(source):
            raise ValueError(f"Overlapping or out-of-range edit: {edit['name']}")
        if source[offset : offset + len(before)] != before:
            raise ValueError(f"Original bytes differ: {edit['name']}")
        target[offset : offset + len(after)] = after
        previous_end = offset + len(before)
    target = bytes(target)
    if hashes(target) != manifest["target"]:
        raise ValueError("Target hashes differ from the manifest.")
    header_sum = 0
    for value in target[0x134:0x14D]:
        header_sum = (header_sum - value - 1) & 255
    global_sum = (sum(target) - target[0x14E] - target[0x14F]) & 65535
    if target[0x14D] != header_sum:
        raise ValueError("The target header checksum is invalid.")
    if int.from_bytes(target[0x14E:0x150], "big") != global_sum:
        raise ValueError("The target global checksum is invalid.")
    return target


def runs(source, target):
    start = 0
    while start < len(source):
        changed = source[start] != target[start]
        end = start + 1
        while end < len(source) and (source[end] != target[end]) == changed:
            end += 1
        yield start, end, changed
        start = end


def bps_number(value):
    result = bytearray()
    while True:
        low = value & 127
        value >>= 7
        if value == 0:
            result.append(low | 128)
            return result
        result.append(low)
        value -= 1


def make_bps(source, target):
    """Encode SourceRead and TargetRead actions from the BPS specification."""
    result = bytearray(b"BPS1")
    result += bps_number(len(source))
    result += bps_number(len(target))
    result += bps_number(0)
    for start, end, changed in runs(source, target):
        result += bps_number(((end - start - 1) << 2) | int(changed))
        if changed:
            result += target[start:end]
    result += struct.pack("<II", zlib.crc32(source), zlib.crc32(target))
    result += struct.pack("<I", zlib.crc32(result))
    return bytes(result)


def make_ips(edits):
    """Write each complete edit, because IPS cannot check the bytes that it skips."""
    result = bytearray(b"PATCH")
    for edit in edits:
        start = int(edit["offset"], 16)
        after = bytes.fromhex(edit["after"])
        for index in range(0, len(after), 65535):
            data = after[index : index + 65535]
            result += (start + index).to_bytes(3, "big")
            result += len(data).to_bytes(2, "big")
            result += data
    return bytes(result + b"EOF")


def write_sums(path, sums):
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    names = [line.split("  ", 1)[-1] for line in lines]
    for name, digest in sums.items():
        line = f"{digest}  {name}"
        if name in names:
            lines[names.index(name)] = line
        else:
            lines.append(line)
    path.write_bytes("".join(line + "\n" for line in lines).encode("utf-8"))


def main():
    fix_option = argparse.ArgumentParser(add_help=False)
    fix_option.add_argument(
        "--fix",
        choices=("apc", "campbell", "combined"),
        default=argparse.SUPPRESS,
        help=(
            "Select APC, Campbell, or both color corrections. "
            "Apply and verify default to apc; build defaults to apc and combined."
        ),
    )
    parser = argparse.ArgumentParser(description=__doc__, parents=[fix_option])
    commands = parser.add_subparsers(dest="command", required=True)
    verify = commands.add_parser(
        "verify", parents=[fix_option], help="Check the source ROM hashes."
    )
    verify.add_argument("rom", type=Path)
    apply = commands.add_parser(
        "apply", parents=[fix_option], help="Write the patched ROM locally."
    )
    apply.add_argument("rom", type=Path)
    apply.add_argument("output", type=Path)
    build = commands.add_parser(
        "build", parents=[fix_option], help="Rebuild BPS and IPS patch files."
    )
    build.add_argument("rom", type=Path)
    build.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    fix = getattr(args, "fix", None)
    source = args.rom.read_bytes()
    actual = hashes(source)
    if args.command == "build":
        for name in (fix,) if fix else ("apc", "combined"):
            manifest = load_manifest(name, actual)
            target = patched(source, manifest)
            output_dir = args.output_dir or manifest_dir(name) / "patches"
            output_dir.mkdir(parents=True, exist_ok=True)
            sums = {}
            for extension, data in (
                ("bps", make_bps(source, target)),
                ("ips", make_ips(manifest["edits"])),
            ):
                path = output_dir / f"{manifest['patch_name']}.{extension}"
                path.write_bytes(data)
                sums[path.name] = hashes(data)["sha256"]
                print(f"{path.name}: {len(data)} bytes; SHA-256 {sums[path.name]}")
            write_sums(output_dir / "SHA256SUMS.txt", sums)
        return
    manifest = load_manifest(fix or "apc", actual)
    if args.command == "verify":
        print(f"Source ROM verified: {manifest['region']}.")
        print(json.dumps(actual, indent=2))
        return
    target = patched(source, manifest)
    if args.rom.resolve() == args.output.resolve():
        raise ValueError("Use a separate output file.")
    with args.output.open("xb") as handle:
        handle.write(target)
    print(f"Patched ROM: {args.output}")
    print(f"SHA-256: {manifest['target']['sha256']}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
