# Sonic-Forage Claude Code Video Toolkit Fork

This fork tracks upstream `digitalsamba/claude-code-video-toolkit` and adds Jimsky/Sonic-Forage review surfaces, safe Modal readiness wrappers, and launch-ready example renders.

## Safety rails

- Keep `upstream` fetch-only; do not push to upstream.
- Never commit secrets, API keys, tokens, stream keys, Modal credentials, or generated credential files.
- Do not start GPU jobs, paid model inference, long Modal jobs, public social posts, public dataset changes, or livestreams without explicit approval for the exact action.
- Default experiments must be local/CPU-only, deterministic, and small enough for GitHub Pages review.
- Generated public artifacts must use owned/generated visuals/audio or explicitly licensed sources.
- Keep large model weights, caches, raw captures, and bulk outputs out of git.

## Verification

Run before commit:

```bash
python3 scripts/verify_jimsky_setup.py
python3 -m py_compile scripts/verify_jimsky_setup.py examples/sonic-forage-afterparty-signal/build_signal_video.py modal/sonic_forage_video_toolkit_readiness.py
git diff --check
```
