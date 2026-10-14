# Combined APC and Campbell corrections: validation

Validation date: 2026-10-13.
The version 1.2 combined ROMs passed the repeated validation checks below.
Physical Game Boy Color hardware remains untested.

We repeated the [APC validation process](../VALIDATION.md) on the USA, European, and Japanese combined ROMs.
Room comparisons, normal and thermal rendering, and movement passed in PyBoy and SameBoy.

We also repeated the [Campbell validation process](VALIDATION.md) on the combined ROMs.
The USA introduction, mirrored portrait, and gameplay passed in PyBoy and SameBoy.
European and Japanese opening-scene checks passed in PyBoy.

Floating IPS independently applied the BPS and IPS patches for all three regions.
Each result matched the target hash in the [combined patch documentation](../combined/README.md).
