#!/usr/bin/env python3
"""
Footboom Universe - Instagram Auto Poster v2.0
Daily automated posting system:
  - 2x Prediction Reels with Paul Boom (top match predictions)
  - 1x Discovery/Fan Content Post
Designed to run on GitHub Actions via cron schedule.
"""

import os
import sys
import json
import random
import time
import requests
from datetime import datetime, timezone
from openai import OpenAI

# ─── Configuration ────────────────────────────────────────────────────────────
OPENAI_API_KEY  = os.environ.get("OPENAI_API_KEY")
IG_ACCESS_TOKEN = os.environ.get("IG_ACCESS_TOKEN")
IG_ACCOUNT_ID   = os.environ.get("IG_ACCOUNT_ID")
FOOTBALL_API_KEY = os.environ.get("FOOTBALL_API_KEY", "")  # optional: api-football.com

if not all([OPENAI_API_KEY, IG_ACCESS_TOKEN, IG_ACCOUNT_ID]):
    print("❌ Missing required environment variables.")
    print("   Required: OPENAI_API_KEY, IG_ACCESS_TOKEN, IG_ACCOUNT_ID")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

# ─── Sports Calendar ──────────────────────────────────────────────────────────
# Top tournaments tracked by Footboom Universe
TOP_TOURNAMENTS = [
    "UEFA Champions League",
    "UEFA Europa League",
    "UEFA Conference League",
    "English Premier League",
    "Spanish La Liga",
    "German Bundesliga",
    "Italian Serie A",
    "French Ligue 1",
    "FIFA World Cup 2026",
    "UEFA EURO 2028",
    "Copa del Rey",
    "FA Cup",
    "DFB-Pokal",
    "Coppa Italia",
]

# Discovery/Fan content themes
DISCOVERY_THEMES = [
    "Rising star spotlight — young talent under 21 taking the world by storm",
    "Legendary football moment throwback — iconic goal or match from history",
    "Tactical breakdown — formation and pressing style of a top European club",
    "Transfer window analysis — biggest rumored deals and their impact",
    "Golden Boot race — top scorers stats and who will win it",
    "Manager spotlight — tactical genius behind a top team's success",
    "Underdog story — a smaller club punching above their weight this season",
    "Stadium spotlight — the most iconic football stadiums in the world",
    "Fan culture — the most passionate supporter groups in world football",
    "Record breakers — players chasing all-time football records right now",
    "Head-to-head history — classic rivalry stats and memorable encounters",
    "Best XI of the week — top performers across all European leagues",
]

# Paul Boom avatar description (for image generation prompts)
PAUL_BOOM_DESC = (
    "Paul Boom, a professional male sports commentator and football analyst, "
    "40-45 years old, short dark brown hair, stubble beard, intense focused grey-blue eyes, "
    "dark navy blue suit, white dress shirt, dark blue tie, black professional headset with microphone, "
    "bust shot in the bottom-right corner of the frame, looking directly at camera with authoritative expression"
)

# ─── Fetch Today's Top Matches ────────────────────────────────────────────────

def fetch_top_matches_from_api():
    """Fetch today's top matches from api-football.com if API key is available."""
    if not FOOTBALL_API_KEY:
        return []
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": FOOTBALL_API_KEY}
    params = {"date": today, "status": "NS"}  # NS = Not Started
    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        data = res.json()
        fixtures = data.get("response", [])
        # Filter top leagues only
        top_league_ids = {2, 3, 4, 5, 39, 140, 78, 135, 61}  # UCL, UEL, PL, LaLiga, BL, SA, L1
        top = [f for f in fixtures if f["league"]["id"] in top_league_ids]
        top.sort(key=lambda x: x["league"]["id"])
        return top[:5]
    except Exception as e:
        print(f"⚠️  API fetch failed: {e}")
        return []


