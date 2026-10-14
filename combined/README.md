# Optional APC + Campbell patch set

Version 1.2.1 includes both the Stage 2 APC correction and Campbell's opening portrait correction.
The [primary patch set](../README.md#download) contains the APC correction only.
This optional set adds consistent skin colors and corrected collar and background boundaries to Campbell's portrait.

Each combined patch requires a clean regional ROM and contains both corrections.
Applying this set does not require the APC-only patch first.
The original artist's intent remains uncertain; Campbell's correction offers an optional color interpretation.

## Patch files

| Region | BPS | IPS |
| --- | --- | --- |
| USA | [USA BPS](patches/ghost-babel-color-corrections-us-v1.2.1.bps) | [USA IPS](patches/ghost-babel-color-corrections-us-v1.2.1.ips) |
| Europe | [European BPS](patches/ghost-babel-color-corrections-eu-v1.2.1.bps) | [European IPS](patches/ghost-babel-color-corrections-eu-v1.2.1.ips) |
| Japan | [Japanese BPS](patches/ghost-babel-color-corrections-jp-v1.2.1.bps) | [Japanese IPS](patches/ghost-babel-color-corrections-jp-v1.2.1.ips) |

[Release downloads](https://github.com/afahy/ghost-babel-color-fix/releases/tag/v1.2.1) include the optional combined archive.
[SHA256SUMS.txt](patches/SHA256SUMS.txt) records the patch file hashes.
The repository contains no game ROM.

## Required source ROMs

Use your own clean ROM dump without an added copier header.
Select the patch that matches your ROM's region.

| Region | Source ROM | Size | Source CRC32 |
| --- | --- | --- | --- |
| USA | Metal Gear Solid (USA) | 2,097,152 bytes | `04b0c5d6` |
| Europe | Metal Gear Solid (Europe) (En,Fr,De,Es,It) | 4,194,304 bytes | `16796957` |
| Japan | Metal Gear - Ghost Babel (Japan) | 2,097,152 bytes | `7831f84d` |

| Region | Combined target SHA-256 |
| --- | --- |
| USA | `cfba270d86cec5185bfbd0ca6d600e39e5224f593aed59a790aaee78900274ce` |
| Europe | `97e01085822bce72f9e394aa73464198623c2193bbdf3e73d478990b9de9a5b9` |
| Japan | `88e66f0e2340f4baa7f1991cb4344375cde74f672b9ed9464911680cb352f801` |

## Apply the optional combined patch

1. Start [Floating IPS](https://github.com/Sir-Walrus/Flips/releases).
2. Select **Apply Patch**.
3. Select the combined BPS patch for your ROM's region.
4. Select your clean ROM dump.
5. Save the patched ROM as a separate file.
6. Start a fresh emulator session with the patched ROM.

BPS checks the source checksum.
IPS does not include a source checksum.
Each combined BPS rejects a source that already contains another patch.

## Apply with Python

Run this command from the repository directory:

```sh
python patch.py --fix combined apply "/path/to/Metal Gear Solid (USA).gbc" "/path/to/Metal Gear Solid (USA) (APC and Campbell).gbc"
```

The tool detects the region and checks the source and target hashes.
When you omit `--fix`, the apply command selects the primary APC-only correction.

## Build the patch sets

Build both release patch sets for a clean regional source ROM:

```sh
python patch.py build "/path/to/Metal Gear Solid (USA).gbc"
```

The command writes APC-only patches to `patches/` and optional combined patches to `combined/patches/`.

Build only the optional combined set:

```sh
python patch.py --fix combined build "/path/to/Metal Gear Solid (USA).gbc"
```

## Technical details and validation

The tool builds each combined edit list from the APC and Campbell manifests and computes one global checksum update.
The edit ranges for the two corrections do not overlap, except for the global checksum.
Each combined ROM changes 2,566 bytes and preserves its original size.
The patch changes no executable instructions.

[APC technical notes](../TECHNICAL.md) and [Campbell technical notes](../campbell/TECHNICAL.md) explain the underlying graphics and palette changes.
[Combined validation](../campbell/COMBINED_VALIDATION.md) records the room, introduction, gameplay, and patch application checks.
The release targets match the ROMs used in those tests exactly.
Physical Game Boy Color hardware remains untested.
