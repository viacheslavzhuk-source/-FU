# Footboom Universe - Instagram Auto-Poster 🚀

This repository contains an automated Python script and GitHub Actions workflow to publish Instagram posts for **Footboom Universe** on a daily schedule.

## How it works

1. **GitHub Actions** triggers the script every day at 10:00 UTC (or manually via the Actions tab).
2. **OpenAI (GPT-4o-mini)** generates a relevant football topic and an engaging caption with hashtags.
3. **OpenAI (DALL-E 3)** generates a high-quality, cinematic football image based on the topic.
4. **Instagram Graph API** automatically publishes the image and caption to the connected Instagram Business account.

## Setup Instructions

To make this work, you need to configure three **Repository Secrets** in GitHub:

1. Go to your repository on GitHub.
2. Click on **Settings** > **Secrets and variables** > **Actions**.
3. Click **New repository secret** and add the following three secrets:

### Required Secrets

| Secret Name | Description |
| :--- | :--- |
| `OPENAI_API_KEY` | Your OpenAI API key for generating text and images. |
| `IG_ACCESS_TOKEN` | A long-lived Facebook Graph API access token with `instagram_basic`, `instagram_content_publish`, and `pages_show_list` permissions. |
| `IG_ACCOUNT_ID` | The Instagram Business Account ID connected to your Facebook Page. |

## Customizing the Schedule

By default, the bot posts every day at 10:00 UTC. To change this, edit the `.github/workflows/instagram_autopost.yml` file:

```yaml
on:
  schedule:
    # Change this cron expression (e.g., '0 18 * * *' for 18:00 UTC)
    - cron: '0 10 * * *'
```

## Manual Trigger

You can test the bot at any time without waiting for the schedule:
1. Go to the **Actions** tab in GitHub.
2. Select **Footboom Universe Auto-Poster** on the left.
3. Click **Run workflow** on the right.
