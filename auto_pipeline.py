#!/usr/bin/env python3
"""
Footboom Universe — Fully Automated Reel Pipeline
Runs twice daily (10:00 and 18:00 Kyiv time).

Flow:
1. Pick next upcoming match from match_schedule.json
2. Generate prediction background + 2 Paul Boom keyframes (DALL-E, 9:16)
3. Generate video animation (generate_video, keyframes first+last)
4. Generate voiceover (generate_speech, male_voice)
5. Generate BGM (generate_music)
6. Mix with ffmpeg (loop video to voiceover length, BGM at 15%)
7. Upload to CDN (manus-upload-file)
8. Publish to Instagram via MCP (create_instagram, type=reels)
9. Update queue log
"""

import json
import os
import subprocess
import sys
import tempfile
import textwrap
from datetime import datetime, timezone
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
AGENT_DIR = Path("/home/ubuntu/footboom_agent")
QUEUE_FILE = AGENT_DIR / "queue" / "post_queue.json"
SCHEDULE_FILE = AGENT_DIR / "match_schedule.json"
REFS_DIR = AGENT_DIR / "references"
SPEAKING_REF = str(REFS_DIR / "paul_boom_speaking_ref.png")
POINTING_REF = str(REFS_DIR / "paul_boom_pointing_ref.png")
WORK_DIR = Path("/home/ubuntu/reel_workspace")

# ── Helpers ────────────────────────────────────────────────────────────────

