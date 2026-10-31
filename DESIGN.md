# DESIGN — Image holograms

## What it is

The holographic projection concept made concrete with pictures:
four 16×16 images stored as one interference record
W = Σ|p_k⟩⟨p_k|, reconstructed by projection W|probe⟩.
The demo's money shot: zero out half the pixels of a cue and the
whole image still comes back — every fragment contains the whole,
because each pattern is distributed across the entire memory.

## Two honest distinctions the measurements forced

1. **Classification vs optical reconstruction.** The winner is
   always right (even at σ=0.5 + 50% occlusion), but the raw field
   W|probe⟩ reconstructs at fidelity ~0.75, not 1.0. The pictures
   are correlated (bars vs checker share half their pixels), so
   the losers bleed into the reconstruction. Winner-take-all
   "collapses" to 1.0; the honest optical image carries crosstalk.
2. **Weights are diluted by correlation.** Even a clean probe
   scores weight 0.65–0.75, not 1.0 — the correlated-capacity
   lesson showing up again: natural patterns are never orthogonal.

## Measured

- Winner correct at every (σ, occlusion) tested, incl. σ=0.5/50%.
- Field fidelity ~0.73–0.79 under noise+occlusion; recognizable
  in every ASCII rendering.
- Reconstruction always beats the cue (fidelity).

## Honest limits

- Four toy images at 16×16; amplitude encoding uses real
  non-negative amplitudes only — phase carries nothing here.
- This is the *mathematics* of holography (interference record +
  projection), not optical holography: no reference beam physics,
  no Bragg selectivity, no wavelength multiplexing.
- Correlated library: a near-orthogonal set would score cleaner;
  pictures are the hard case, reported as-is.
