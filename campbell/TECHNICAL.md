# Campbell correction: technical notes

The experimental patch changes the opening briefing's scene `03` graphics, tile map, palette attributes, and palette set.
The USA, European, and Japanese releases use the same resource offsets.
Each regional manifest identifies its clean source ROM and target hashes.
Each patch changes 1,225 ROM bytes without changing the ROM size.

## Background tiles and palettes

Each tile uses one four-color background palette.
The patch stores 104 graphics tiles; the original stream stores 99.
The extra tiles separate pixels that need different color assignments.
The new compressed stream contains 1,093 bytes and expands to 1,664 bytes.

The scene palette set grows from four palettes to six.
Campbell uses palettes `0`, `1`, and `4`.
Snake retains his colors in palettes `2` and `3`.
Palette `5` retains the original grayscale colors for other background tiles.
Fixed palettes `6` and `7` remain unchanged.

The table shows the stored BGR555 color words.
The ROM stores each word in little-endian byte order.

| Palette | Color 0 | Color 1 | Color 2 | Color 3 | Use |
| --- | --- | --- | --- | --- | --- |
| `0` | `77BF` | `4E79` | `294E` | `0003` | Campbell skin and pale pink background |
| `1` | `7FFF` | `4E79` | `294E` | `0003` | Campbell skin and white collar |
| `2` | `77BF` | `4E79` | `294E` | `0003` | Original Snake colors |
| `3` | `001F` | `49F0` | `2D09` | `0C00` | Original Snake colors |
| `4` | `77BF` | `7FFF` | `294E` | `0003` | Campbell collar boundary |
| `5` | `7FFF` | `56B5` | `294A` | `0000` | Original grayscale background colors |

Small outline and shading changes keep each tile within its four-color limit.
One skin pixel at portrait coordinate `(48, 44)` uses the darker skin shade.
This adjustment keeps Campbell's palettes separate from Snake's palettes.

## ROM edits

Offsets identify bytes from the start of the ROM.
Bank addresses use the game's switchable ROM address range.

| ROM offset | Bank address | Change |
| --- | --- | --- |
| `00014E` | `00:014E` | Update the global checksum |
| `1941A1` | `65:41A1` | Increase scene `03`'s palette-set size from hexadecimal `20` to `30` (32 to 48 bytes) |
| `194A5E` | `65:4A5E` | Update the tile map and stored mirrored Campbell portrait |
| `194BC6` | `65:4BC6` | Update the palette attributes |
| `196AF4` | `65:6AF4` | Redirect the palette pointer from `6D26` to `75E0` |
| `1975E0` | `65:75E0` | Store the 48-byte palette set in unused padding |
| `197610` | `65:7610` | Store the 1,093-byte compressed graphics stream |
| `1C1828` | `70:5828` | Redirect the graphics pointer from `67:4E13` to `65:7610` |

The new palette set ends immediately before the compressed graphics stream.
The graphics stream ends at `65:7A54`, within the same ROM bank.
The original bytes in the allocated range are all `FF`.
The patch leaves the original graphics stream and original palette set `0C` unchanged.

| Region | Original global checksum | Patched global checksum |
| --- | --- | --- |
| USA | `3E5E` | `F925` |
| Europe | `9974` | `543B` |
| Japan | `5E56` | `191D` |

## Portrait fades and mirrored graphics

The scene stores the normal portraits in its upper tile-map rows.
Its lower eight rows contain mirrored portrait data.
The patch updates both Campbell representations and preserves their orientation.

The existing fade masks `F3` and `0C` remain unchanged.
Campbell's palettes stay outside Snake's mask, and Snake's palettes stay outside Campbell's mask.
The game's existing scene loader and fade routines continue to control the portraits.
The patch changes no executable instructions or sprite-overlay data.

## Reproduction

1. Obtain a clean regional ROM listed in [README.md](README.md).
2. Run `python patch.py --fix campbell verify "/path/to/source.gbc"` from the repository directory.
3. Run `python patch.py --fix campbell build "/path/to/source.gbc"`.
4. Run `python patch.py --fix campbell apply "/path/to/source.gbc" "/path/to/patched.gbc"`.

The tool checks source hashes and expected original byte ranges before applying edits.
It then checks the target hashes, header checksum, and global checksum.
The build reads the original ROM and writes separate patch files.
Applying writes a separate ROM file.
