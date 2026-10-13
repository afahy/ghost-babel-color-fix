# Technical notes

Version 1.0 changes background data for both tanks in area `02`, room `04`.
It uses the clean, unheadered USA ROM identified in `changes.json`.
The ROM remains 2,097,152 bytes long.
The patch changes no executable instructions.

## Palette design

The room uses background palettes 0 through 4.
Palette 5 is unused in the original room map.
Palettes 6 and 7 supply the HUD colors.

The front corners need sand and three hull greens.
The lower left corner also contains three brown shadow pixels per tank.
An exact correction would require seven distinct four-color combinations in the room map.
The six map palettes cannot hold all seven combinations while preserving the other tiles.

This version changes those six brown pixels to the hull's dark green.
It preserves all sand pixels.
The intended difference contains 378 color corrections and six additional shadow changes: 384 pixels total.

Palette 5 uses these BGR555 values:

| Color index | Normal palette | Source |
| --- | --- | --- |
| 0 | `3F7F` | Original sand color |
| 1 | `2F2D` | Hull palette 3, color 1 |
| 2 | `1DE5` | Hull palette 3, color 2 |
| 3 | `04C1` | Hull palette 3, color 3 |

## ROM edits

Offsets below identify bytes from the start of the ROM.
Bank addresses use the game's switchable ROM address range.
Words use little-endian byte order, except the global checksum.

| ROM offset | Bank address | Original bytes | Patched bytes | Purpose |
| --- | --- | --- | --- | --- |
| `00014E` | `00:014E` | `3E5E` | `0FE5` | Update the global checksum |
| `011D2C` | `04:5D2C` | `B117AB0E8500` | `2D2FE51DC104` | Set palette 5 colors 1 through 3 |
| `01C9F6` | `07:49F6` | `A15B` | `4075` | Redirect room 02/04's VBK0 tileset |
| `0C547F` | `31:547F` | `0C0C` | `0D0D` | Select palette 5 for metatile `28F.BL` and `28F.BR` |
| `0C5498` | `31:5498` | `0C` | `0D` | Select palette 5 for metatile `292.BR` |
| `0C54BB` | `31:54BB` | `02` | `05` | Select palette 5 for metatile `297.TL` |
| `107540` | `41:7540` | 1,509 bytes of `FF` | Compressed tileset | Store the isolated room tileset |
| `155581` | `55:5581` | `19` | `14` | Correct thermal palette 5, color 2 |

`changes.json` contains every original and replacement byte, including the compressed tileset.

## Isolated tileset

The original VBK0 tileset starts at `41:5BA1`.
Its compressed stream contains 1,511 bytes and produces 2,048 bytes: 128 tiles.
The patch retains that original stream for other rooms.

The patch copies the tileset to `41:7540` and changes tile `1E` in the copy.
That tile's color index 1 becomes color index 3.
Only two bytes change in the uncompressed copy:

| Uncompressed offset | Original | Patched |
| --- | --- | --- |
| `01ED` | `07` | `0F` |
| `01EF` | `03` | `0F` |

The new stream contains 1,509 bytes and ends at `41:7B24`.
The source ROM contains only `FF` padding from `41:7540` through `41:7FFF`.
The new stream stays within the bank and reads no unwritten decompression output.
Only room 02/04's tileset pointer selects the copy.

## Thermal colors and priority

Room 02/04 uses thermal palette set 4 at `55:5555`.
Other rooms do not use that set.
Its corrected palette 5 contains `319F`, `1CFF`, `0014`, and `000A`.
These values combine the thermal sand color with the thermal hull colors.

The patch preserves color index 0, which determines how sprites with background priority overlap background pixels.
It changes the six shadow pixels from one nonzero index to another nonzero index.
The metatile edits preserve VRAM bank, flip, and background priority bits.
HUD palettes 6 and 7 remain unchanged.
The game's existing palette updates continue to control fades and thermal colors.

## Independent reproduction

The public repository includes all required patch data and uses Python's standard library.
Reproduction requires no private repository, assembler, or separate graphics tools.

1. Obtain the clean USA ROM identified in `changes.json`.
2. Run `python patch.py verify "/path/to/Metal Gear Solid (USA).gbc"`.
3. Run `python patch.py build "/path/to/Metal Gear Solid (USA).gbc"`.
4. Run `python patch.py apply "/path/to/Metal Gear Solid (USA).gbc" "/path/to/patched.gbc"`.

The tool checks the source hashes and each original byte range.
It then checks all target hashes, the header checksum, and the global checksum.
It refuses an existing output file or an output path that equals the input path.

The target SHA-256 is:

```text
245ea9cda899fe042d26a68a9429e789d15fddbcf38e8dbe7ade43c59db2d525
```
