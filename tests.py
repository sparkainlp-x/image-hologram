"""Tests for image-hologram. Run: python tests.py"""

import math
import random

from hologram import (LIBRARY, encode, store, project, fidelity,
                      noisy, occlude, cue, ascii_art, decode,
                      make_circle)


def _lib(n=16):
    px = [fn(n) for _, fn in LIBRARY]
    return px, [encode(p) for p in px]


def test_encode_normalizes():
    for _, fn in LIBRARY:
        v = encode(fn(16))
        assert abs(sum(abs(c) ** 2 for c in v) - 1.0) < 1e-12


def test_clean_probe_recalls_exactly():
    # winners are exact, but weights are < 1: the pictures are
    # correlated (bars vs checker share half their pixels), so the
    # vote is split -- the correlated-capacity lesson, again.
    px, pats = _lib()
    W = store(pats)
    for k, p in enumerate(pats):
        w, wt, _ = project(W, pats, p)
        assert w == k and wt > 0.60, (k, w, wt)


def test_noisy_probe_finds_winner():
    px, pats = _lib()
    W = store(pats)
    for k, p in enumerate(px):
        c = cue(p, 0.30, 0.0, random.Random(k))
        w, _, _ = project(W, pats, c)
        assert w == k, (k, w)


def test_half_occluded_still_recalls():
    # the holographic property: 50% of pixels gone, the right image
    # still wins. The raw field is degraded by crosstalk (the pictures
    # are correlated), so its fidelity is ~0.75, not 1.0 -- the
    # classification is perfect, the optical reconstruction is not.
    px, pats = _lib()
    W = store(pats)
    for k, p in enumerate(px):
        c = cue(p, 0.0, 0.50, random.Random(50 + k))
        w, _, field = project(W, pats, c)
        assert w == k, (k, w)
        assert fidelity(pats[k], field) > 0.70


def test_reconstruction_beats_cue():
    px, pats = _lib()
    W = store(pats)
    for k, p in enumerate(px):
        c = cue(p, 0.40, 0.25, random.Random(9 + k))
        _, _, field = project(W, pats, c)
        assert fidelity(pats[k], field) > fidelity(pats[k], c)


def test_cue_deterministic():
    p = make_circle(16)
    a = cue(p, 0.2, 0.3, random.Random(3))
    b = cue(p, 0.2, 0.3, random.Random(3))
    assert a == b


def test_ascii_art_shape():
    art = ascii_art(make_circle(16)).split("\n")
    assert len(art) == 16 and all(len(r) == 16 for r in art)


def test_decode_normalizes_display():
    px, pats = _lib()
    d = decode(pats[0])
    assert abs(max(d) - 1.0) < 1e-12 and min(d) >= 0.0


if __name__ == "__main__":
    for name, fn in sorted(
            [(k, v) for k, v in globals().items() if k.startswith("test_")]):
        fn()
        print(f"PASS {name}")
    print("all tests passed")
