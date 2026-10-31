"""Image holograms: store pictures as interference patterns,
reconstruct them from noisy or fragmented cues.

The memory W = sum_k |p_k><p_k| is the hologram -- an interference
record of every stored image. Projection is the reconstruction:
W|probe> = sum_k |p_k><p_k|probe>. The defining holographic property:
every fragment of the cue still contains the whole image, because
each stored pattern is distributed across the entire memory.

Stdlib only. Images are generated programmatically (no files).
"""

import math
import random


# ------------------------------------------------------------ images
def make_circle(n=16):
    c = (n - 1) / 2
    return [1.0 if math.hypot(i - c, j - c) < n * 0.32 else 0.0
            for i in range(n) for j in range(n)]


def make_cross(n=16):
    c = n // 2
    return [1.0 if i == c or j == c else 0.0
            for i in range(n) for j in range(n)]


def make_bars(n=16):
    return [1.0 if (j // 2) % 2 == 0 else 0.0
            for i in range(n) for j in range(n)]


def make_checker(n=16):
    return [1.0 if (i // 2 + j // 2) % 2 == 0 else 0.0
            for i in range(n) for j in range(n)]


LIBRARY = [("circle", make_circle), ("cross", make_cross),
           ("bars", make_bars), ("checker", make_checker)]


# ------------------------------------------------------------ codec
def encode(pixels):
    """Amplitude encoding: pixel brightness -> complex amplitude."""
    v = [complex(p, 0.0) for p in pixels]
    n = math.sqrt(sum(abs(c) ** 2 for c in v))
    return [c / n for c in v]


def store(patterns):
    """Hologram: sum of outer products."""
    n = len(patterns[0])
    W = [[0j] * n for _ in range(n)]
    for p in patterns:
        for i in range(n):
            pi = p[i]
            Wi = W[i]
            for j in range(n):
                Wi[j] += pi * p[j].conjugate()
    return W


def overlaps(W_probe_field, patterns, probe):
    """Projection amplitudes <p_k|probe> for each stored pattern."""
    return [sum(p[k].conjugate() * probe[k] for k in range(len(probe)))
            for p in patterns]


def project(W, patterns, probe):
    """Returns (winner_index, winner_weight, field_reconstruction).
    winner = argmax |overlap|^2; field = W|probe> normalized."""
    ms = overlaps(None, patterns, probe)
    tot = sum(abs(m) ** 2 for m in ms)
    w = max(range(len(ms)), key=lambda i: abs(ms[i]))
    n = len(probe)
    field = [sum(W[i][j] * probe[j] for j in range(n)) for i in range(n)]
    norm = math.sqrt(sum(abs(c) ** 2 for c in field))
    if norm > 0:
        field = [c / norm for c in field]
    return w, (abs(ms[w]) ** 2 / tot if tot else 0.0), field


def fidelity(a, b):
    return abs(sum(x.conjugate() * y for x, y in zip(a, b))) ** 2


# ------------------------------------------------------------ cues
def noisy(pixels, sigma, rng):
    v = [min(1.0, max(0.0, p + rng.gauss(0, sigma))) for p in pixels]
    return encode(v)


def occlude(pixels, fraction, rng):
    """Zero out a random fraction of pixels: the fragment test."""
    idx = list(range(len(pixels)))
    rng.shuffle(idx)
    kill = set(idx[:int(len(pixels) * fraction)])
    return encode([0.0 if i in kill else p for i, p in enumerate(pixels)])


def cue(pixels, sigma, occ, rng):
    """One cue pipeline: Gaussian noise, then a random fraction of
    pixels zeroed. occ=0 -> pure noise; sigma=0 -> pure fragment."""
    raw = [min(1.0, max(0.0, p + rng.gauss(0, sigma))) for p in pixels]
    idx = list(range(len(raw)))
    rng.shuffle(idx)
    kill = set(idx[:int(len(raw) * occ)])
    return encode([0.0 if i in kill else v for i, v in enumerate(raw)])


# ------------------------------------------------------------ seeing
GRADIENT = " .:-=+*#%@"


def ascii_art(pixels, n=16):
    rows = []
    for i in range(n):
        rows.append("".join(
            GRADIENT[min(len(GRADIENT) - 1, int(p * len(GRADIENT)))]
            for p in pixels[i * n:(i + 1) * n]))
    return "\n".join(rows)


def decode(field):
    """Complex field -> pixel brightnesses for display."""
    m = max(abs(c) for c in field) or 1.0
    return [abs(c) / m for c in field]
