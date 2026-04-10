---
name: paul-boom-reel
description: "Workflow for generating Footboom Universe Instagram Reels with Paul Boom avatar. Use when creating football match prediction videos for @footboom.universe Instagram account. Covers: consistent Paul Boom character description, match-specific background generation (DALL-E 3), keyframe compositing, video creation (generate_video), TTS voiceover (generate_speech), BGM (generate_music), ffmpeg audio mixing, and Instagram publishing via MCP or Graph API. Always uses the Footboom Universe logo and the provided visual template."
---

# Paul Boom Reel — Footboom Universe

## ⚠️ APPROVED STYLE — MUST FOLLOW

The approved visual style is locked. All reels MUST match these reference images exactly:

| Reference File | Purpose |
|---|---|
| `/home/ubuntu/footboom_agent/references/paul_boom_speaking_ref.png` | Keyframe 1 — Paul Boom speaking (first frame) |
| `/home/ubuntu/footboom_agent/references/paul_boom_pointing_ref.png` | Keyframe 2 — Paul Boom pointing (last frame) |
| `/home/ubuntu/footboom_agent/references/bg_layout_ref.png` | Background layout reference |
| `/home/ubuntu/upload/photo_2026-04-1002.30.45.jpeg` | Paul Boom character reference photo |

Always pass the appropriate reference file via the `references` parameter when calling `generate_image`.

---

## Character (use EXACTLY this description every time)

```
Paul Boom — white European male, 40-45 years old, short brown hair,
short beard, blue-grey eyes, dark navy blue suit, white shirt, dark blue tie,
black professional broadcast headset with microphone.
Authoritative, confident sports TV commentator. Chest-up shot, bottom-right corner.
```

## Permanent Assets

| Asset | Local Path |
|---|---|
| Paul Boom speaking reference | `/home/ubuntu/footboom_agent/references/paul_boom_speaking_ref.png` |
| Paul Boom pointing reference | `/home/ubuntu/footboom_agent/references/paul_boom_pointing_ref.png` |
| Background layout reference | `/home/ubuntu/footboom_agent/references/bg_layout_ref.png` |
| Character photo reference | `/home/ubuntu/upload/photo_2026-04-1002.30.45.jpeg` |

---

## Reel Production Workflow

### Step 1 — Match Data

Gather for each match:
- `home_team`, `away_team`, `tournament`, `match_date`
- `odds_home_win`, `odds_draw`, `odds_away_win`
- `key_factors` (3 bullet points: form, injuries, H2H)
- `analysis` (1 sentence)
- `prediction` (e.g. "CHELSEA WIN")
- `voiceover_script` (3-4 sentences EN, end with CTA)

**CTA phrase (always append):** `"Don't miss the action — follow Footboom Universe!"`

---

### Step 2 — Background Image (`generate_image`, 9:16)

```
Professional football match prediction infographic for Instagram Reels, 9:16 vertical format.
Top section: bold red banner with white text 'MATCH PREDICTION: {HOME} vs {AWAY}'.
Below: {HOME} badge on the left, {AWAY} badge on the right, large white 'VS' in the center,
on a dark blurred stadium background with floodlights.
Middle section: clean white rounded card with sections —
ODDS (WIN {OH} · DRAW {OD} · LOSS {OA}),
KEY FACTORS (bullet points: {KF1} · {KF2} · {KF3}),
ANALYSIS ({ANALYSIS}),
large red button EXPERT PREDICTION: {PREDICTION}.
Bottom section: dark stadium grass background,
Footboom Universe circular logo in center,
'PAUL BOOM' white bold text bottom-left.
Right side of bottom reserved for commentator.
Photorealistic, cinematic quality, professional sports broadcast design.
```

---

### Step 3 — Keyframe 1 — Speaking (`generate_image`, 9:16)

Use `references: ["/home/ubuntu/footboom_agent/references/paul_boom_speaking_ref.png"]`

```
Professional football match prediction Instagram Reels vertical 9:16 image.
Top 65% of frame: dark stadium background with a white prediction card showing
'MATCH PREDICTION: {HOME} vs {AWAY}' red banner, {HOME} and {AWAY} logos with VS,
white card with ODDS WIN {OH} DRAW {OD} LOSS {OA}, KEY FACTORS bullets,
ANALYSIS, red EXPERT PREDICTION: {PREDICTION} button, Footboom Universe logo.
Bottom-right 35% of frame: professional male sports TV commentator Paul Boom —
white European male, 40-45 years old, short brown hair, short beard, blue-grey eyes,
dark navy blue suit, white shirt, dark blue tie,
black professional broadcast headset with microphone,
speaking confidently to camera with mouth slightly open, chest-up shot,
blurred stadium background behind him.
'PAUL BOOM' white bold text at very bottom-left.
Photorealistic, cinematic, 4K quality.
```

---

### Step 4 — Keyframe 2 — Pointing (`generate_image`, 9:16)

Use `references: ["/home/ubuntu/footboom_agent/references/paul_boom_pointing_ref.png"]`

