# 📅 Footboom Universe — Sports Calendar 2026

## Posting Strategy
| Time (UTC) | Time (Kyiv) | Content Type |
|---|---|---|
| 08:00 | 11:00 | 🎬 Prediction Reel #1 (Paul Boom) |
| 14:00 | 17:00 | 🎬 Prediction Reel #2 (Paul Boom) |
| 18:00 | 21:00 | 🌟 Discovery / Fan Content Post |

---

## 🏆 Top Tournaments Tracked

### UEFA Champions League 2025/26
| Round | Dates |
|---|---|
| Quarter-Finals 1st Leg | April 7–8, 2026 |
| Quarter-Finals 2nd Leg | April 14–15, 2026 |
| Semi-Finals 1st Leg | April 28–29, 2026 |
| Semi-Finals 2nd Leg | May 5–6, 2026 |
| **Final** | **May 30, 2026 — Allianz Arena, Munich** |

### UEFA Europa League 2025/26
| Round | Dates |
|---|---|
| Quarter-Finals 1st Leg | April 10, 2026 |
| Quarter-Finals 2nd Leg | April 17, 2026 |
| Semi-Finals 1st Leg | May 1, 2026 |
| Semi-Finals 2nd Leg | May 8, 2026 |
| **Final** | **May 20, 2026 — San Mamés, Bilbao** |

### UEFA Conference League 2025/26
| Round | Dates |
|---|---|
| Quarter-Finals | April 9–10 & 16–17, 2026 |
| Semi-Finals | May 1 & 8, 2026 |
| **Final** | **May 27, 2026 — Wrocław** |

### 🏴󠁧󠁢󠁥󠁮󠁧󠁿 English Premier League
| Event | Dates |
|---|---|
| Matchweek 31–38 | April–May 2026 |
| Season End | May 24, 2026 |
| FA Cup Final | May 16, 2026 |

### 🇪🇸 Spanish La Liga
| Event | Dates |
|---|---|
| Matchweeks 30–38 | April–May 2026 |
| Season End | May 24, 2026 |
| Copa del Rey Final | April 26, 2026 |

### 🇩🇪 German Bundesliga
| Event | Dates |
|---|---|
| Matchweeks 29–34 | April–May 2026 |
| Season End | May 23, 2026 |
| DFB-Pokal Final | May 23, 2026 |

### 🇮🇹 Italian Serie A
| Event | Dates |
|---|---|
| Matchweeks 31–38 | April–May 2026 |
| Season End | May 24, 2026 |
| Coppa Italia Final | May 13, 2026 |

### 🇫🇷 French Ligue 1
| Event | Dates |
|---|---|
| Matchweeks 29–34 | April–May 2026 |
| Season End | May 24, 2026 |

### 🌍 FIFA World Cup 2026
| Round | Dates |
|---|---|
| Group Stage | June 11 – July 2, 2026 |
| Round of 32 | July 4–7, 2026 |
| Round of 16 | July 9–12, 2026 |
| Quarter-Finals | July 15–16, 2026 |
| Semi-Finals | July 19–20, 2026 |
| **Final** | **July 23, 2026 — MetLife Stadium, New York** |

---

## 🎬 Content Plan by Day Type

### Match Day (Tuesday–Thursday, weekends)
- **Post 1 (08:00 UTC):** Paul Boom prediction reel — Match 1 of the day
- **Post 2 (14:00 UTC):** Paul Boom prediction reel — Match 2 of the day
- **Post 3 (18:00 UTC):** Discovery post — tactical analysis, stats, fan content

### Non-Match Day (Monday, Friday)
- **Post 1 (10:00 UTC):** Paul Boom — Weekend preview / upcoming big matches
- **Post 2 (15:00 UTC):** Discovery post — throwback, rising star, transfer news
- **Post 3 (19:00 UTC):** Fan engagement — poll, quiz, prediction challenge

---

## 🤖 Automation Setup

### Required GitHub Secrets
| Secret | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4.1-mini and DALL-E 3 |
| `IG_ACCESS_TOKEN` | Long-lived Instagram Graph API access token |
| `IG_ACCOUNT_ID` | Instagram Business Account ID |
| `FOOTBALL_API_KEY` | (Optional) api-football.com key for live match data |

### How to Set Up
1. Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**
2. Add all required secrets listed above
3. The workflow runs automatically 3x per day via cron schedule
4. You can also trigger manually via **Actions** → **Run workflow**

### Manual Trigger Options
- `all` — Run full pipeline (2 predictions + 1 discovery)
- `prediction` — Post only a prediction reel
- `discovery` — Post only a discovery/fan content post

---

## 📊 Weekly Content Mix Target

| Content Type | Posts/Week | Goal |
|---|---|---|
| Prediction Reels (Paul Boom) | 14 | Drive engagement & credibility |
| Discovery / Fan Content | 7 | Grow reach & new followers |
| **Total** | **21** | **3 posts/day** |
