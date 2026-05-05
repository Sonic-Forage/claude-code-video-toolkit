import json
import modal

app = modal.App("sonic-forage-video-toolkit-readiness")
image = modal.Image.debian_slim(python_version="3.11")
outputs = modal.Volume.from_name("outputs", create_if_missing=True)

@app.function(image=image, cpu=0.25, memory=512, timeout=120, volumes={"/outputs": outputs})
def probe():
    import datetime, json, os, pathlib, platform
    payload = {
        "ok": True,
        "app": "sonic-forage-video-toolkit-readiness",
        "purpose": "CPU-only readiness probe for Sonic-Forage claude-code-video-toolkit fork",
        "python": platform.python_version(),
        "utc": datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "gpu_started": False,
        "model_download_started": False,
        "secrets_present_but_not_printed": {
            "modal_token_id": bool(os.getenv("MODAL_TOKEN_ID")),
            "modal_token_secret": bool(os.getenv("MODAL_TOKEN_SECRET")),
        },
    }
    p = pathlib.Path("/outputs/sonic-forage-video-toolkit-readiness.json")
    p.write_text(json.dumps(payload, indent=2))
    outputs.commit()
    return payload

@app.local_entrypoint()
def main():
    print(json.dumps(probe.remote(), indent=2))
