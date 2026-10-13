METAL GEAR SOLID: GHOST BABEL COLOR CORRECTIONS
Version 1.2.0
October 13, 2026
Author: Adam Fahy

This project provides color corrections for Metal Gear Solid on Game Boy Color, also known as Metal Gear: Ghost Babel.
The primary patch set corrects the Stage 2 APCs only.
The optional patch set includes both the APC and Campbell portrait corrections.
The repository contains no game ROM.

The APC correction changes two armored personnel carriers in Stage 2's yard outside Galuade fortress.
The corrected tiles use the hull's greens and preserve the surrounding sand.
Six brown shadow pixels become dark green to fit the room's available palettes.
The correction also fixes the thermal palette mapping.

The Campbell correction changes his portrait in the opening briefing.
It gives his face consistent skin colors and corrects parts of the collar and background.
Small shading changes let the portrait use ordinary background tiles and palettes.
The original artist's intent remains uncertain.
This correction offers an optional color interpretation; it does not establish a confirmed bug.

Both corrections change graphics and palette data without changing executable code.

PATCH SELECTION

Version 1.2.0 includes two release archives:
Primary APC-only: ghost-babel-apc-color-fix-v1.2.zip
Optional APC + Campbell: ghost-babel-apc-campbell-color-fixes-v1.2.zip

Each archive includes USA, European, and Japanese patches in BPS and IPS formats.
The filenames contain us, eu, or jp.
The primary set provides a version without Campbell's portrait correction.
The optional set contains both corrections in each patch.

Use the BPS patch that matches your chosen patch set and clean ROM dump.
The BPS patch checks the source checksum.
The IPS format does not include a source checksum.
Each patch requires a clean source ROM.
The standalone BPS files cannot be applied sequentially.

Primary APC-only patches are in patches/.
Optional combined patches are in combined/patches/.
combined/README.md describes the optional set and its target hashes.
campbell/README.md describes the portrait correction and retained Campbell-only tooling.
The earlier version 1.1.0 release contains the same APC correction only.

SUPPORTED SOURCES AND VERSION 1.2 TARGETS

Both patch sets use the clean source ROMs listed below.
The primary APC-only target bytes and hashes match version 1.1.
The optional combined target hashes include both corrections.

USA
Source: Metal Gear Solid (USA).gbc
Size: 2097152 bytes
Source CRC32: 04b0c5d6
Source MD5: f6dd1b1e5747412b9e5f25376c972d5a
Primary target CRC32: a3bd2abc
Primary target SHA-256: 245ea9cda899fe042d26a68a9429e789d15fddbcf38e8dbe7ade43c59db2d525
Optional combined target SHA-256: cfba270d86cec5185bfbd0ca6d600e39e5224f593aed59a790aaee78900274ce
Primary BPS: patches/ghost-babel-apc-color-fix-us-v1.2.bps
Optional BPS: combined/patches/ghost-babel-color-corrections-us-v1.2.bps

EUROPE
Source: Metal Gear Solid (Europe) (En,Fr,De,Es,It).gbc
Size: 4194304 bytes
Source CRC32: 16796957
Source MD5: 7971c95ad9745fe20df52e03cd52f636
Primary target CRC32: 4bc7796e
Primary target SHA-256: 9fb2e85c813bff77e76b317f7f94b9e7b49e088cc4d7255362bbdd317494bbdf
Optional combined target SHA-256: 97e01085822bce72f9e394aa73464198623c2193bbdf3e73d478990b9de9a5b9
Primary BPS: patches/ghost-babel-apc-color-fix-eu-v1.2.bps
Optional BPS: combined/patches/ghost-babel-color-corrections-eu-v1.2.bps

JAPAN
Source: Metal Gear - Ghost Babel (Japan).gbc
Size: 2097152 bytes
Source CRC32: 7831f84d
Source MD5: 7830328f323bd77d52a6985b1b10031f
Primary target CRC32: 80fedc50
Primary target SHA-256: 76407a78fb64b2c1648806a66f8439ec7b1aa4bb783df628d8577bbccda71025
Optional combined target SHA-256: 88e66f0e2340f4baa7f1991cb4344375cde74f672b9ed9464911680cb352f801
Primary BPS: patches/ghost-babel-apc-color-fix-jp-v1.2.bps
Optional BPS: combined/patches/ghost-babel-color-corrections-jp-v1.2.bps

