# Image Hologram

**Store pictures as interference patterns. Reconstruct them from
fragments.**

Four 16×16 images stored in one complex outer-product hologram;
projection is the reconstruction. Zero out half the pixels of a
cue and the whole image still returns — every fragment contains
the whole. Stdlib-only Python, ASCII-art display. AGPL-3.0.

## Verified

- Correct winner at every noise/occlusion level tested
  (σ up to 0.5, 50% pixels gone)
- Reconstruction fidelity ~0.73–0.79, always beats the cue
- 8/8 tests pass

## Run it

```bash
python tests.py   # 8 tests
python demo.py    # ASCII reconstructions + fidelity table
```

## Honest limits

Toy images; amplitude encoding only (phase unused); the
mathematics of holography, not optical holography; correlated
library means crosstalk in the raw field. Full account in
`DESIGN.md`.

## Credits

Authors: Jean-François Brisson and Mun Seok Lee.
Lee, author of the Digital to Wave paradigm (Zenodo 21947036,
21947108), is the inspiration friend behind this wave and
membrane work. This package's code was built by Brisson with
AI assistance, except where a file already credits Lee as
author; the joint credit here is for the shared programme,
not a claim that Lee wrote every line of this package.
