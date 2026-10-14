"""Check patch.py and the committed manifests, patches, and checksum lists without a ROM."""

import hashlib
import re
import struct
import unittest
import zlib

import patch

FIXES = ("apc", "campbell", "combined")


def manifests(fix):
    for path in sorted(patch.manifest_dir(fix).glob("changes*.json")):
        yield patch.load_manifest(fix, patch.read_manifest(path)["source"])


def bps_records(data):
    """Decode a BPS patch that has only SourceRead and TargetRead actions."""
    position = 4

    def number():
        nonlocal position
        result, shift = 0, 1
        while True:
            value = data[position]
            position += 1
            result += (value & 127) * shift
            if value & 128:
                return result
            shift <<= 7
            result += shift

    sizes = (number(), number())
    metadata_size = number()
    position += metadata_size
    offset, records = 0, []
    while position < len(data) - 12:
        action = number()
        length = (action >> 2) + 1
        if action & 3 == 1:
            records.append((offset, bytes(data[position : position + length])))
            position += length
        elif action & 3:
            raise ValueError("Unexpected BPS action.")
        offset += length
    return sizes, struct.unpack("<III", data[-12:]), records


def ips_records(data):
    position, records = 5, []
    while position < len(data) - 3:
        offset = int.from_bytes(data[position : position + 3], "big")
        length = int.from_bytes(data[position + 3 : position + 5], "big")
        records.append((offset, bytes(data[position + 5 : position + 5 + length])))
        position += 5 + length
    return records


def changed_runs(edits):
    result = []
    for edit in edits:
        start = int(edit["offset"], 16)
        pairs = zip(bytes.fromhex(edit["before"]), bytes.fromhex(edit["after"]))
        for offset, (old, new) in enumerate(pairs, start):
            if old == new:
                continue
            if result and result[-1][0] + len(result[-1][1]) == offset:
                result[-1][1].append(new)
            else:
                result.append((offset, bytearray([new])))
    return [(offset, bytes(data)) for offset, data in result]


def applied(records, source):
    target = bytearray(source)
    for offset, data in records:
        target[offset : offset + len(data)] = data
    return bytes(target)


class FormatTests(unittest.TestCase):
    def test_bps_number(self):
        self.assertEqual(patch.bps_number(0), b"\x80")
        self.assertEqual(patch.bps_number(127), b"\xff")
        self.assertEqual(patch.bps_number(128), b"\x00\x80")

    def test_round_trip(self):
        source = bytes(range(256)) * 300
        long_edit = source[256:70256]
        edits = [
            {"offset": "000010", "before": "10111213", "after": "10ffff13"},
            {
                "offset": "000100",
                "before": long_edit.hex(),
                "after": bytes(value ^ 255 for value in long_edit).hex(),
            },
        ]
        target = bytearray(source)
        target[17:19] = b"\xff\xff"
        target[256:70256] = bytes.fromhex(edits[1]["after"])
        target = bytes(target)

        bps = patch.make_bps(source, target)
        sizes, crcs, records = bps_records(bps)
        self.assertEqual(sizes, (len(source), len(target)))
        self.assertEqual(crcs, (zlib.crc32(source), zlib.crc32(target), zlib.crc32(bps[:-4])))
        self.assertEqual(records, changed_runs(edits))
        self.assertEqual(applied(records, source), target)

        records = ips_records(patch.make_ips(edits))
        self.assertEqual([len(data) for _, data in records], [4, 65535, 4465])
        self.assertEqual(applied(records, source), target)

    def test_manifest_errors(self):
        with self.assertRaisesRegex(ValueError, "No changes"):
            patch.load_manifest("missing", {})
        with self.assertRaisesRegex(ValueError, "no 'target' key"):
            patch.Manifest()["target"]


class CommittedFileTests(unittest.TestCase):
    def test_patches_match_manifests(self):
        for fix in FIXES:
            for manifest in manifests(fix):
                name = manifest["patch_name"]
                directory = patch.manifest_dir(fix) / "patches"
                with self.subTest(patch=name):
                    ips = (directory / f"{name}.ips").read_bytes()
                    self.assertEqual(ips, patch.make_ips(manifest["edits"]))
                    bps = (directory / f"{name}.bps").read_bytes()
                    sizes, crcs, records = bps_records(bps)
                    source, target = manifest["source"], manifest["target"]
                    self.assertEqual(sizes, (source["size"], target["size"]))
                    self.assertEqual(
                        [f"{crc:08x}" for crc in crcs],
                        [source["crc32"], target["crc32"], f"{zlib.crc32(bps[:-4]):08x}"],
                    )
                    self.assertEqual(records, changed_runs(manifest["edits"]))

    def test_checksum_edits(self):
        for fix in FIXES:
            for manifest in manifests(fix):
                checksum, *edits = manifest["edits"]
                value = int(checksum["before"], 16)
                for edit in edits:
                    value += sum(bytes.fromhex(edit["after"])) - sum(bytes.fromhex(edit["before"]))
                with self.subTest(patch=manifest["patch_name"]):
                    self.assertEqual(int(checksum["offset"], 16), patch.CHECKSUM)
                    self.assertEqual(int(checksum["after"], 16), value & 65535)

    def test_checksum_lists(self):
        for fix in FIXES:
            directory = patch.manifest_dir(fix) / "patches"
            lines = (directory / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
            listed = {name: digest for digest, name in (line.split("  ", 1) for line in lines)}
            files = {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in directory.iterdir()
                if path.suffix in (".bps", ".ips")
            }
            with self.subTest(fix=fix):
                self.assertEqual(listed, files)

    def test_document_hashes(self):
        known = set()
        for fix in FIXES:
            for manifest in manifests(fix):
                known |= {manifest["source"]["sha256"], manifest["target"]["sha256"]}
        documents = [patch.ROOT / "readme.txt"]
        for pattern in ("*.md", "campbell/*.md", "combined/*.md"):
            documents += sorted(patch.ROOT.glob(pattern))
        for path in documents:
            for digest in re.findall(r"\b[0-9a-f]{64}\b", path.read_text(encoding="utf-8")):
                with self.subTest(document=path.name):
                    self.assertIn(digest, known)


if __name__ == "__main__":
    unittest.main()
