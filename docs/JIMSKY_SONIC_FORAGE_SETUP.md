# Jimsky / Sonic-Forage Setup Notes

This fork queues `digitalsamba/claude-code-video-toolkit` for Sonic-Forage / Afterparty Forge use.

## What is wired now

- GitHub fork: `Sonic-Forage/claude-code-video-toolkit`
- Upstream remote: `digitalsamba/claude-code-video-toolkit` fetch-only
- Local deterministic demo render: `examples/sonic-forage-afterparty-signal/`
- Public Pages review surface: `docs/index.html`
- Safe CPU-only Modal readiness app: `modal/sonic_forage_video_toolkit_readiness.py`
- Verifier: `scripts/verify_jimsky_setup.py`

## Operating mode

This is a safe launch queue, not an uncontrolled GPU runner.

Allowed by default:

- local Remotion/Python/FFmpeg renders
- CPU-only Modal readiness checks
- GitHub Pages review pages
- small owned/generated video artifacts

Requires explicit approval for the exact action:

- GPU Modal jobs
- paid generation
- external publishing/social posts
- livestream start/restart
- cloud storage writes outside the documented review artifacts

## Modal notes

Modal CLI is available from Hermes at `/opt/data/hermes-agent/venv/bin/modal` with credentials in `/opt/data/.env`.

The readiness wrapper intentionally uses CPU only and writes a small JSON report to the `outputs` Modal volume. It proves that the fork can run on Modal without waking GPUs or downloading model weights.

Run:

```bash
cd /opt/data/hermes-agent
source venv/bin/activate
set -a; source /opt/data/.env; set +a
modal run /opt/data/workspace/projects/claude-code-video-toolkit/modal/sonic_forage_video_toolkit_readiness.py
```

## Demo artifact

The first Sonic-Forage render is `Sonic-Forage Afterparty Signal 001`: a short neon signal bumper that shows the concept of a video toolkit lane feeding the public proof hub and stream loop.

Source:

```text
examples/sonic-forage-afterparty-signal/build_signal_video.py
```

Output:

```text
docs/media/sonic_forage_afterparty_signal_001.mp4
```