def generate_match_context_with_gpt(match_count=2):
    """Use GPT to generate realistic top match predictions for today."""
    today_str = datetime.now(timezone.utc).strftime("%A, %B %d, %Y")
    prompt = f"""Today is {today_str}. You are a football data expert for Footboom Universe.

Generate {match_count} realistic top European football matches that would be played today or in the next 2 days.
Choose from: UEFA Champions League, Premier League, La Liga, Bundesliga, Serie A, Europa League.

For each match return a JSON object with these exact keys:
- tournament: tournament name
- home_team: home team name
- away_team: away team name  
- match_date: date string like "April 14, 2026"
- context: one sentence about the match stakes (e.g. "Second leg, Bayern leads 2-1 on aggregate")
- home_form: last 3 results as string like "WWD"
- away_form: last 3 results as string like "LWW"
- key_injury: most important injury/suspension or "None"
- head_to_head: one sentence h2h fact
- analysis: one sentence tactical analysis
- odds_home_win: decimal odds like 2.10
- odds_draw: decimal odds like 3.40
- odds_away_win: decimal odds like 2.80
- prediction: one of "HOME WIN", "DRAW", "AWAY WIN", or team name + "ADVANCE"
- prediction_reasoning: one sentence explanation

Return a JSON array of {match_count} match objects."""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    result = json.loads(response.choices[0].message.content)
    # Handle both array and wrapped object responses
    if isinstance(result, list):
        return result
    for v in result.values():
        if isinstance(v, list):
            return v
    return [result]


# ─── Image Generation ─────────────────────────────────────────────────────────

def generate_prediction_background(match):
    """Generate a prediction infographic image for a match using DALL-E 3."""
    home = match["home_team"]
    away = match["away_team"]
    tournament = match["tournament"]
    context = match.get("context", "")
    odds_home = match["odds_home_win"]
    odds_draw = match["odds_draw"]
    odds_away = match["odds_away_win"]
    prediction = match["prediction"]

    prompt = (
        f"Professional football match prediction infographic poster for Instagram Reels, vertical 9:16 format. "
        f"Dark atmospheric stadium background with dramatic lighting and blurred crowd. "
        f"Top section: bold red banner with white bold text 'MATCH PREDICTION: {home.upper()} vs {away.upper()}'. "
        f"Below: '{tournament.upper()} — {context.upper()}' in smaller white text on dark background. "
        f"Middle section: white semi-transparent card panel. "
        f"Left side: {home} football club crest/logo. Center: large bold 'VS' text in red. Right side: {away} football club crest/logo. "
        f"Below crests: three columns showing betting odds — 'WIN {odds_home}' in red box, 'DRAW {odds_draw}' in grey box, 'LOSS {odds_away}' in dark box. "
        f"KEY FACTORS section in bold red text. "
        f"ANALYSIS section with one bullet point. "
        f"Bottom red banner: 'EXPERT PREDICTION: {prediction.upper()}'. "
        f"Very bottom: Footboom Universe logo circle with F letter. Below that: white text 'What is your prediction?'. "
        f"Bottom right corner reserved for commentator avatar. "
        f"Professional sports broadcast design, clean modern layout, no watermarks."
    )

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1792",
        quality="standard",
        n=1,
    )
    return response.data[0].url


def generate_paul_boom_reel_image(match):
    """Generate a Paul Boom prediction reel composite image."""
    home = match["home_team"]
    away = match["away_team"]
    tournament = match["tournament"]
    prediction = match["prediction"]
    odds_home = match["odds_home_win"]
    odds_draw = match["odds_draw"]
    odds_away = match["odds_away_win"]
    context = match.get("context", "")
    injury = match.get("key_injury", "None")
    analysis = match.get("analysis", "")

    prompt = (
        f"Professional football prediction Instagram Reels video frame, vertical 9:16 format. "
        f"Full background shows: dark stadium atmosphere, red banner 'MATCH PREDICTION: {home.upper()} vs {away.upper()}', "
        f"'{tournament.upper()}' subtitle, {home} crest on left and {away} crest on right with VS between them, "
        f"context banner '{context.upper()}', white stats card WIN {odds_home} / DRAW {odds_draw} / LOSS {odds_away}, "
        f"KEY FACTORS section with injury info '{injury}', ANALYSIS: '{analysis}', "
        f"red banner 'EXPERT PREDICTION: {prediction.upper()}', Footboom Universe logo, 'What is your prediction?' text. "
        f"In the bottom right corner: {PAUL_BOOM_DESC}, mouth open mid-speech, energetic and decisive expression, "
        f"right index finger pointing confidently toward camera. "
        f"Photorealistic quality, sharp details, professional broadcast lighting, cinematic sports TV atmosphere."
    )

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1792",
        quality="standard",
        n=1,
    )
    return response.data[0].url


