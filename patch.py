#!/usr/bin/env python3
"""Apply or rebuild the isolated Ghost Babel APC color patch."""

import argparse
import hashlib
import json
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PATCH_NAME = "ghost-babel-tank-color-fix-v1.0"


def hashes(data):
    return {
        "size": len(data),
        "crc32": f"{zlib.crc32(data):08x}",
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def load_source(path, manifest_dir=ROOT):
    data = path.read_bytes()
    actual = hashes(data)
    for manifest_path in sorted(manifest_dir.glob("changes*.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if actual == manifest["source"]:
            return data, manifest
    raise ValueError(
        "Unsupported source ROM. Use a clean, unheadered USA, Europe, or Japan release. "
        f"Received SHA-256 {actual['sha256']}."
    )


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


def make_ips(source, target):
    result = bytearray(b"PATCH")
    for start, end, changed in runs(source, target):
        if not changed:
            continue
        while start < end:
            stop = min(end, start + 65535)
            result += start.to_bytes(3, "big")
            result += (stop - start).to_bytes(2, "big")
            result += target[start:stop]
            start = stop
    return bytes(result + b"EOF")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fix",
        choices=("apc", "campbell"),
        default="apc",
        help="Select the color correction. The default is apc.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    verify = commands.add_parser("verify", help="Check the source ROM hashes.")
    verify.add_argument("rom", type=Path)
    apply = commands.add_parser("apply", help="Write the patched ROM locally.")
    apply.add_argument("rom", type=Path)
    apply.add_argument("output", type=Path)
    build = commands.add_parser("build", help="Rebuild BPS and IPS patch files.")
    build.add_argument("rom", type=Path)
    build.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    manifest_dir = ROOT if args.fix == "apc" else ROOT / "campbell"
    source, manifest = load_source(args.rom, manifest_dir)
    if args.command == "verify":
        print(f"Source ROM verified: {manifest.get('region', 'USA')}.")
        print(json.dumps(hashes(source), indent=2))
        return
    target = patched(source, manifest)
    if args.command == "apply":
        if args.rom.resolve() == args.output.resolve():
            raise ValueError("Use a separate output file.")
        with args.output.open("xb") as handle:
            handle.write(target)
        print(f"Patched ROM: {args.output}")
        print(f"SHA-256: {hashes(target)['sha256']}")
        return
    output_dir = args.output_dir or manifest_dir / "patches"
    output_dir.mkdir(parents=True, exist_ok=True)
    patch_name = manifest.get("patch_name", PATCH_NAME)
    for extension, maker in (("bps", make_bps), ("ips", make_ips)):
        path = output_dir / f"{patch_name}.{extension}"
        data = maker(source, target)
        path.write_bytes(data)
        print(f"{path.name}: {len(data)} bytes; SHA-256 {hashes(data)['sha256']}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