```
Professional football match prediction Instagram Reels vertical 9:16 image.
Top 65% of frame: dark stadium background with a white prediction card showing
'MATCH PREDICTION: {HOME} vs {AWAY}' red banner, {HOME} and {AWAY} logos with VS,
white card with ODDS WIN {OH} DRAW {OD} LOSS {OA}, KEY FACTORS bullets,
ANALYSIS, red EXPERT PREDICTION: {PREDICTION} button, Footboom Universe logo.
Bottom-right 35% of frame: professional male sports TV commentator Paul Boom —
white European male, 40-45 years old, short brown hair, short beard, blue-grey eyes,
dark navy blue suit, white shirt, dark blue tie,
black professional broadcast headset with microphone,
pointing confidently at camera with right index finger,
direct eye contact, authoritative expression.
'PAUL BOOM' white bold text at very bottom-left.
Photorealistic, cinematic, 4K quality.
```

---

### Step 5 — Video (`generate_video`, portrait, 8s, no audio)

- `keyframes.first`: keyframe 1 path (speaking)
- `keyframes.last`: keyframe 2 path (pointing)
- `generate_audio`: false

```
Professional sports TV commentator Paul Boom in dark navy suit with black broadcast headset,
standing in front of a football stadium background.
He starts speaking confidently to camera, gesturing with hands, then points directly at the viewer.
The prediction infographic card is visible in the upper portion of the frame
showing {HOME} vs {AWAY} match prediction.
Dynamic camera with slight zoom, cinematic sports broadcast lighting.
Energetic, authoritative sports prediction content. Vertical 9:16 format.
```

---

### Step 6 — Voiceover (`generate_speech`, male_voice)

```
{HOME} versus {AWAY} — this is the {TOURNAMENT} clash you cannot miss!
{CONTEXT sentence about form/injuries}.
Our odds: {HOME} win at {OH}, draw at {OD}, {AWAY} win at {OA}.
Key factors — {KF1}, {KF2}.
My expert prediction: {PREDICTION}!
Don't miss the action — follow Footboom Universe!
```

---

### Step 7 — BGM (`generate_music`)

```
Energetic sports broadcast background music. Fast-paced electronic beat with punchy drums,
driving bass line, and uplifting synth stabs. Stadium atmosphere feel, pre-match hype music.
Tempo around 128 BPM.
[0:00-0:04] Intro: building tension with rising synth.
[0:04-0:12] Main: full energy beat with brass hits and electronic percussion.
[0:12-0:16] Outro: fade out with reverb tail.
Instrumental only, no vocals. Original melody, not recognizable from any existing music.
```

---

### Step 8 — ffmpeg Mix

Get voiceover duration first: `ffprobe -v quiet -show_entries format=duration -of csv=p=0 voice.wav`

```bash
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 voice.wav)

ffmpeg -y \
  -stream_loop -1 -i paul_boom_video.mp4 \
  -i voice.wav \
  -i bgm.mp3 \
  -filter_complex "[1:a]volume=1.0[voice];[2:a]volume=0.15,atrim=0:${DURATION}[bgm];[voice][bgm]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" \
  -t ${DURATION} \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 192k \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -r 30 \
  final_reel.mp4
```

---

### Step 9 — Publish (Instagram MCP)

Upload video and cover to CDN first:
```bash
manus-upload-file final_reel.mp4
manus-upload-file keyframe2_pointing.png
```

Then publish:
```bash
manus-mcp-cli tool call create_instagram --server instagram --input '{
  "type": "reels",
  "caption": "<CAPTION>",
  "media": [{"type": "video", "media_url": "<VIDEO_CDN_URL>", "thumbnail_url": "<COVER_CDN_URL>"}],
  "cover_url": "<COVER_CDN_URL>",
  "share_to_feed": true
}'
```

---

## Caption Template

```
🔥 MATCH PREDICTION: {HOME} vs {AWAY} {EMOJI1}{EMOJI2}

{CONTEXT about the match}

📊 ODDS:
✅ {HOME} WIN — {OH}
🤝 DRAW — {OD}
❌ {AWAY} WIN — {OA}

🔑 KEY FACTORS:
• {KF1}
• {KF2}
• {KF3}

🎯 EXPERT PREDICTION: {PREDICTION}!

Don't miss the action — follow @footboom.universe for daily predictions!

#{HomeTag} #{AwayTag} #{TournamentTag} #FootballPrediction #FootboomUniverse #PaulBoom #MatchPrediction #Football #Soccer
```

---

## Visual Style Rules

- Format: **9:16 portrait** (1080×1920) for all Reels
- Background: dark stadium atmosphere, dramatic floodlights
- Accent color: **red (#EF4444)** for banners and prediction boxes
- Logo: Footboom Universe circular badge — always centered at bottom
- Paul Boom: always **bottom-right corner**, consistent character description
- **PAUL BOOM** text: always **bottom-left**, white bold
- **NEVER** use DALL-E to generate text-heavy infographics alone — always include Paul Boom in the same frame
- **NEVER** use Pillow/Python for background — always use `generate_image` (DALL-E)
- **ALWAYS** pass reference images via `references` parameter for consistency
