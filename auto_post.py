#!/usr/bin/env python3
"""
Footboom Universe - Instagram Auto Poster
Generates a football post using OpenAI and publishes it via Instagram Graph API.
Designed to run on GitHub Actions.
"""

import os
import sys
import json
import random
import requests
from openai import OpenAI

# Configuration from environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
IG_ACCESS_TOKEN = os.environ.get("IG_ACCESS_TOKEN")
IG_ACCOUNT_ID = os.environ.get("IG_ACCOUNT_ID")

if not all([OPENAI_API_KEY, IG_ACCESS_TOKEN, IG_ACCOUNT_ID]):
    print("❌ Missing required environment variables.")
    print("Please set OPENAI_API_KEY, IG_ACCESS_TOKEN, and IG_ACCOUNT_ID.")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

# Post themes based on Footboom Universe strategy
THEMES = [
    "Tactical analysis of a recent major European match",
    "Rising star spotlight (young talent under 21)",
    "Legendary football moment throwback",
    "Transfer rumor or confirmed deal analysis",
    "Top scorer statistics and golden boot race",
    "Managerial tactics and formation breakdown",
    "Underdog team success story"
]

def generate_content():
    """Generate image prompt and caption using GPT-4o-mini"""
    theme = random.choice(THEMES)
    print(f"🎯 Selected theme: {theme}")
    
    system_prompt = """You are the lead content creator for 'Footboom Universe', a premium football Instagram account.
Your style is dynamic, professional, and engaging. You use emojis appropriately but not excessively.
Always include relevant hashtags at the end, including #FootboomUniverse."""
    
    user_prompt = f"""Create an Instagram post about: {theme}.
    
Return a JSON object with two keys:
1. 'image_prompt': A highly detailed prompt for DALL-E 3 to generate a photorealistic, cinematic football image. Include 'Footboom Universe style, dark navy blue and emerald green accents, ultra HD, professional sports photography'.
2. 'caption': The Instagram caption text, including emojis and hashtags."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

def generate_image(prompt):
    """Generate image using DALL-E 3"""
    print("🎨 Generating image...")
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

def publish_to_instagram(image_url, caption):
    """Publish to Instagram using Graph API"""
    print("📱 Publishing to Instagram...")
    
    # Step 1: Create media container
    container_url = f"https://graph.facebook.com/v19.0/{IG_ACCOUNT_ID}/media"
    container_payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": IG_ACCESS_TOKEN
    }
    
    container_res = requests.post(container_url, data=container_payload)
    container_data = container_res.json()
    
    if "id" not in container_data:
        print(f"❌ Failed to create media container: {container_data}")
        return False
        
    creation_id = container_data["id"]
    print(f"✅ Media container created: {creation_id}")
    
    # Step 2: Publish container
    publish_url = f"https://graph.facebook.com/v19.0/{IG_ACCOUNT_ID}/media_publish"
    publish_payload = {
        "creation_id": creation_id,
        "access_token": IG_ACCESS_TOKEN
    }
    
    publish_res = requests.post(publish_url, data=publish_payload)
    publish_data = publish_res.json()
    
    if "id" not in publish_data:
        print(f"❌ Failed to publish media: {publish_data}")
        return False
        
    print(f"✅ Post published successfully! ID: {publish_data['id']}")
    return True

def main():
    print("🚀 Starting Footboom Universe Auto-Poster")
    
    try:
        # 1. Generate content
        content = generate_content()
        print("\n📝 Generated Caption:")
        print(content["caption"])
        
        # 2. Generate image
        image_url = generate_image(content["image_prompt"])
        print(f"\n🖼️ Image URL: {image_url}")
        
        # 3. Publish
        success = publish_to_instagram(image_url, content["caption"])
        
        if success:
            print("\n🎉 Auto-posting completed successfully!")
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error during execution: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
