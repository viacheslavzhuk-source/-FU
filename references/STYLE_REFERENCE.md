# Footboom Universe — Approved Style References

## Status: APPROVED ✅ (April 10, 2026)

These images are the **golden reference** for all auto-generated reels.
Every new video MUST match this style exactly.

---

## Reference Files

| File | Role | Description |
|------|------|-------------|
| `paul_boom_speaking_ref.png` | Keyframe 1 (first) | Paul Boom speaking to camera, mouth open, gesturing |
| `paul_boom_pointing_ref.png` | Keyframe 2 (last) | Paul Boom pointing at viewer, authoritative expression |
| `bg_layout_ref.png` | Background layout | Full prediction card with all sections |

---

## Layout Specification (9:16 vertical, 1080×1920px)

### Top Section (~30%)
- **Red banner** at very top: `MATCH PREDICTION: [TEAM A] vs [TEAM B]`
- Team badge left, **VS** center, team badge right
- Dark blurred stadium background

### Middle Section (~45%) — White rounded card
- **ODDS** row: WIN [x.xx] · DRAW [x.xx] · LOSS [x.xx]
- **KEY FACTORS** with 3 bullet points
- **ANALYSIS** short text paragraph
- **EXPERT PREDICTION: [OUTCOME]** — large red rounded button

### Bottom Section (~25%)
- Stadium grass/pitch background
- **FOOTBOOM UNIVERSE** circular logo — centered
- **PAUL BOOM** white bold text — bottom-left
- Paul Boom avatar — bottom-right (chest-up, ~35% of frame width)

---

## Paul Boom Character Description

> White European male, 40–45 years old, short brown hair, short beard,
> blue-grey eyes, dark navy blue suit, white shirt, dark blue tie,
> black professional broadcast headset with microphone.
> Authoritative, confident sports TV commentator look.

### Keyframe 1 — Speaking (first frame)
Paul Boom speaking confidently to camera, mouth slightly open,
hands gesturing, direct eye contact. Blurred stadium behind.

### Keyframe 2 — Pointing (last frame)
Paul Boom pointing directly at viewer with right index finger,
intense direct eye contact, authoritative expression.

---

## Generation Prompts

### Background (`generate_image`, 9:16)
```
Professional football match prediction infographic for Instagram Reels, 9:16 vertical format.
Top section: bold red banner with white text 'MATCH PREDICTION: [TEAM A] vs [TEAM B]'.
Below: [TEAM A] badge on the left, [TEAM B] badge on the right, large white 'VS' in the center,
on a dark blurred stadium background with floodlights.
Middle section: clean white rounded card with sections —
ODDS (WIN [x.xx] · DRAW [x.xx] · LOSS [x.xx]),
KEY FACTORS (bullet points: [factor1] · [factor2] · [factor3]),
ANALYSIS ([analysis text]),
large red button EXPERT PREDICTION: [OUTCOME].
Bottom section: dark stadium grass background,
Footboom Universe circular logo in center,
'PAUL BOOM' white bold text bottom-left.
Right side of bottom reserved for commentator.
Photorealistic, cinematic quality, professional sports broadcast design.
```

### Keyframe 1 — Speaking (`generate_image`, 9:16, references: paul_boom_speaking_ref.png)
```
Professional football match prediction Instagram Reels vertical 9:16 image.
Top 65% of frame: dark stadium background with a white prediction card showing
'MATCH PREDICTION: [TEAM A] vs [TEAM B]' red banner, [TEAM A] and [TEAM B] logos with VS,
white card with ODDS WIN [x.xx] DRAW [x.xx] LOSS [x.xx], KEY FACTORS bullets,
ANALYSIS, red EXPERT PREDICTION: [OUTCOME] button, Footboom Universe logo.
Bottom-right 35% of frame: professional male sports TV commentator Paul Boom —
white European male, 40-45 years old, short brown hair, short beard, blue-grey eyes,
dark navy blue suit, white shirt, dark blue tie,
black professional broadcast headset with microphone,
speaking confidently to camera with mouth slightly open, chest-up shot,
blurred stadium background behind him.
'PAUL BOOM' white bold text at very bottom-left.
Photorealistic, cinematic, 4K quality.
```

