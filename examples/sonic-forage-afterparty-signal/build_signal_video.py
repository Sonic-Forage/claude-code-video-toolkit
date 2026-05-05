#!/usr/bin/env python3
from pathlib import Path
import json, math, subprocess, wave
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/media"
OUT.mkdir(parents=True, exist_ok=True)
TMP = ROOT / "examples/sonic-forage-afterparty-signal/out"
TMP.mkdir(parents=True, exist_ok=True)

W, H, FPS, DURATION = 1280, 720, 30, 34
FRAMES = FPS * DURATION
FRAMES_DIR = TMP / "frames"
FRAMES_DIR.mkdir(exist_ok=True)
for old in FRAMES_DIR.glob("*.png"):
    old.unlink()

try:
    FONT_BIG = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
    FONT_MED = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
    FONT_SMALL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 24)
except Exception:
    FONT_BIG = FONT_MED = FONT_SMALL = ImageFont.load_default()

SCENES = [
    (0, 7, "SONIC-FORAGE", "video toolkit fork online"),
    (7, 14, "AFTERPARTY SIGNAL", "proof hub → render lane → stream loop"),
    (14, 22, "CLAUDE CODE VIDEO TOOLKIT", "forked, queued, verified"),
    (22, 29, "MODAL READY", "CPU probe only // GPU gates closed"),
    (29, 34, "WATCH IT BUILD", "next: Remotion + generated segments"),
]

def scene_at(t):
    for a,b,title,sub in SCENES:
        if a <= t < b:
            return title, sub
    return SCENES[-1][2], SCENES[-1][3]

def text_center(draw, y, text, font, fill):
    bbox = draw.textbbox((0,0), text, font=font)
    draw.text(((W-(bbox[2]-bbox[0]))/2, y), text, font=font, fill=fill)

for i in range(FRAMES):
    t = i / FPS
    im = Image.new("RGB", (W,H), (5, 4, 18))
    px = im.load()
    # cheap neon scanline/starfield background
    for y in range(0, H, 3):
        shade = int(12 + 18 * (0.5 + 0.5*math.sin(y*0.04 + t*1.7)))
        for x in range(0, W, 8):
            if (x*13 + y*7 + i*5) % 97 < 3:
                px[x,y] = (30, shade, 75)
    draw = ImageDraw.Draw(im, "RGBA")
    # pulsing tunnel/grid
    for k in range(22):
        z = (k/22 + t*0.12) % 1
        rw = int(80 + z*z*1260)
        rh = int(40 + z*z*700)
        col = (0, int(120+100*z), 255, int(28*(1-z)+8))
        draw.rectangle([(W/2-rw/2,H/2-rh/2),(W/2+rw/2,H/2+rh/2)], outline=col, width=2)
    for x in range(-200, W+200, 80):
        off = (t*95) % 80
        draw.line([(x+off, H), (W/2, H/2+70)], fill=(255,0,180,45), width=2)
    title, sub = scene_at(t)
    pulse = int(160 + 80*math.sin(t*math.tau*1.2))
    draw.rounded_rectangle([80,85,W-80,H-85], radius=32, outline=(0,220,255,180), width=4, fill=(0,0,25,105))
    draw.rounded_rectangle([110,115,W-110,205], radius=18, fill=(255,0,190,45), outline=(255,0,190,180), width=3)
    text_center(draw, 127, title, FONT_BIG, (255,255,255,255))
    text_center(draw, 232, sub, FONT_MED, (0,255,220,255))
    callouts = [
        "owned/generated visuals",
        "no public post without approval",
        "Modal CPU probe: safe",
        "GitHub Pages review surface",
    ]
    for n, c in enumerate(callouts):
        x = 165 + (n%2)*500
        y = 335 + (n//2)*92
        draw.rounded_rectangle([x,y,x+435,y+56], radius=14, fill=(0,255,190,25), outline=(0,255,190,120), width=2)
        draw.text((x+22,y+15), c, font=FONT_SMALL, fill=(230,255,255,240))
    # bottom ticker
    ticker = "▰ AI-NATIVE VIDEO LANE ▰ FORKED TO SONIC-FORAGE ▰ QUEUED FOR REALTIME STREAM BUILDING ▰"
    tx = int(W - ((t*145) % (W+1300)))
    draw.text((tx, H-54), ticker, font=FONT_SMALL, fill=(255,pulse,0,255))
    im.save(FRAMES_DIR / f"frame_{i:05d}.png")

# smooth audible synth bed (no random static)
sr=48000
wav=TMP / "afterparty_signal_bed.wav"
with wave.open(str(wav), "w") as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr)
    for n in range(int(DURATION*sr)):
        t=n/sr
        env=min(1,t/2,(DURATION-t)/2)
        s=0.22*math.sin(2*math.pi*110*t) + 0.10*math.sin(2*math.pi*220*t+0.6) + 0.05*math.sin(2*math.pi*330*t)
        # tiny kick pulse, not noise
        beat=(t*2)%1
        s += 0.18*math.exp(-beat*18)*math.sin(2*math.pi*55*t)
        val=max(-1,min(1,s*env))*32767
        wf.writeframes(int(val).to_bytes(2,'little',signed=True)*2)

mp4=OUT / "sonic_forage_afterparty_signal_001.mp4"
cmd=[
    "ffmpeg","-y","-hide_banner","-loglevel","error",
    "-framerate",str(FPS),"-i",str(FRAMES_DIR/"frame_%05d.png"),
    "-i",str(wav),"-shortest",
    "-vf","format=yuv420p",
    "-c:v","libx264","-preset","veryfast","-crf","23","-pix_fmt","yuv420p",
    "-c:a","aac","-b:a","160k","-ar","48000","-movflags","+faststart",str(mp4)
]
subprocess.run(cmd, check=True)
meta={
    "title":"Sonic-Forage Afterparty Signal 001",
    "duration_seconds": DURATION,
    "video":"1280x720 H.264",
    "audio":"AAC 48kHz stereo generated synth bed",
    "rights":"owned/generated",
    "gpu_started": False,
    "model_download_started": False,
    "public_posted": False,
    "source_script":"examples/sonic-forage-afterparty-signal/build_signal_video.py",
}
(OUT/"sonic_forage_afterparty_signal_001.json").write_text(json.dumps(meta, indent=2)+"\n")
print(mp4)
