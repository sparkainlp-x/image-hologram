"""Demo: every fragment contains the whole image.

Stores 4 pictures as one hologram. Then:
 1. Shows a noisy cue and its reconstruction.
 2. Shows a 50%-occluded cue (half the pixels gone) and its
    reconstruction -- the holographic property.
 3. Prints the fidelity table over noise and occlusion levels.

Run: python demo.py
"""

import random

from hologram import (LIBRARY, encode, store, project, fidelity,
                      noisy, occlude, cue, ascii_art, decode)


def show(title, pixels):
    print(f"--- {title} ---")
    print(ascii_art(pixels))


def main():
    n = 16
    names = [name for name, _ in LIBRARY]
    pixels = [fn(n) for _, fn in LIBRARY]
    patterns = [encode(p) for p in pixels]
    W = store(patterns)
    rng = random.Random(7)

    show("original: circle", pixels[0])
    probe = noisy(pixels[0], 0.30, rng)
    w, wt, field = project(W, patterns, probe)
    print(f"\nnoisy cue (sigma=0.30) -> winner: {names[w]} "
          f"(weight {wt:.3f}, fidelity {fidelity(patterns[0], field):.3f})")
    show("reconstruction", decode(field))

    frag = occlude(pixels[2], 0.50, rng)
    w2, wt2, field2 = project(W, patterns, frag)
    print(f"\n50%-occluded cue of 'bars' -> winner: {names[w2]} "
          f"(weight {wt2:.3f}, fidelity {fidelity(patterns[2], field2):.3f})")
    show("reconstruction from fragment", decode(field2))

    print("\n== fidelity table (winner vs true pattern) ==")
    print(f"{'sigma':>6} {'occ':>5} " +
          " ".join(f"{nm[:6]:>7}" for nm in names))
    for sigma in (0.10, 0.30, 0.50):
        for occ in (0.0, 0.50):
            row = []
            for k, p in enumerate(pixels):
                c = cue(p, sigma, occ, random.Random(1000 + k))
                w_, _, _ = project(W, patterns, c)
                row.append(fidelity(patterns[k], patterns[w_]))
            print(f"{sigma:>6.2f} {occ:>5.2f} " +
                  " ".join(f"{v:>7.3f}" for v in row))


if __name__ == "__main__":
    main()
