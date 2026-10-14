"""Check patch.py, release.py, and the committed manifests, patches, and checksum lists.

No test needs a game ROM. The command tests use a small synthetic ROM.
"""

import hashlib
import json
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile
import zlib
from pathlib import Path

import patch
import release

FIXES = ("apc", "campbell", "combined")
PATCH_NAME = re.compile(r"ghost-babel-[a-z-]+-v\d+(?:\.\d+)*\.(?:bps|ips)")
ARCHIVE_NAME = re.compile(r"ghost-babel-[a-z-]+-v\d+(?:\.\d+)*\.zip")
RELEASE_TAG = re.compile(r"releases/tag/(v\d+(?:\.\d+)*)")
ARCHIVE_DOWNLOAD = re.compile(r"releases/download/(v\d+(?:\.\d+)*)/[^)\s]+\.zip")


def manifests(fix):
    for path in sorted(patch.manifest_dir(fix).glob("changes*.json")):
        yield patch.load_manifest(fix, patch.read_manifest(path)["source"])


def documents():
    paths = [patch.ROOT / "readme.txt"]
    for pattern in ("*.md", "campbell/*.md", "combined/*.md"):
        paths += sorted(patch.ROOT.glob(pattern))
    return paths


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


def global_sum(data):
    return (sum(data) - data[0x14E] - data[0x14F]) & 65535


def write_fixture(root):
    """Write patch.py, a synthetic ROM, and APC, Campbell, and combined manifests into root.

    Return the source ROM and the target ROM of each fix.
    """
    source = bytearray(bytes(range(256)) * 256)
    source[0x134:0x14D] = b"SYNTHETIC".ljust(0x19, b"\0")
    header = 0
    for value in source[0x134:0x14D]:
        header = (header - value - 1) & 255
    source[0x14D] = header
    source[0x14E:0x150] = global_sum(source).to_bytes(2, "big")
    source = bytes(source)
    changes = {
        "apc": [(0x1000, b"\xaa\xbb\xcc\xdd"), (0x2000, b"\xff" + source[0x2001:0x2007] + b"\xff")],
        "campbell": [(0x3000, bytes(range(0x80, 0x88)))],
    }

    def target_of(*fixes):
        target = bytearray(source)
        for fix in fixes:
            for offset, data in changes[fix]:
                target[offset : offset + len(data)] = data
        target[0x14E:0x150] = global_sum(target).to_bytes(2, "big")
        return bytes(target)

    def manifest(name, target):
        return {
            "region": "Test",
            "patch_name": name,
            "source": patch.hashes(source),
            "target": patch.hashes(target),
        }

    targets = {"apc": target_of("apc"), "campbell": target_of("campbell")}
    targets["combined"] = target_of("apc", "campbell")
    files = {}
    for fix in ("apc", "campbell"):
        data = manifest(f"test-{fix}", targets[fix])
        data["edits"] = [
            {
                "name": "Checksum",
                "offset": "00014e",
                "before": source[0x14E:0x150].hex(),
                "after": targets[fix][0x14E:0x150].hex(),
            }
        ]
        data["edits"] += [
            {
                "name": f"Edit {offset:x}",
                "offset": f"{offset:06x}",
                "before": source[offset : offset + len(after)].hex(),
                "after": after.hex(),
            }
            for offset, after in changes[fix]
        ]
        files["changes.json" if fix == "apc" else f"{fix}/changes-us.json"] = data
    combined = manifest("test-combined", targets["combined"])
    combined["combines"] = ["apc", "campbell"]
    files["combined/changes-us.json"] = combined
    for name, data in files.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(json.dumps(data, indent=2), encoding="utf-8")
    shutil.copyfile(patch.ROOT / "patch.py", root / "patch.py")
    (root / "source.gbc").write_bytes(source)
    return source, targets


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