### Keyframe 2 — Pointing (`generate_image`, 9:16, references: paul_boom_pointing_ref.png)
```
Professional football match prediction Instagram Reels vertical 9:16 image.
Top 65% of frame: dark stadium background with a white prediction card showing
'MATCH PREDICTION: [TEAM A] vs [TEAM B]' red banner, [TEAM A] and [TEAM B] logos with VS,
white card with ODDS WIN [x.xx] DRAW [x.xx] LOSS [x.xx], KEY FACTORS bullets,
ANALYSIS, red EXPERT PREDICTION: [OUTCOME] button, Footboom Universe logo.
Bottom-right 35% of frame: professional male sports TV commentator Paul Boom —
white European male, 40-45 years old, short brown hair, short beard, blue-grey eyes,
dark navy blue suit, white shirt, dark blue tie,
black professional broadcast headset with microphone,
pointing confidently at camera with right index finger,
direct eye contact, authoritative expression.
'PAUL BOOM' white bold text at very bottom-left.
Photorealistic, cinematic, 4K quality.
```

### Video (`generate_video`, portrait, 8s, no audio)
```
Professional sports TV commentator Paul Boom in dark navy suit with black broadcast headset,
standing in front of a football stadium background.
He starts speaking confidently to camera, gesturing with hands, then points directly at the viewer.
The prediction infographic card is visible in the upper portion of the frame
showing [TEAM A] vs [TEAM B] match prediction.
Dynamic camera with slight zoom, cinematic sports broadcast lighting.
Energetic, authoritative sports prediction content. Vertical 9:16 format.
```

### Voiceover (`generate_speech`, male_voice)
```
[TEAM A] versus [TEAM B] — this is the [COMPETITION] clash you cannot miss!
[CONTEXT SENTENCE about form/injuries].
Our odds: [TEAM A] win at [WIN_ODDS], draw at [DRAW_ODDS], [TEAM B] win at [LOSS_ODDS].
Key factors — [FACTOR1], [FACTOR2].
My expert prediction: [OUTCOME]!
Don't miss the action — follow Footboom Universe!
```

### BGM (`generate_music`)
```
Energetic sports broadcast background music. Fast-paced electronic beat with punchy drums,
driving bass line, and uplifting synth stabs. Stadium atmosphere feel, similar to pre-match hype music.
Tempo around 128 BPM.
[0:00-0:04] Intro: building tension with rising synth.
[0:04-0:12] Main: full energy beat with brass hits and electronic percussion.
[0:12-0:16] Outro: fade out with reverb tail.
Instrumental only, no vocals. Original melody, not recognizable from any existing music.
```

---

## ffmpeg Mix Command

```bash
ffmpeg -y \
  -stream_loop -1 -i paul_boom_video.mp4 \
  -i voiceover.wav \
  -i bgm.mp3 \
  -filter_complex "[1:a]volume=1.0[voice];[2:a]volume=0.15,atrim=0:{DURATION}[bgm];[voice][bgm]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" \
  -t {DURATION} \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 192k \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -r 30 \
  final_reel.mp4
```

---

## Instagram Caption Template

```
🔥 MATCH PREDICTION: [TEAM A] vs [TEAM B] [EMOJI1][EMOJI2]

[CONTEXT about the match]

📊 ODDS:
✅ [TEAM A] WIN — [WIN_ODDS]
🤝 DRAW — [DRAW_ODDS]
❌ [TEAM B] WIN — [LOSS_ODDS]

🔑 KEY FACTORS:
• [FACTOR1]
• [FACTOR2]
• [FACTOR3]

🎯 EXPERT PREDICTION: [OUTCOME]!

Don't miss the action — follow @footboom.universe for daily predictions!

#[Team1Hashtag] #[Team2Hashtag] #[Competition] #FootballPrediction #FootboomUniverse #PaulBoom #MatchPrediction #Football #Soccer
```
