METAL GEAR SOLID GHOST BABEL APC COLOR FIX
Version 1.1
October 13, 2026
Author: Adam Fahy

This patch corrects the colors of the two armored personnel carriers in Stage 2's yard outside Galuade fortress.
It targets Metal Gear Solid for Game Boy Color, also known as Metal Gear: Ghost Babel.
The corrected tiles use the hull's greens and preserve the surrounding sand.
Six brown shadow pixels become dark green to fit the room's available palettes.
The patch also corrects the thermal palette mapping.
It changes no executable code.

REGIONAL PATCHES

Each region has separate BPS and IPS patches.
The filenames contain us, eu, or jp.
Use the BPS patch that matches your clean ROM dump.
The BPS patch checks the source checksum.
The IPS format does not include a source checksum.

USA
Source: Metal Gear Solid (USA).gbc
Size: 2097152 bytes
Source CRC32: 04b0c5d6
Source MD5: f6dd1b1e5747412b9e5f25376c972d5a
Target CRC32: a3bd2abc
Target SHA-256: 245ea9cda899fe042d26a68a9429e789d15fddbcf38e8dbe7ade43c59db2d525
Patch: ghost-babel-apc-color-fix-us-v1.1.bps

EUROPE
Source: Metal Gear Solid (Europe) (En,Fr,De,Es,It).gbc
Size: 4194304 bytes
Source CRC32: 16796957
Source MD5: 7971c95ad9745fe20df52e03cd52f636
Target CRC32: 4bc7796e
Target SHA-256: 9fb2e85c813bff77e76b317f7f94b9e7b49e088cc4d7255362bbdd317494bbdf
Patch: ghost-babel-apc-color-fix-eu-v1.1.bps

JAPAN
Source: Metal Gear - Ghost Babel (Japan).gbc
Size: 2097152 bytes
Source CRC32: 7831f84d
Source MD5: 7830328f323bd77d52a6985b1b10031f
Target CRC32: 80fedc50
Target SHA-256: 76407a78fb64b2c1648806a66f8439ec7b1aa4bb783df628d8577bbccda71025
Patch: ghost-babel-apc-color-fix-jp-v1.1.bps

DESKTOP APPLICATION

1. Obtain your own clean regional ROM dump.
2. Download Floating IPS from https://github.com/Sir-Walrus/Flips/releases.
3. Start Floating IPS.
4. Select Apply Patch.
5. Select the BPS patch for your ROM's region.
6. Select your clean ROM dump.
7. Save the patched ROM as a separate file.
8. Start the patched ROM in your emulator or flash cartridge.

BROWSER APPLICATION

1. Open https://www.marcrobledo.com/RomPatcher.js/.
2. Select your clean dump in ROM file.
3. Select the matching regional BPS patch in Patch file.
4. Select Apply patch.
5. Save the patched ROM as a separate file.

Use a fresh emulator session to load the changed graphics and palettes.

SCREENSHOTS

before.png and after.png show the original and patched USA ROMs.
eu-before.png and eu-after.png show the European ROMs.
jp-before.png and jp-after.png show the Japanese ROMs.
SameBoy rendered all six images directly from their original or patched ROMs.
Each image retains the native 160 x 144 resolution and the game's HUD.
RAM selects the same room, camera position, and player position in each pair.
The capture process changes no ROM bytes.

VALIDATION AND COMPATIBILITY

Each version changes only the Stage 2 APC yard, with 384 corrected pixels.
Checks covered all 496 valid rooms per version.
Normal and thermal movement checks passed in PyBoy and SameBoy.
Floating IPS applied all six BPS and IPS files to the expected target hashes.
Its BPS checks rejected mismatched regional ROMs.
Physical Game Boy Color hardware and compatibility with other patches remain untested.

SOURCE AND UPDATES

Repository: https://github.com/afahy/ghost-babel-tank-color-fix
Releases: https://github.com/afahy/ghost-babel-tank-color-fix/releases

The repository includes a Python tool and regional manifests for reproducible patch builds.
The tool detects the source region and verifies the patched ROM hashes.
Ruff provides Python code checks and formatting.
GitHub Actions runs these checks without game ROMs.
The repository also includes technical notes and validation details.

CREDITS

Patch: Adam Fahy.
Original game: Konami.
The repository license covers the patch tools and original documentation.
It grants no rights to the original game or its graphics.
