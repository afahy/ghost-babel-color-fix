METAL GEAR SOLID: GHOST BABEL COLOR CORRECTIONS
October 13, 2026
Author: Adam Fahy

This project provides color corrections for Metal Gear Solid on Game Boy Color, also known as Metal Gear: Ghost Babel.

APC v1.1 corrects two armored personnel carriers in Stage 2's yard outside Galuade fortress.
The corrected tiles use the hull's greens and preserve the surrounding sand.
Six brown shadow pixels become dark green to fit the room's available palettes.
The correction also fixes the thermal palette mapping.

The experimental Campbell correction changes his portrait in the opening briefing.
It gives his face consistent skin colors and corrects parts of the collar and background.
Small shading changes let the portrait use ordinary background tiles and palettes.
The original artist's intent remains uncertain; this optional color interpretation does not establish a confirmed bug.

Both corrections change graphics and palette data without changing executable code.
The APC correction is released as v1.1.0.
The Campbell correction remains experimental and unreleased.

PATCH SELECTION

Each region has separate BPS and IPS patches.
The filenames contain us, eu, or jp.
Use the BPS patch that matches your clean ROM dump.
The BPS patch checks the source checksum.
The IPS format does not include a source checksum.

APC-only patches are in patches/.
Campbell-only patches are in campbell/patches/.
campbell/README.md describes the experimental correction and its patch files.

Both standalone corrections require clean source ROMs.
The standalone BPS patches cannot be applied sequentially.
Local ROMs containing both corrections passed the tests in campbell/COMBINED_VALIDATION.md.
Combined patches are not included in this repository or the existing release.

SUPPORTED SOURCES AND APC v1.1 TARGETS

Both corrections use the clean source ROMs listed below.
The target hashes and filenames in this section apply only to APC v1.1.
Campbell target hashes are in campbell/changes-us.json, campbell/changes-eu.json, and campbell/changes-jp.json.

USA
Source: Metal Gear Solid (USA).gbc
Size: 2097152 bytes
Source CRC32: 04b0c5d6
Source MD5: f6dd1b1e5747412b9e5f25376c972d5a
APC v1.1 target CRC32: a3bd2abc
APC v1.1 target SHA-256: 245ea9cda899fe042d26a68a9429e789d15fddbcf38e8dbe7ade43c59db2d525
APC patch: patches/ghost-babel-apc-color-fix-us-v1.1.bps

EUROPE
Source: Metal Gear Solid (Europe) (En,Fr,De,Es,It).gbc
Size: 4194304 bytes
Source CRC32: 16796957
Source MD5: 7971c95ad9745fe20df52e03cd52f636
APC v1.1 target CRC32: 4bc7796e
APC v1.1 target SHA-256: 9fb2e85c813bff77e76b317f7f94b9e7b49e088cc4d7255362bbdd317494bbdf
APC patch: patches/ghost-babel-apc-color-fix-eu-v1.1.bps

JAPAN
Source: Metal Gear - Ghost Babel (Japan).gbc
Size: 2097152 bytes
Source CRC32: 7831f84d
Source MD5: 7830328f323bd77d52a6985b1b10031f
APC v1.1 target CRC32: 80fedc50
APC v1.1 target SHA-256: 76407a78fb64b2c1648806a66f8439ec7b1aa4bb783df628d8577bbccda71025
APC patch: patches/ghost-babel-apc-color-fix-jp-v1.1.bps

DESKTOP APPLICATION

1. Obtain your own clean regional ROM dump.
2. Download Floating IPS from https://github.com/Sir-Walrus/Flips/releases.
3. Start Floating IPS.
4. Select Apply Patch.
5. Select the desired correction's BPS patch for your ROM's region.
6. Select your clean ROM dump.
7. Save the patched ROM as a separate file.
8. Start the patched ROM in your emulator or flash cartridge.

BROWSER APPLICATION

1. Open https://www.marcrobledo.com/RomPatcher.js/.
2. Select your clean dump in ROM file.
3. Select the desired correction's regional BPS patch in Patch file.
4. Select Apply patch.
5. Save the patched ROM as a separate file.

Use a fresh emulator session to load the changed graphics and palettes.

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
Floating IPS applied all regional standalone BPS and IPS files to their expected target hashes.

Combined experimental ROMs passed APC checks in both emulators for all regions.
They also passed the USA Campbell sequence and European and Japanese Campbell opening checks.
Physical Game Boy Color hardware and other patch combinations remain untested.

VALIDATION.md records the APC checks.
campbell/VALIDATION.md records the Campbell checks.
campbell/COMBINED_VALIDATION.md records the combined checks and their limits.

SOURCE AND UPDATES

Repository: https://github.com/afahy/ghost-babel-tank-color-fix
Releases: https://github.com/afahy/ghost-babel-tank-color-fix/releases

The repository includes a Python tool and regional manifests for reproducible patch builds.
The tool detects the source region and verifies the patched ROM hashes.
The default selection is APC; --fix campbell selects the experimental Campbell correction.
Place --fix before the verify, apply, or build subcommand.
Ruff provides Python code checks and formatting.
GitHub Actions runs these checks without game ROMs.
The repository also includes technical notes and validation details.

CREDITS

Color corrections: Adam Fahy.
Original game: Konami.
The repository license covers the patch tools and original documentation.
It grants no rights to the original game or its graphics.
