# Campbell correction: validation

Validation date: 2026-10-13.
This patch remains experimental and unreleased.
The USA ROM passed introduction and gameplay checks in PyBoy and SameBoy.
European and Japanese ROMs passed shorter PyBoy opening-scene checks.
Physical Game Boy Color hardware has not been tested.

## ROM identities

The regional manifests identify these clean source ROMs and experimental targets.
Each patch changes 1,225 bytes and preserves the source ROM size.

| Region | Source SHA-256 | Target SHA-256 |
| --- | --- | --- |
| USA | `56a69d19ba26941a25adad8bdf17c7baba12245097e901999f4c897eec877ddb` | `60144b0727b1676ac552644810d3ba2a1fda6f2744294edef92c34173ed6ccee` |
| Europe | `90d3bb23de52e642ce361f9688910f3dc3669427452de6290589e72b1f22311f` | `bbb53f118bc2fb5ac84d2a52af99bffd3c0acc0dcd2bc2d2a791bc8854aa12be` |
| Japan | `e2bd68276538c8eb939fc1d7a65c7caf54cab09ca3bbf9d819b94344582717f7` | `07c265fc8697c1fb468dbe3ef89b43097971bdcae4ca46b79ad5d786e5d3326c` |

## USA runtime checks

| Check | PyBoy 2.7.0 | SameBoy 1.0.3 CGB core |
| --- | --- | --- |
| Retail boot | Passed | Passed |
| Opening briefing portrait | 1,073 changed pixels | 1,073 changed pixels |
| Briefing transitions and portrait fades | Passed | Passed |
| Briefing, mission start, and player control | Passed | Passed |
| Upward movement | Matching gameplay images | Matching gameplay images |
| Stored mirrored portrait | 1,073 changed pixels | 1,073 changed pixels |

The USA portrait matched the expected image exactly, including the darker skin pixel at `(48, 44)`.
Both normal and mirrored scenes changed only Campbell's portrait, by 1,073 pixels.
Snake's portrait and dialogue remained unchanged.
The test continued through the briefing, the first mission's codec sequence, and player control.
Matching upward movement produced equal gameplay images.
The replacement compressed graphics added one loading frame.

All 1,631 recorded USA fade-state transitions matched between the original and patched ROMs.
The checked fade images preserved Snake's portrait and dialogue.

PyBoy found no unrelated image differences at the checked scene, mission, player-control, and movement checkpoints.
SameBoy's mission-start and movement images also matched.
At one later player-control checkpoint, SameBoy showed four different pixels in a blinking radar marker.
The marker's blink phase differed after the loading delay.

PyBoy's compared sprite attributes matched.
SameBoy's visible sprite attributes matched.
One hidden sprite's X coordinate differed while its Y coordinate was zero.
These results do not establish identical instruction timing or random-number state.

## European and Japanese checks

| Regional runtime check | Europe | Japan |
| --- | --- | --- |
| PyBoy cold boot and opening scene | Passed | Passed |
| Expected Campbell portrait | Exact match | Exact match |
| Changed portrait pixels | 1,073 | 1,073 |
| Snake, dialogue, and sprite attributes | Unchanged | Unchanged |

These regional checks did not repeat the complete introduction and gameplay tests.
SameBoy regional tests and physical hardware tests have not been performed.

## ROM screenshots

[Before](../images/campbell-before.png) and [after](../images/campbell-after.png) show the full opening briefing scene.
[Mirrored before](../images/campbell-before-mirrored.png) and [mirrored after](../images/campbell-after-mirrored.png) show the later portrait orientation.
These files are native 160 × 144 SameBoy screenshots from the source and experimental target ROMs.
They contain no image-editor color corrections.

The emulator tests loaded the original and separately patched ROMs.
They did not modify the original source files.

## Patch format and tool checks

Floating IPS independently applied all three regional BPS files and all three regional IPS files.
Each output matched its manifest's target SHA-256.
The Python tool applied all three regional corrections and rejected existing output files.
Rebuilding reproduced the patch files exactly.
The CLI's default APC selection remained unchanged.
All source ROM hashes remained unchanged, and the targets passed cartridge checksum checks.

The existing APC release's validation does not validate this experimental Campbell patch.

## Limits

An image preview cannot establish ROM runtime behavior.
Emulator checks cannot guarantee operation on physical hardware.
The original artist's intent remains uncertain.
This patch implements an optional color interpretation.