def generate_discovery_image(theme):
    """Generate a discovery/fan content image."""
    prompt = (
        f"Professional football Instagram post image. Theme: {theme}. "
        f"Footboom Universe style: dark navy blue and emerald green accents, ultra HD, "
        f"professional sports photography, cinematic lighting, dramatic composition. "
        f"Include subtle Footboom Universe branding. No text overlays. "
        f"Square 1:1 format, high quality."
    )
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url


# ─── Caption Generation ───────────────────────────────────────────────────────

def generate_prediction_caption(match):
    """Generate Instagram caption for a prediction reel."""
    home = match["home_team"]
    away = match["away_team"]
    tournament = match["tournament"]
    context = match.get("context", "")
    home_form = match.get("home_form", "")
    away_form = match.get("away_form", "")
    injury = match.get("key_injury", "None")
    h2h = match.get("head_to_head", "")
    analysis = match.get("analysis", "")
    prediction = match["prediction"]
    reasoning = match.get("prediction_reasoning", "")
    odds_home = match["odds_home_win"]
    odds_draw = match["odds_draw"]
    odds_away = match["odds_away_win"]

    caption = f"""🔥 MATCH PREDICTION: {home.upper()} vs {away.upper()} 🔥

Paul Boom breaks down this {tournament} clash! ⚽️🏆

📊 KEY FACTORS:
🔹 Form: {home} {home_form} | {away} {away_form}
🔹 {f"Injury/Suspension: {injury}" if injury and injury != "None" else f"H2H: {h2h}"}
🔹 Context: {context}

🧠 ANALYSIS:
{analysis}

💰 ODDS: WIN {odds_home} | DRAW {odds_draw} | LOSS {odds_away}

🎯 EXPERT PREDICTION: {prediction}
{reasoning}

What's your prediction? Drop it in the comments! 👇

🔔 Don't miss the action — follow @footboom.universe for daily predictions!

#FootboomUniverse #PaulBoom #{home.replace(" ", "")} #{away.replace(" ", "")} #{tournament.replace(" ", "").replace("UEFA", "UCL")} #FootballPrediction #MatchPreview #SportsBetting #FootballAnalysis #PremierLeague #ChampionsLeague"""
    return caption


def generate_discovery_caption(theme):
    """Generate an engaging discovery/fan content caption using GPT."""
    prompt = f"""You are the lead content creator for 'Footboom Universe', a premium football Instagram account.
Create an engaging Instagram caption for a discovery/fan content post about: {theme}

Style: dynamic, professional, passionate football fan tone. Use emojis appropriately.
End with: "🔔 Don't miss the action — follow @footboom.universe for daily football content!"
Include 10-12 relevant hashtags including #FootboomUniverse.

Return only the caption text, no JSON."""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


# ─── Instagram Publishing ─────────────────────────────────────────────────────

def publish_image_post(image_url, caption):
    """Publish an image post to Instagram via Graph API."""
    print("   📱 Creating media container...")
    container_url = f"https://graph.facebook.com/v19.0/{IG_ACCOUNT_ID}/media"
    container_res = requests.post(container_url, data={
        "image_url": image_url,
        "caption": caption,
        "access_token": IG_ACCESS_TOKEN
    })
    container_data = container_res.json()
    if "id" not in container_data:
        print(f"   ❌ Container failed: {container_data}")
        return False
    creation_id = container_data["id"]

    print("   📤 Publishing post...")
    publish_res = requests.post(
        f"https://graph.facebook.com/v19.0/{IG_ACCOUNT_ID}/media_publish",
        data={"creation_id": creation_id, "access_token": IG_ACCESS_TOKEN}
    )
    publish_data = publish_res.json()
    if "id" not in publish_data:
        print(f"   ❌ Publish failed: {publish_data}")
        return False
    print(f"   ✅ Published! Post ID: {publish_data['id']}")
    return True


