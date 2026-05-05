#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
required = [
    "AGENTS.md",
    "docs/JIMSKY_SONIC_FORAGE_SETUP.md",
    "docs/index.html",
    "docs/media/sonic_forage_afterparty_signal_001.mp4",
    "docs/media/sonic_forage_afterparty_signal_001.json",
    "docs/reports/SONIC_FORAGE_VIDEO_TOOLKIT_REPORT.md",
    "examples/sonic-forage-afterparty-signal/build_signal_video.py",
    "modal/sonic_forage_video_toolkit_readiness.py",
]
for rel in required:
    p = ROOT / rel
    assert p.exists(), f"missing {rel}"
    assert p.stat().st_size > 0, f"empty {rel}"

index = (ROOT / "docs/index.html").read_text()
for needle in [
    "Sonic-Forage Video Toolkit Fork",
    "Afterparty Signal 001",
    "sonic_forage_afterparty_signal_001.mp4",
    "CPU-only Modal readiness",
]:
    assert needle in index, f"missing index needle: {needle}"

meta = json.loads((ROOT / "docs/media/sonic_forage_afterparty_signal_001.json").read_text())
assert meta["rights"] == "owned/generated"
assert meta["gpu_started"] is False
assert meta["public_posted"] is False
assert meta["title"] == "Sonic-Forage Afterparty Signal 001"

report = (ROOT / "docs/reports/SONIC_FORAGE_VIDEO_TOOLKIT_REPORT.md").read_text()
for needle in ["Sonic-Forage/claude-code-video-toolkit", "digitalsamba/claude-code-video-toolkit", "No GPU inference was run"]:
    assert needle in report, f"missing report needle: {needle}"

print("VERIFY OK sonic-forage video toolkit fork")
