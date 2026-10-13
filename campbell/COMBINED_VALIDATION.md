# Combined APC and Campbell corrections: validation

Validation date: 2026-10-13.
Local experimental ROMs containing both corrections passed the checks below.
The distributed standalone patch files remain unchanged.
Physical Game Boy Color hardware has not been tested.

## Composition and patch checks

The combined build starts with each region's clean original ROM and applies both manifests.
Their data ranges do not overlap, except for the global checksum.
The build calculates the checksum once, after applying all other edits.
Either edit order produces the same combined ROM.
Both corrections retain their expected data bytes.

Each combined ROM changes 2,566 bytes and preserves the original ROM size.
All original source hashes remained unchanged.
Floating IPS independently applied six newly generated local combined patches: BPS and IPS for each region.
Each result matched its combined ROM's SHA-256.

| Region | Combined ROM SHA-256 |
| --- | --- |
| USA | `cfba270d86cec5185bfbd0ca6d600e39e5224f593aed59a790aaee78900274ce` |
| Europe | `97e01085822bce72f9e394aa73464198623c2193bbdf3e73d478990b9de9a5b9` |
| Japan | `88e66f0e2340f4baa7f1991cb4344375cde74f672b9ed9464911680cb352f801` |

The existing standalone BPS patches reject a ROM containing the other correction.
The combined checks used patches built for clean originals; they did not apply the two standalone patches in sequence.

## APC checks

An independent decoder compared 496 valid rooms in each region.
Only room `02/04` changed, by 384 pixels.
No unexpected pixels or decoded gameplay records changed.

| Check across all three regions | PyBoy 2.7.0 | SameBoy 1.0.3 CGB core |
| --- | --- | --- |
| Normal yard image | Matches APC-only ROM | Matches APC-only ROM |
| Thermal yard image | Matches APC-only ROM | Matches APC-only ROM |
| Yard images after movement | Match APC-only ROM | Match APC-only ROM |
| Compared game state and movement | Match | Match |

The tests used retail boot, followed by the existing developer selector through RAM.
RAM setup selected the yard, viewport, and equipped item.
Regional PyBoy checks used the existing SVBK compatibility hook.
USA checks also passed with sound emulation enabled and that hook disabled.
SameBoy used the CGB boot ROM.

## Campbell checks

The USA combined ROM passed a cold boot and the full introduction through ordinary button inputs in both emulators.
The tests continued through the mirrored portrait, Mission 1's codec sequence, player control, and upward movement.
Campbell's portrait matched the expected correction, with 1,073 changed pixels in each orientation.
Snake's portrait, dialogue, and visible sprite attributes remained unchanged.

All 1,631 recorded USA fade-state transitions matched.
The 16 checked fade images preserved Snake's portrait and dialogue.
PyBoy's later gameplay images and compared sprite attributes matched.
SameBoy's mission-start and movement images also matched.

The combined ROM retained the standalone Campbell patch's one additional loading frame.
At one later SameBoy control checkpoint, four radar marker pixels differed because the blink phase differed.
One hidden sprite's X coordinate also differed while its Y coordinate remained zero.
These observations do not establish identical instruction timing or random-number state.

European and Japanese combined ROMs passed shorter PyBoy opening-scene checks.
Each Campbell portrait matched the expected correction, with 1,073 changed pixels.
Snake's portrait, dialogue, and compared sprite attributes remained unchanged.
These checks did not repeat the full introduction or later gameplay in those regions.

## Limits

The tests establish the recorded emulator behavior of these experimental combined ROMs.
They do not establish physical hardware compatibility.
Other patch combinations have not been tested.
