"""
Computes and verifies SHA-256 hashes for evidence files (product images,
generated PDFs, etc). Used at capture-time to create a tamper-evident
fingerprint, and later to verify the stored file hasn't changed.
"""
from __future__ import annotations

import hashlib
from pathlib import Path


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_file(path: str | Path, chunk_size: int = 65536) -> str:
    path = Path(path)
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def verify_file(path: str | Path, expected_hash: str) -> bool:
    return hash_file(path) == expected_hash
