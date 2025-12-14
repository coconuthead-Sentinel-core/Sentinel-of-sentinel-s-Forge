"""
Lightweight vector utilities with optional NumPy acceleration.

Functions provided:
  - dot(u, v)
  - norm(u)
  - normalize(u)
  - cosine(u, v)

Optional PCAProjector is enabled only if NumPy is available and
the environment variable QNF_USE_PCA is set to a truthy value.
"""

from __future__ import annotations

import os
import math
from typing import Iterable, List, Sequence, Optional


_USE_NUMPY = False
_NP = None  # type: ignore

try:
    # Only enable NumPy path if explicitly requested
    if str(os.getenv("QNF_USE_NUMPY", "0")).lower() in ("1", "true", "yes", "on"):
        import numpy as _np  # type: ignore

        _USE_NUMPY = True
        _NP = _np
except Exception:
    _USE_NUMPY = False
    _NP = None


def _to_list(x: Iterable[float]) -> List[float]:
    return list(float(v) for v in x)


def dot(u: Sequence[float], v: Sequence[float]) -> float:
    if _USE_NUMPY and _NP is not None:
        return float(_NP.dot(_NP.asarray(u, dtype=float), _NP.asarray(v, dtype=float)))
    # Pure Python fallback
    return sum((float(a) * float(b) for a, b in zip(u, v)), 0.0)


def norm(u: Sequence[float]) -> float:
    if _USE_NUMPY and _NP is not None:
        arr = _NP.asarray(u, dtype=float)
        return float(_NP.linalg.norm(arr))
    return math.sqrt(dot(u, u))


def normalize(u: Sequence[float]) -> List[float]:
    if _USE_NUMPY and _NP is not None:
        arr = _NP.asarray(u, dtype=float)
        n = float(_NP.linalg.norm(arr))
        if n <= 0.0:
            return _to_list(arr)
        return _to_list(arr / n)
    n = norm(u)
    if n <= 0.0:
        return _to_list(u)
    return [float(x) / n for x in u]


def cosine(u: Sequence[float], v: Sequence[float]) -> float:
    du = dot(u, v)
    nu = norm(u)
    nv = norm(v)
    denom = (nu * nv) if (nu > 0.0 and nv > 0.0) else 0.0
    if denom <= 0.0:
        return 0.0
    return float(du / denom)


class PCAProjector:
    """Optional PCA projector using NumPy SVD.

    Enabled only if both NumPy is available and QNF_USE_PCA is truthy.
    """

    def __init__(self, dim: int, k: int = 8, window: int = 512) -> None:
        self.dim = int(dim)
        self.k = max(1, int(k))
        self.window = max(16, int(window))
        self._enabled = bool(
            _USE_NUMPY
            and _NP is not None
            and str(os.getenv("QNF_USE_PCA", "0")).lower() in ("1", "true", "yes", "on")
        )
        self._buf: List[List[float]] = []
        self._mean: Optional["_NP.ndarray"] = None  # type: ignore
        self._components: Optional["_NP.ndarray"] = None  # type: ignore
        self._singular_values: Optional["_NP.ndarray"] = None  # type: ignore

    @property
    def enabled(self) -> bool:
        return self._enabled

    def add(self, vec: Sequence[float]) -> None:
        if not self._enabled:
            return
        self._buf.append(_to_list(vec))
        if len(self._buf) > self.window:
            self._buf.pop(0)

    def fit(self) -> None:
        if not self._enabled or _NP is None or not self._buf:
            return
        X = _NP.asarray(self._buf, dtype=float)
        self._mean = _NP.mean(X, axis=0)
        Xc = X - self._mean
        # economy SVD
        U, S, Vt = _NP.linalg.svd(Xc, full_matrices=False)
        k = min(self.k, Vt.shape[0])
        self._components = Vt[:k, :]
        self._singular_values = S

    def transform(self, vec: Sequence[float]) -> List[float]:
        if not self._enabled or _NP is None or self._components is None or self._mean is None:
            return _to_list(vec)
        x = _NP.asarray(vec, dtype=float)
        x_c = x - self._mean
        z = self._components.dot(x_c)
        return _to_list(z)

    def metrics(self) -> dict:
        """Return retained variance and reconstruction error estimates.

        - retained_variance: sum(S[:k]^2) / sum(S^2)
        - recon_error_mean: sum(S[k:]^2) / n_samples (Frobenius residual per-sample)
        """
        if not self._enabled or _NP is None or self._singular_values is None:
            return {"enabled": False}
        S = self._singular_values
        total = float(_NP.sum(S * S)) if S.size else 0.0
        k = min(self.k, S.shape[0])
        retained = float(_NP.sum(S[:k] * S[:k])) if S.size else 0.0
        discarded = total - retained
        n_samples = float(len(self._buf)) if self._buf else 1.0
        retained_frac = (retained / total) if total > 0.0 else 0.0
        recon_per_sample = discarded / max(1.0, n_samples)
        return {
            "enabled": True,
            "proj_dim": k,
            "base_dim": self.dim,
            "retained_variance": retained_frac,
            "recon_error_mean": recon_per_sample,
        }
