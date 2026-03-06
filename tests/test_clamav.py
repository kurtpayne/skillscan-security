from __future__ import annotations

from pathlib import Path

from skillscan.clamav import scan_paths


def test_clamav_unavailable(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr("skillscan.clamav.shutil.which", lambda _x: None)
    result = scan_paths(tmp_path)
    assert result.available is False
    assert result.detections == []
    assert "not installed" in (result.message or "")


def test_clamav_detects_signature(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr("skillscan.clamav.shutil.which", lambda _x: "/usr/bin/clamscan")

    class _Proc:
        def __init__(self):
            self.stdout = f"{tmp_path}/bad.bin: Win.Test.Eicar FOUND\n"

    monkeypatch.setattr("skillscan.clamav.subprocess.run", lambda *a, **k: _Proc())
    result = scan_paths(tmp_path)
    assert result.available is True
    assert len(result.detections) == 1
    assert result.detections[0].signature == "Win.Test.Eicar"


def test_clamav_timeout(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr("skillscan.clamav.shutil.which", lambda _x: "/usr/bin/clamscan")

    def _raise_timeout(*_a, **_k):
        raise __import__("subprocess").TimeoutExpired(cmd="clamscan", timeout=30)

    monkeypatch.setattr("skillscan.clamav.subprocess.run", _raise_timeout)
    result = scan_paths(tmp_path)
    assert result.available is True
    assert result.detections == []
    assert "timed out" in (result.message or "")