def publish_reel(video_url, caption, cover_url=None):
    """Publish a Reel to Instagram via Graph API."""
    print("   📱 Creating reel container...")
    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": "true",
        "access_token": IG_ACCESS_TOKEN
    }
    if cover_url:
        payload["cover_url"] = cover_url

    container_res = requests.post(
        f"https://graph.facebook.com/v19.0/{IG_ACCOUNT_ID}/media",
        data=payload
    )
    container_data = container_res.json()
    if "id" not in container_data:
        print(f"   ❌ Container failed: {container_data}")
        return False
    creation_id = container_data["id"]

    # Wait for video processing
    print("   ⏳ Waiting for video processing...")
    for attempt in range(12):
        time.sleep(10)
        status_res = requests.get(
            f"https://graph.facebook.com/v19.0/{creation_id}",
            params={"fields": "status_code", "access_token": IG_ACCESS_TOKEN}
        )
        status = status_res.json().get("status_code", "")
        print(f"      Status: {status}")
        if status == "FINISHED":
            break
        if status == "ERROR":
            print("   ❌ Video processing error")
            return False

    print("   📤 Publishing reel...")
    publish_res = requests.post(
        f"https://graph.facebook.com/v19.0/{IG_ACCOUNT_ID}/media_publish",
        data={"creation_id": creation_id, "access_token": IG_ACCESS_TOKEN}
    )
    publish_data = publish_res.json()
    if "id" not in publish_data:
        print(f"   ❌ Publish failed: {publish_data}")
        return False
    print(f"   ✅ Reel published! Post ID: {publish_data['id']}")
    return True


# ─── Main Pipeline ────────────────────────────────────────────────────────────

def main():
    print("🚀 Footboom Universe Auto-Poster v2.0 starting...")
    print(f"📅 Date: {datetime.now(timezone.utc).strftime('%A, %B %d, %Y %H:%M UTC')}")
    print("=" * 60)

    results = {"prediction_reels": [], "discovery_post": None}

    # ── Step 1: Get today's top matches ──────────────────────────────────────
    print("\n🔍 Fetching today's top matches...")
    matches = fetch_top_matches_from_api()
    if not matches:
        print("   ℹ️  No live API data — generating matches with GPT...")
        matches = generate_match_context_with_gpt(match_count=2)
    else:
        matches = matches[:2]

    print(f"   ✅ Got {len(matches)} matches to preview")

    # ── Step 2: Post 2 Prediction Reels ──────────────────────────────────────
    for i, match in enumerate(matches, 1):
        home = match.get("home_team", "Team A")
        away = match.get("away_team", "Team B")
        print(f"\n🎬 [{i}/2] Generating prediction reel: {home} vs {away}")

        try:
            # Generate composite Paul Boom image
            print("   🎨 Generating Paul Boom prediction image...")
            image_url = generate_paul_boom_reel_image(match)

            # Generate caption
            caption = generate_prediction_caption(match)
            print("   📝 Caption generated")

            # Publish as image post (reels require video; image posts work as carousel/post)
            success = publish_image_post(image_url, caption)
            results["prediction_reels"].append({
                "match": f"{home} vs {away}",
                "success": success
            })

            # Delay between posts to avoid rate limits
            if i < len(matches):
                print("   ⏳ Waiting 30s before next post...")
                time.sleep(30)

        except Exception as e:
            print(f"   ❌ Error for {home} vs {away}: {e}")
            results["prediction_reels"].append({"match": f"{home} vs {away}", "success": False})

    # ── Step 3: Post 1 Discovery/Fan Content ─────────────────────────────────
    print("\n🌟 [3/3] Generating discovery/fan content post...")
    theme = random.choice(DISCOVERY_THEMES)
    print(f"   🎯 Theme: {theme}")

    try:
        print("   ⏳ Waiting 30s before discovery post...")
        time.sleep(30)

        print("   🎨 Generating discovery image...")
        disc_image_url = generate_discovery_image(theme)

        print("   📝 Generating caption...")
        disc_caption = generate_discovery_caption(theme)

        success = publish_image_post(disc_image_url, disc_caption)
        results["discovery_post"] = {"theme": theme, "success": success}

    except Exception as e:
        print(f"   ❌ Discovery post error: {e}")
        results["discovery_post"] = {"theme": theme, "success": False}

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("📊 DAILY POSTING SUMMARY")
    print("=" * 60)
    for r in results["prediction_reels"]:
        status = "✅" if r["success"] else "❌"
        print(f"  {status} Prediction Reel: {r['match']}")
    if results["discovery_post"]:
        d = results["discovery_post"]
        status = "✅" if d["success"] else "❌"
        print(f"  {status} Discovery Post: {d['theme'][:60]}...")

    all_ok = all(r["success"] for r in results["prediction_reels"]) and \
             (results["discovery_post"] or {}).get("success", False)

    if all_ok:
        print("\n🎉 All posts published successfully!")
    else:
        print("\n⚠️  Some posts failed. Check logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