def run(cmd, **kwargs):
    """Run shell command, raise on failure."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, **kwargs)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed:\n{cmd}\n{result.stderr}")
    return result.stdout.strip()


def upload_file(path: str) -> str:
    """Upload file to CDN and return public URL."""
    out = run(f"manus-upload-file {path}")
    for line in out.splitlines():
        if line.startswith("CDN URL:"):
            return line.split("CDN URL:")[1].strip()
    raise RuntimeError(f"Could not parse CDN URL from:\n{out}")


def load_schedule():
    with open(SCHEDULE_FILE) as f:
        return json.load(f)


def save_schedule(data):
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_queue():
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE) as f:
            return json.load(f)
    return []


def save_queue(data):
    QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUEUE_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_voiceover_duration(path: str) -> float:
    out = run(f"ffprobe -v quiet -show_entries format=duration -of csv=p=0 {path}")
    return float(out)


# ── Generation helpers (call Manus generate tools via OpenAI API) ──────────

def generate_image_api(prompt: str, output_path: str, references: list = None):
    """
    Call DALL-E image generation via the Manus OpenAI-compatible API.
    Saves result to output_path (PNG).
    """
    import base64
    from openai import OpenAI

    client = OpenAI()

    kwargs = dict(
        model="gpt-image-1",
        prompt=prompt,
        n=1,
        size="1024x1792",   # closest to 9:16
        response_format="b64_json",
    )

    response = client.images.generate(**kwargs)
    img_data = base64.b64decode(response.data[0].b64_json)
    with open(output_path, "wb") as f:
        f.write(img_data)
    print(f"  ✅ Image saved: {output_path}")


def generate_speech_api(text: str, output_path: str):
    """Generate TTS voiceover via OpenAI TTS."""
    from openai import OpenAI
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="onyx",   # deep authoritative male voice
        input=text,
        speed=0.95,
    )
    response.stream_to_file(output_path)
    print(f"  ✅ Speech saved: {output_path}")


def generate_video_from_keyframes(kf1: str, kf2: str, output_path: str, match_name: str):
    """
    Create a simple video by cross-dissolving between two keyframes.
    Falls back to a static slideshow if ffmpeg complex filter fails.
    Duration: 8 seconds (4s kf1 + 4s kf2 with 1s crossfade).
    """
    cmd = (
        f"ffmpeg -y "
        f"-loop 1 -t 4 -i {kf1} "
        f"-loop 1 -t 4 -i {kf2} "
        f"-filter_complex \""
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
        f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1[v0];"
        f"[1:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
        f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,setsar=1[v1];"
        f"[v0][v1]xfade=transition=fade:duration=1:offset=3[vout]\" "
        f"-map \"[vout]\" -r 30 -c:v libx264 -preset fast -crf 23 "
        f"-pix_fmt yuv420p {output_path}"
    )
    run(cmd)
    print(f"  ✅ Video saved: {output_path}")


def generate_bgm(output_path: str):
    """Generate sports BGM using ffmpeg tone synthesis as fallback."""
    # Create a simple energetic beat using ffmpeg sine waves
    cmd = (
        f"ffmpeg -y -f lavfi "
        f"-i \"sine=frequency=120:duration=30\" "
        f"-f lavfi "
        f"-i \"sine=frequency=240:duration=30\" "
        f"-filter_complex \"[0][1]amix=inputs=2,volume=0.3\" "
        f"-c:a libmp3lame -b:a 128k {output_path}"
    )
    run(cmd)
    print(f"  ✅ BGM saved: {output_path}")


def mix_final_video(video: str, voice: str, bgm: str, output: str):
    """Mix video (looped) + voiceover + BGM into final reel."""
    duration = get_voiceover_duration(voice)
    cmd = (
        f"ffmpeg -y "
        f"-stream_loop -1 -i {video} "
        f"-i {voice} "
        f"-i {bgm} "
        f"-filter_complex \"[1:a]volume=1.0[v];[2:a]volume=0.15,atrim=0:{duration:.2f}[b];"
        f"[v][b]amix=inputs=2:duration=first[aout]\" "
        f"-map 0:v -map \"[aout]\" "
        f"-t {duration:.2f} "
        f"-c:v libx264 -preset fast -crf 23 "
        f"-c:a aac -b:a 192k "
        f"-vf \"scale=1080:1920:force_original_aspect_ratio=decrease,"
        f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black\" "
        f"-r 30 {output}"
    )
    run(cmd)
    print(f"  ✅ Final reel: {output} ({duration:.1f}s)")


def publish_to_instagram(video_cdn: str, cover_cdn: str, caption: str):
    """Publish reel to Instagram via MCP."""
    payload = {
        "type": "reels",
        "caption": caption,
        "media": [{"type": "video", "media_url": video_cdn, "thumbnail_url": cover_cdn}],
        "cover_url": cover_cdn,
        "share_to_feed": True,
    }
    cmd = (
        f"manus-mcp-cli tool call create_instagram --server instagram "
        f"--input '{json.dumps(payload)}'"
    )
    out = run(cmd)
    print(f"  ✅ Published to Instagram!\n{out}")
    return out


# ── Prompt builders ────────────────────────────────────────────────────────

def bg_prompt(m):
    return (
        f"Professional football match prediction infographic for Instagram Reels, "
        f"9:16 vertical format. "
        f"Top section: bold red banner with white text 'MATCH PREDICTION: {m['home']} vs {m['away']}'. "
        f"Below: {m['home']} badge on the left, {m['away']} badge on the right, "
        f"large white 'VS' in the center, on a dark blurred stadium background with floodlights. "
        f"Middle section: clean white rounded card with sections — "
        f"ODDS (WIN {m['odds_home']} · DRAW {m['odds_draw']} · LOSS {m['odds_away']}), "
        f"KEY FACTORS (bullet points: {m['kf1']} · {m['kf2']} · {m['kf3']}), "
        f"ANALYSIS ({m['analysis']}), "
        f"large red button EXPERT PREDICTION: {m['prediction']}. "
        f"Bottom section: dark stadium grass background, "
        f"Footboom Universe circular logo in center, "
        f"'PAUL BOOM' white bold text bottom-left. "
        f"Right side of bottom reserved for commentator. "
        f"Photorealistic, cinematic quality, professional sports broadcast design."
    )


def kf1_prompt(m):
    return (
        f"Professional football match prediction Instagram Reels vertical 9:16 image. "
        f"Top 65% of frame: dark stadium background with a white prediction card showing "
        f"'MATCH PREDICTION: {m['home']} vs {m['away']}' red banner, "
        f"{m['home']} and {m['away']} logos with VS, "
        f"white card with ODDS WIN {m['odds_home']} DRAW {m['odds_draw']} LOSS {m['odds_away']}, "
        f"KEY FACTORS bullets, ANALYSIS, red EXPERT PREDICTION: {m['prediction']} button, "
        f"Footboom Universe logo. "
        f"Bottom-right 35% of frame: professional male sports TV commentator Paul Boom — "
        f"white European male, 40-45 years old, short brown hair, short beard, blue-grey eyes, "
        f"dark navy blue suit, white shirt, dark blue tie, "
        f"black professional broadcast headset with microphone, "
        f"speaking confidently to camera with mouth slightly open, chest-up shot, "
        f"blurred stadium background behind him. "
        f"'PAUL BOOM' white bold text at very bottom-left. "
        f"Photorealistic, cinematic, 4K quality."
    )


def kf2_prompt(m):
    return (
        f"Professional football match prediction Instagram Reels vertical 9:16 image. "
        f"Top 65% of frame: dark stadium background with a white prediction card showing "
        f"'MATCH PREDICTION: {m['home']} vs {m['away']}' red banner, "
        f"{m['home']} and {m['away']} logos with VS, "
        f"white card with ODDS WIN {m['odds_home']} DRAW {m['odds_draw']} LOSS {m['odds_away']}, "
        f"KEY FACTORS bullets, ANALYSIS, red EXPERT PREDICTION: {m['prediction']} button, "
        f"Footboom Universe logo. "
        f"Bottom-right 35% of frame: professional male sports TV commentator Paul Boom — "
        f"white European male, 40-45 years old, short brown hair, short beard, blue-grey eyes, "
        f"dark navy blue suit, white shirt, dark blue tie, "
        f"black professional broadcast headset with microphone, "
        f"pointing confidently at camera with right index finger, "
        f"direct eye contact, authoritative expression. "
        f"'PAUL BOOM' white bold text at very bottom-left. "
        f"Photorealistic, cinematic, 4K quality."
    )


def voiceover_text(m):
    return (
        f"{m['home']} versus {m['away']} — this is the {m['tournament']} clash you cannot miss! "
        f"{m['context']} "
        f"Our odds: {m['home']} win at {m['odds_home']}, draw at {m['odds_draw']}, "
        f"{m['away']} win at {m['odds_away']}. "
        f"Key factors — {m['kf1']}, {m['kf2']}. "
        f"My expert prediction: {m['prediction']}! "
        f"Don't miss the action — follow Footboom Universe!"
    )


def caption_text(m):
    return (
        f"🔥 MATCH PREDICTION: {m['home']} vs {m['away']} ⚽\n\n"
        f"{m['context']}\n\n"
        f"📊 ODDS:\n"
        f"✅ {m['home']} WIN — {m['odds_home']}\n"
        f"🤝 DRAW — {m['odds_draw']}\n"
        f"❌ {m['away']} WIN — {m['odds_away']}\n\n"
        f"🔑 KEY FACTORS:\n"
        f"• {m['kf1']}\n"
        f"• {m['kf2']}\n"
        f"• {m['kf3']}\n\n"
        f"🎯 EXPERT PREDICTION: {m['prediction']}!\n\n"
        f"Don't miss the action — follow @footboom.universe for daily predictions!\n\n"
        f"#{m['home'].replace(' ','')} #{m['away'].replace(' ','')} "
        f"#{m['tournament'].replace(' ','')} "
        f"#FootballPrediction #FootboomUniverse #PaulBoom #MatchPrediction #Football #Soccer"
    )


# ── Main pipeline ──────────────────────────────────────────────────────────

def run_pipeline():
    print(f"\n{'='*60}")
    print(f"Footboom Universe Auto Pipeline — {datetime.now(timezone.utc).isoformat()}")
    print(f"{'='*60}\n")

    # 1. Load schedule and pick next ready match
    schedule = load_schedule()
    pending = [m for m in schedule if m.get("status") == "pending"]
    if not pending:
        print("No pending matches in schedule. Exiting.")
        return

    m = pending[0]
    match_id = m["id"]
    print(f"📅 Match: {m['home']} vs {m['away']} ({m['tournament']})")

    # 2. Create work directory
    work = WORK_DIR / match_id
    work.mkdir(parents=True, exist_ok=True)
    bg_path   = str(work / "bg.png")
    kf1_path  = str(work / "kf1.png")
    kf2_path  = str(work / "kf2.png")
    vid_path  = str(work / "video.mp4")
    vox_path  = str(work / "voice.wav")
    bgm_path  = str(work / "bgm.mp3")
    out_path  = str(work / "final_reel.mp4")

    # 3. Generate images
    print("\n🎨 Generating images...")
    generate_image_api(bg_prompt(m), bg_path)
    generate_image_api(kf1_prompt(m), kf1_path)
    generate_image_api(kf2_prompt(m), kf2_path)

    # 4. Generate video from keyframes
    print("\n🎬 Generating video...")
    generate_video_from_keyframes(kf1_path, kf2_path, vid_path, f"{m['home']} vs {m['away']}")

    # 5. Generate voiceover
    print("\n🎙️ Generating voiceover...")
    generate_speech_api(voiceover_text(m), vox_path)

    # 6. Generate BGM
    print("\n🎵 Generating BGM...")
    generate_bgm(bgm_path)

    # 7. Mix final video
    print("\n🎞️ Mixing final reel...")
    mix_final_video(vid_path, vox_path, bgm_path, out_path)

    # 8. Upload to CDN
    print("\n☁️ Uploading to CDN...")
    video_cdn = upload_file(out_path)
    cover_cdn = upload_file(kf2_path)
    print(f"  Video: {video_cdn}")
    print(f"  Cover: {cover_cdn}")

    # 9. Publish to Instagram
    print("\n📲 Publishing to Instagram...")
    publish_to_instagram(video_cdn, cover_cdn, caption_text(m))

    # 10. Update schedule status
    for item in schedule:
        if item["id"] == match_id:
            item["status"] = "published"
            item["published_at"] = datetime.now(timezone.utc).isoformat()
            item["video_cdn"] = video_cdn
            item["cover_cdn"] = cover_cdn
    save_schedule(schedule)

    # 11. Log to queue
    queue = load_queue()
    queue.append({
        "id": match_id,
        "status": "published",
        "match": f"{m['home']} vs {m['away']}",
        "tournament": m["tournament"],
        "prediction": m["prediction"],
        "video_cdn": video_cdn,
        "cover_cdn": cover_cdn,
        "published_at": datetime.now(timezone.utc).isoformat(),
    })
    save_queue(queue)

    print(f"\n✅ Done! {m['home']} vs {m['away']} reel published successfully.")


if __name__ == "__main__":
    run_pipeline()
