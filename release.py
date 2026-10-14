#!/usr/bin/env python3
"""Package the release archives, patch files, and checksum list without a ROM."""

import argparse
import hashlib
import shutil
import sys
import zipfile
from pathlib import Path

import patch

URL = "https://github.com/afahy/ghost-babel-color-fix"
APC_IMAGES = (
    "before.png",
    "after.png",
    "eu-before.png",
    "eu-after.png",
    "jp-before.png",
    "jp-after.png",
)
CAMPBELL_IMAGES = (
    "campbell-before.png",
    "campbell-after.png",
    "campbell-before-mirrored.png",
    "campbell-after-mirrored.png",
)
SETS = (
    (
        "apc",
        "ghost-babel-apc-color-fix",
        "Primary APC-only patch set",
        "This set corrects Stage 2 APC colors in the yard outside Galuade fortress.\n"
        "It includes normal and thermal palette corrections.\n"
        "The optional APC + Campbell set adds Campbell's opening portrait correction.\n",
        APC_IMAGES,
    ),
    (
        "combined",
        "ghost-babel-apc-campbell-color-fixes",
        "Optional APC + Campbell patch set",
        "This set includes the APC correction and Campbell's opening portrait correction.\n"
        "It updates both Campbell portrait orientations and preserves Snake's colors "
        "and separate portrait fades.\n"
        "The original artist's intent remains uncertain; "
        "Campbell's correction offers an optional color interpretation.\n",
        APC_IMAGES + CAMPBELL_IMAGES,
    ),
)
INSTRUCTIONS = """Apply a patch:
1. Obtain your own clean ROM dump.
2. Start Floating IPS.
3. Select Apply Patch.
4. Select this set's BPS patch for your ROM's region.
5. Select your clean ROM dump.
6. Save the patched ROM as a separate file.
7. Start a fresh emulator session with the patched ROM.

Each patch requires a clean ROM without an added copier header.
Apply one selected patch set to the clean ROM.
The combined set includes both corrections and does not require the APC-only patch first.
BPS checks the source checksum.
IPS does not include a source checksum.
The package contains no game ROM.

Required source ROMs and expected outputs:
"""


def manifests(fix):
    paths = sorted(patch.manifest_dir(fix).glob("changes*.json"))
    return [patch.read_manifest(path) for path in paths]


def version():
    versions = {
        manifest["version"]
        for fix in ("apc", "campbell", "combined")
        for manifest in manifests(fix)
    }
    if len(versions) != 1:
        raise ValueError(f"The manifests use different versions: {', '.join(sorted(versions))}.")
    return versions.pop()


def readme(fix, title, description, release, tag):
    text = f"Metal Gear Solid: Ghost Babel Color Corrections v{release}\n{title}\n\n{description}\n"
    text += INSTRUCTIONS
    for manifest in manifests(fix):
        text += f"\n{manifest['region']}\nSource: {manifest['source_filename']}\n"
        text += f"Size: {manifest['source']['size']} bytes\n"
        text += f"Source CRC32: {manifest['source']['crc32']}\n"
        text += f"Target SHA-256: {manifest['target']['sha256']}\n"
        text += f"Patch: {manifest['patch_name']}.bps\n"
    text += "\nValidation:\n"
    text += "APC normal and thermal rendering and movement pass in PyBoy and SameBoy for all three regions.\n"
    if fix == "combined":
        text += "Campbell's USA introduction and gameplay pass in both emulators.\n"
        text += "Campbell's European and Japanese opening-scene checks pass in PyBoy.\n"
    text += "Floating IPS and Rom Patcher JS independently apply both formats to the expected targets.\n"
    text += "Physical Game Boy Color hardware remains untested.\n\n"
    text += "The images show the difference between the original and patched ROMs.\n"
    text += "SameBoy rendered the included screenshots directly from the ROMs.\n"
    text += "SHA256SUMS.txt identifies all six patch files in this package.\n"
    text += f"\nRepository: {URL}\nRelease: {URL}/releases/tag/{tag}\n"
    text += "\nThe license covers the patch tools and original documentation.\n"
    text += "It grants no rights to the original game or its graphics.\n"
    return text


def add(bundle, name, data):
    """Write one archive member with fixed metadata, so the same files give the same archive."""
    info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o644 << 16
    bundle.writestr(info, data)


def build(output_dir, tag=None):
    """Write the release assets into output_dir and return their paths."""
    release = version()
    if tag is not None and tag != f"v{release}":
        raise ValueError(f"Tag {tag} does not match the manifest version {release}.")
    tag = tag or f"v{release}"
    output_dir.mkdir(parents=True, exist_ok=True)
    archives, patches = [], []
    for fix, stem, title, description, images in SETS:
        directory = patch.manifest_dir(fix) / "patches"
        files = [
            directory / f"{manifest['patch_name']}.{extension}"
            for manifest in manifests(fix)
            for extension in ("bps", "ips")
        ]
        sums = (directory / "SHA256SUMS.txt").read_text(encoding="utf-8")
        for path in files:
            if f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}" not in sums:
                raise ValueError(f"{directory / 'SHA256SUMS.txt'} does not list {path.name}.")
        members = files + [directory / "SHA256SUMS.txt", patch.ROOT / "LICENSE"]
        members += [patch.ROOT / "images" / name for name in images]
        archive = output_dir / f"{stem}-v{release}.zip"
        with zipfile.ZipFile(archive, "w") as bundle:
            text = readme(fix, title, description, release, tag)
            add(bundle, "README.txt", text.encode("utf-8"))
            for path in members:
                if path.suffix.lower() in (".gb", ".gbc", ".sav", ".ram", ".state"):
                    raise ValueError(f"Refusing to package {path.name}.")
                add(bundle, path.name, path.read_bytes())
        archives.append(archive)
        for path in files:
            patches.append(output_dir / path.name)
            shutil.copyfile(path, patches[-1])
    assets = archives + patches
    checksums = output_dir / f"SHA256SUMS-v{release}.txt"
    lines = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n" for path in assets]
    checksums.write_bytes("".join(lines).encode("utf-8"))
    return assets + [checksums]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--tag", help="Stop unless the tag matches the manifest version.")
    args = parser.parse_args()
    for path in build(args.output_dir, args.tag):
        print(f"{path.name}: {path.stat().st_size} bytes")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