class CommandTests(unittest.TestCase):
    """Run a copy of patch.py against a synthetic ROM and synthetic manifests."""

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        # patch.py reports resolved paths, for example /private/var on macOS.
        self.root = Path(directory.name).resolve()
        self.source, self.targets = write_fixture(self.root)
        self.rom = self.root / "source.gbc"

    def run_tool(self, *args):
        command = [sys.executable, str(self.root / "patch.py"), *map(str, args)]
        return subprocess.run(command, capture_output=True, text=True, cwd=str(self.root))

    def assert_fails(self, result, message):
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(message, result.stderr)

    def test_verify(self):
        result = self.run_tool("verify", self.rom)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Source ROM verified: Test.", result.stdout)

    def test_apply_selects_the_fix_in_each_position(self):
        cases = [
            ("apc", ["apply", self.rom, "{out}"]),
            ("combined", ["--fix", "combined", "apply", self.rom, "{out}"]),
            ("combined", ["apply", "--fix", "combined", self.rom, "{out}"]),
            ("campbell", ["apply", self.rom, "{out}", "--fix", "campbell"]),
            ("campbell", ["--fix", "apc", "apply", "--fix", "campbell", self.rom, "{out}"]),
        ]
        for index, (fix, args) in enumerate(cases):
            output = self.root / f"out-{index}.gbc"
            with self.subTest(args=args):
                args = [output if arg == "{out}" else arg for arg in args]
                result = self.run_tool(*args)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(output.read_bytes(), self.targets[fix])

    def test_apply_keeps_existing_files(self):
        output = self.root / "out.gbc"
        output.write_bytes(b"keep")
        self.assert_fails(self.run_tool("apply", self.rom, output), "exists")
        self.assertEqual(output.read_bytes(), b"keep")
        self.assert_fails(self.run_tool("apply", self.rom, self.rom), "separate output file")
        self.assertEqual(self.rom.read_bytes(), self.source)

    def test_build(self):
        for _ in range(2):
            result = self.run_tool("build", self.rom)
            self.assertEqual(result.returncode, 0, result.stderr)
        for fix, directory in (("apc", "patches"), ("combined", "combined/patches")):
            directory = self.root / directory
            lines = (directory / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()
            files = sorted(
                path.name for path in directory.iterdir() if path.suffix in (".bps", ".ips")
            )
            self.assertEqual(sorted(line.split("  ", 1)[1] for line in lines), files)
            for line in lines:
                digest, name = line.split("  ", 1)
                self.assertEqual(
                    hashlib.sha256((directory / name).read_bytes()).hexdigest(), digest
                )
            bps = (directory / f"test-{fix}.bps").read_bytes()
            ips = (directory / f"test-{fix}.ips").read_bytes()
            with self.subTest(fix=fix):
                self.assertEqual(applied(bps_records(bps)[2], self.source), self.targets[fix])
                self.assertEqual(applied(ips_records(ips), self.source), self.targets[fix])
        self.assertFalse((self.root / "campbell" / "patches").exists())

    def test_errors(self):
        patched = self.root / "patched.gbc"
        patched.write_bytes(self.targets["apc"])
        self.assert_fails(self.run_tool("verify", patched), "Unsupported source ROM")
        shutil.rmtree(self.root / "campbell")
        self.assert_fails(
            self.run_tool("verify", "--fix", "campbell", self.rom), "No changes*.json"
        )
        manifest = self.root / "changes.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        del data["patch_name"]
        manifest.write_text(json.dumps(data), encoding="utf-8")
        result = self.run_tool("build", "--fix", "apc", self.rom)
        self.assert_fails(result, "no 'patch_name' key")
        self.assertIn(str(manifest), result.stderr)


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
        for path in documents():
            for digest in re.findall(r"\b[0-9a-f]{64}\b", path.read_text(encoding="utf-8")):
                with self.subTest(document=path.name):
                    self.assertIn(digest, known)


class ManifestRuleTests(unittest.TestCase):
    def test_versions(self):
        versions = {manifest["version"] for fix in FIXES for manifest in manifests(fix)}
        self.assertEqual(len(versions), 1, versions)
        (version,) = versions
        for fix in FIXES:
            for manifest in manifests(fix):
                self.assertTrue(
                    manifest["patch_name"].endswith(f"-v{version}"), manifest["patch_name"]
                )
        lines = (patch.ROOT / "readme.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[1], f"Version {version}")
        patch_files = {
            path.name for fix in FIXES for path in (patch.manifest_dir(fix) / "patches").iterdir()
        }
        for path in documents():
            text = path.read_text(encoding="utf-8")
            with self.subTest(document=path.name):
                for name in PATCH_NAME.findall(text):
                    self.assertIn(name, patch_files)
                for name in ARCHIVE_NAME.findall(text):
                    self.assertTrue(name.endswith(f"-v{version}.zip"), name)
                for tag in ARCHIVE_DOWNLOAD.findall(text):
                    self.assertEqual(tag, f"v{version}")
        for name in ("README.md", "readme.txt", "combined/README.md"):
            text = (patch.ROOT / name).read_text(encoding="utf-8")
            with self.subTest(release_link=name):
                self.assertIn(f"releases/tag/v{version}", text)
                if name != "README.md":
                    # README.md also links an earlier release on purpose.
                    self.assertEqual(set(RELEASE_TAG.findall(text)), {f"v{version}"})

    def test_regions_share_edits(self):
        for fix in ("apc", "campbell"):
            edit_lists = {
                manifest["region"]: [
                    (edit["offset"], edit["before"], edit["after"])
                    for edit in manifest["edits"]
                    if int(edit["offset"], 16) != patch.CHECKSUM
                ]
                for manifest in manifests(fix)
            }
            with self.subTest(fix=fix):
                self.assertEqual(len(edit_lists), 3)
                self.assertEqual(len({json.dumps(edits) for edits in edit_lists.values()}), 1)

    def test_edit_layout(self):
        # The combined manifests also show that the APC and Campbell edits do not overlap.
        for fix in FIXES:
            for manifest in manifests(fix):
                previous_end = 0
                for edit in manifest["edits"]:
                    offset = int(edit["offset"], 16)
                    before, after = bytes.fromhex(edit["before"]), bytes.fromhex(edit["after"])
                    with self.subTest(patch=manifest["patch_name"], edit=edit["name"]):
                        self.assertTrue(before)
                        self.assertEqual(len(before), len(after))
                        self.assertGreaterEqual(offset, previous_end)
                        self.assertLessEqual(offset + len(before), manifest["source"]["size"])
                    previous_end = offset + len(before)
                self.assertEqual(manifest["edits"][0]["offset"], f"{patch.CHECKSUM:06x}")
                self.assertEqual(len(bytes.fromhex(manifest["edits"][0]["after"])), 2)


class ReleaseTests(unittest.TestCase):
    def test_build(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            assets = release.build(Path(first))
            again = release.build(Path(second), f"v{release.version()}")
            self.assertEqual([path.name for path in assets], [path.name for path in again])
            for path, other in zip(assets, again):
                self.assertEqual(path.read_bytes(), other.read_bytes(), path.name)
            self.assertEqual(len(assets), 15)
            *files, checksums = assets
            lines = checksums.read_text(encoding="utf-8").splitlines()
            for path, line in zip(files, lines):
                self.assertEqual(
                    line, f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
                )
            for archive in files[:2]:
                with zipfile.ZipFile(archive) as bundle:
                    self.assertIsNone(bundle.testzip())
                    names = bundle.namelist()
                    self.assertEqual(names[0], "README.txt")
                    self.assertIn("SHA256SUMS.txt", names)
                    self.assertEqual(sum(name.endswith((".bps", ".ips")) for name in names), 6)

    def test_tag_must_match_the_version(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "does not match"):
                release.build(Path(directory), "v0.0.0")


if __name__ == "__main__":
    unittest.main()
