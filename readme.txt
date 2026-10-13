METAL GEAR SOLID GHOST BABEL TANK COLOR FIX
Version 1.0
October 13, 2026
Author: Adam Fahy

This patch corrects mismatched colors on both tanks in the Outer Heaven front yard.
It targets area 02, room 04, in Metal Gear Solid for Game Boy Color.
The game is also known as Metal Gear: Ghost Babel.

The corrected tiles use the hull's greens and preserve the surrounding sand.
Six brown shadow pixels become dark green to fit the room's available palettes.
The patch also corrects the thermal palette mapping.
It changes no executable code.

REQUIRED SOURCE

Metal Gear Solid (USA).gbc
Clean USA release, without an added copier header.
Size: 2097152 bytes
CRC32: 04b0c5d6
MD5: f6dd1b1e5747412b9e5f25376c972d5a
SHA-1: 2266499cfa10351b23fefd2216308867d1f1558b
SHA-256: 56a69d19ba26941a25adad8bdf17c7baba12245097e901999f4c897eec877ddb

PATCHED ROM

Size: 2097152 bytes
CRC32: a3bd2abc
MD5: 140a3f1634ac1ec6b7cefeb71696efb9
SHA-1: d9f46720f2e648498131a3759549e456f2523a9d
SHA-256: 245ea9cda899fe042d26a68a9429e789d15fddbcf38e8dbe7ade43c59db2d525

APPLICATION

1. Obtain your own clean USA ROM dump.
2. Open https://www.marcrobledo.com/RomPatcher.js/.
3. Select your dump in ROM file.
4. Select ghost-babel-tank-color-fix-v1.0.bps in Patch file.
5. Select Apply patch.
6. Save the patched ROM as a separate file.
7. Start the patched ROM in your emulator or flash cartridge.

Use a fresh emulator session to load the changed graphics and palettes.
The BPS patch checks the source checksum.
The IPS format does not include a source checksum.

SCREENSHOTS

before.png: Original USA ROM in SameBoy.
after.png: Patched USA ROM in SameBoy.
Both images retain the native 160 x 144 resolution and the game's HUD.
RAM selects the same room, camera position, and player position in both captures.
The capture process changes no ROM bytes.

COMPATIBILITY

The European and Japanese releases require separate patches.
Compatibility with other patches has not been tested.
Physical Game Boy Color hardware has not been tested.

SOURCE AND UPDATES

Repository: https://github.com/afahy/ghost-babel-tank-color-fix
Releases: https://github.com/afahy/ghost-babel-tank-color-fix/releases

The repository includes a Python tool and a manifest for reproducible patch builds.
It also includes technical notes.

CREDITS

Patch: Adam Fahy.
Original game: Konami.
The repository license covers the patch tools and original documentation.
It grants no rights to the original game or its graphics.
