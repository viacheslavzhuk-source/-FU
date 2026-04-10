# Footboom Universe — Instagram Auto-Poster v2.0 🚀⚽

Fully automated daily Instagram posting system for **Footboom Universe** (@footboom.universe).

## What It Does

Every day, the system automatically publishes **3 posts**:

| # | Time (UTC) | Time (Kyiv) | Content |
|---|---|---|---|
| 1 | 08:00 | 11:00 | 🎬 **Prediction Reel** — Paul Boom analyzes Match #1 |
| 2 | 14:00 | 17:00 | 🎬 **Prediction Reel** — Paul Boom analyzes Match #2 |
| 3 | 18:00 | 21:00 | 🌟 **Discovery Post** — Fan content, stats, throwbacks |

## How It Works

```
GitHub Actions (cron 3x/day)
        │
        ▼
  auto_post.py
        │
        ├── 1. Fetch today's top matches
        │       ├── api-football.com (if API key set)
        │       └── GPT-4.1-mini fallback (always works)
        │
        ├── 2. Generate Paul Boom prediction images (DALL-E 3)
        │       └── Composite: prediction infographic + Paul Boom avatar
        │
        ├── 3. Generate captions (GPT-4.1-mini)
        │       └── Match analysis, odds, prediction, CTA
        │
        ├── 4. Publish 2x Prediction Posts (Instagram Graph API)
        │
        ├── 5. Generate Discovery content (DALL-E 3 + GPT)
        │
        └── 6. Publish Discovery Post (Instagram Graph API)
```

## Setup

### 1. Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | ✅ Yes | OpenAI API key (GPT-4.1-mini + DALL-E 3) |
| `IG_ACCESS_TOKEN` | ✅ Yes | Long-lived Instagram Graph API token |
| `IG_ACCOUNT_ID` | ✅ Yes | Instagram Business Account ID |
| `FOOTBALL_API_KEY` | ⚡ Optional | api-football.com key for live match data |

### 2. Enable GitHub Actions

The workflow file is at `.github/workflows/instagram_autopost.yml`.
It runs automatically on schedule. No additional setup needed.

### 3. Manual Trigger

Go to **Actions → Footboom Universe Auto-Poster v2.0 → Run workflow**.

Options:
- `all` — Full pipeline (2 predictions + 1 discovery)
- `prediction` — Prediction reel only
- `discovery` — Discovery post only

## Files

| File | Description |
|---|---|
| `auto_post.py` | Main automation script |
| `.github/workflows/instagram_autopost.yml` | GitHub Actions workflow |
| `SPORTS_CALENDAR.md` | Full tournament schedule & content strategy |
| `README.md` | This file |

## Tournaments Covered

- 🏆 UEFA Champions League
- 🥈 UEFA Europa League
- 🥉 UEFA Conference League
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 English Premier League + FA Cup
- 🇪🇸 Spanish La Liga + Copa del Rey
- 🇩🇪 German Bundesliga + DFB-Pokal
- 🇮🇹 Italian Serie A + Coppa Italia
- 🇫🇷 French Ligue 1
- 🌍 FIFA World Cup 2026

## Content Strategy

See [SPORTS_CALENDAR.md](SPORTS_CALENDAR.md) for the full weekly content plan and tournament schedule.

---

*Powered by OpenAI GPT-4.1-mini + DALL-E 3 · Instagram Graph API · GitHub Actions*
