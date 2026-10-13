# Validation

Validation date: 2026-10-13.

The tests used the unmodified 2 MiB **Metal Gear Solid (USA)** ROM as the source.
The patch produced the target release image.
Both emulators loaded these ROMs directly.

| Image | SHA-256 |
| --- | --- |
| Source | `56a69d19ba26941a25adad8bdf17c7baba12245097e901999f4c897eec877ddb` |
| Target | `245ea9cda899fe042d26a68a9429e789d15fddbcf38e8dbe7ade43c59db2d525` |

## Room comparison

An independent ROM decoder rendered all 496 valid rooms, including story rooms, VR rooms, and four VS candidates.
Only room **02/04** changed, by **384 pixels**.
The existing invalid record **0E/13** remained invalid.
The room comparison found no changes to collision, triggers, entries, exits, objects, or other decoded gameplay records.

The expected image used the four established PC color corrections, reconstructed from the original ROM.
It also included the selected brown-to-dark-green change for three shadow pixels per APC.
Every target pixel matched that expected image.
The changed pixels remained inside the eight selected tile quadrants across both APCs.

## Emulator checks

| Check | PyBoy 2.7.0 | SameBoy 1.0.3 CGB core |
| --- | --- | --- |
| Retail boot and room 02/04 start | Passed | Passed |
| Normal room image | 384 changed pixels | 384 changed pixels |
| Movement in four directions | Passed | Passed |
| Image after movement | 384 changed pixels | 384 changed pixels |
| Thermal goggles and movement | Passed | Passed |
| Thermal room image | 384 changed pixels | 384 changed pixels |
| Compared gameplay state | Equal | Equal |

The checks compared mode, sub-mode, room, camera, and player coordinates.
The PyBoy checks also compared health and entity records.
The screenshot differences contained no HUD changes.

SameBoy used a fixed power-on random seed of `1`.
Its movement checks counted completed game updates at the existing `Mission_DebugHook`, at `06:52D7`.
Fixed display-frame inputs initially produced small movement differences, consistent with CPU phase changes from the replacement compressed tiles.
Equivalent game-update checks passed.
These tests do not claim identical instruction timing or physical hardware validation.

## Published screenshots

[Before](images/before.png) and [after](images/after.png) show both complete APCs and the full HUD.
Both files are native **160 × 144** SameBoy screenshots.
SameBoy rendered the source and release target directly with color correction disabled.
Pillow converted the captured PPM frames to PNG without resizing or recoloring.

Each capture followed the retail boot sequence and opened the existing PRGNO selector through RAM.
The selector started story mode `0B`, area `02`, room `04`, on Normal difficulty.
Matching RAM setup set the camera to `(616, 300)` and the player to `(700, 390)` before the room loader drew.
The capture setup changed no ROM bytes.
The screenshots differ by exactly **384 pixels**.

Thermal tests set the equipped item to `03` before the normal room palette loader ran.
The original and target used the same setup.

## Patch format and application checks

[Rom Patcher JS](https://github.com/marcrobledo/RomPatcher.js/tree/3183884086825c3a57c72026234debcef1e2240c) independently applied both patch files.
The BPS and IPS results matched the target ROM exactly.
The BPS reader rejected a modified source ROM and a corrupted patch.
The patched cartridge passed its header and global checksum checks.

The Python tool reproduced the target ROM exactly.
It detected the clean USA, European, and Japanese releases and rejected already-patched or modified source ROMs.
It preserved an existing output file and rejected the source path as the output path.

## European and Japanese releases

The regional checks used the verified original ROMs and their respective release targets.
Both emulators loaded these ROMs directly.
The decoder checked each regional source against the verified USA data layout before rendering.

| Check | Europe | Japan |
| --- | --- | --- |
| Valid rooms compared | 496 | 496 |
| Changed room | 02/04 | 02/04 |
| Changed pixels | 384 | 384 |
| Expected-image differences | None | None |
| Decoded gameplay-record differences | None | None |
| Existing invalid room | 0E/13, unchanged | 0E/13, unchanged |
| PyBoy retail boot and movement | Passed | Passed |
| SameBoy retail boot and movement | Passed | Passed |
| Normal and thermal screenshot differences | 384 pixels | 384 pixels |
| Compared gameplay state | Equal | Equal |

The European radar table uses `21:667A`; the Japanese table uses `21:6680`.
The decoder derived these addresses from each ROM's radar loader and verified the area pointers.
SameBoy used game-update hooks at `06:52D2` for Europe and `06:52D4` for Japan.
The selector and camera RAM references remain unchanged.

[European before](images/eu-before.png) and [European after](images/eu-after.png) show the original and patched European ROMs.
[Japanese before](images/jp-before.png) and [Japanese after](images/jp-after.png) show the original and patched Japanese ROMs.
Each screenshot retains the native 160 × 144 resolution.
The capture method matches the USA checks described above.

## Floating IPS checks

[Floating IPS](https://github.com/Sir-Walrus/Flips/tree/ff216a75df0987047a67d7923567dc4482ce07ac) independently applied all six regional BPS and IPS files.
Each result matched its manifest's target SHA-256.
All six attempts to apply a BPS patch to another supported region failed without producing output files.

## Python code quality

Ruff 0.17.0 passed its lint and formatting checks.
The configuration targets Python 3.8.
After formatting, all six regional patch files remained byte-identical.
GitHub Actions runs the same checks without ROM files.