Each listed BPS file has an IPS file with the same basename.

DESKTOP APPLICATION

1. Obtain your own clean regional ROM dump.
2. Download Floating IPS from https://github.com/Sir-Walrus/Flips/releases.
3. Start Floating IPS.
4. Select Apply Patch.
5. Select the BPS patch for your chosen patch set and ROM region.
6. Select your clean ROM dump.
7. Save the patched ROM as a separate file.
8. Start the patched ROM in your emulator or flash cartridge.

BROWSER APPLICATION

1. Open https://www.marcrobledo.com/RomPatcher.js/.
2. Select your clean dump in ROM file.
3. Select the matching patch set and regional BPS patch in Patch file.
4. Select Apply patch.
5. Save the patched ROM as a separate file.

Use a fresh emulator session to load the changed graphics and palettes.

PYTHON APPLICATION AND BUILDS

The included tool requires Python 3.8 or later and uses only the standard library.
It detects the source region and verifies source and target hashes.
The apply command selects APC-only when you omit --fix.
The --fix combined option selects the optional APC + Campbell set.

Apply the primary APC-only set:
python patch.py apply SOURCE_ROM OUTPUT_ROM

Apply the optional combined set:
python patch.py --fix combined apply SOURCE_ROM OUTPUT_ROM

Build both release patch sets:
python patch.py build SOURCE_ROM

Build one selected patch set:
python patch.py --fix apc build SOURCE_ROM
python patch.py --fix combined build SOURCE_ROM

Place --fix before the verify, apply, or build subcommand.
The default build writes APC-only files to patches/ and optional combined files to combined/patches/.
Each manifest records the edits and expected source and target hashes.
The build needs no assembler, disassembly project, or separate game assets.

SCREENSHOTS

The images show the difference between the original and patched ROMs.
The images/ directory contains the comparisons.
before.png and after.png show the USA APC correction.
eu-before.png and eu-after.png show the European APC correction.
jp-before.png and jp-after.png show the Japanese APC correction.
campbell-before.png and campbell-after.png show the USA Campbell correction.
campbell-before-mirrored.png and campbell-after-mirrored.png show Campbell's later mirrored portrait.

SameBoy rendered these images directly from the original and patched ROMs.
APC captures use RAM to select the same room, camera position, and player position.
Campbell captures use ordinary inputs from a cold boot.

VALIDATION AND COMPATIBILITY

The APC correction changes only the Stage 2 APC yard, with 384 corrected pixels per region.
APC checks covered all 496 valid rooms per region.
Normal and thermal movement checks passed in PyBoy and SameBoy for all three regions.

The USA Campbell correction passed the introduction, mirrored portrait, mission start, and player movement in PyBoy and SameBoy.
European and Japanese Campbell corrections passed shorter opening-scene checks in PyBoy.
Floating IPS applied every regional BPS and IPS release patch to its expected target hash.

The combined ROMs passed APC checks in both emulators for all regions.
They also passed the USA Campbell sequence and European and Japanese Campbell opening checks.
Physical Game Boy Color hardware and other patch combinations remain untested.

VALIDATION.md records the APC checks.
campbell/VALIDATION.md records the Campbell checks.
campbell/COMBINED_VALIDATION.md records the combined checks and their limits.

SOURCE AND UPDATES

Repository: https://github.com/afahy/ghost-babel-color-fix
Release: https://github.com/afahy/ghost-babel-color-fix/releases/tag/v1.2.0
Releases: https://github.com/afahy/ghost-babel-color-fix/releases

Ruff provides Python code checks and formatting.
GitHub Actions runs these checks without game ROMs.
The repository also includes technical notes and validation details.

CREDITS

Color corrections: Adam Fahy.
Original game: Konami.
The repository license covers the patch tools and original documentation.
It grants no rights to the original game or its graphics.
