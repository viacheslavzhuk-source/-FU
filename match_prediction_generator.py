#!/usr/bin/env python3
"""
Footboom Universe - Match Prediction Post Generator
Generates beautiful Instagram posts with match predictions, odds, and analysis
"""

import json
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap

class MatchPredictionGenerator:
    def __init__(self, output_dir="prediction_posts"):
        """Initialize the prediction post generator"""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Image dimensions (Instagram square post)
        self.width = 1080
        self.height = 1350
        
        # Colors
        self.bg_dark = (20, 20, 30)
        self.red = (239, 68, 68)
        self.white = (255, 255, 255)
        self.light_gray = (200, 200, 200)
        self.dark_gray = (100, 100, 100)
    
    def create_prediction_post(self, match_data):
        """
        Create a match prediction post image
        
        match_data format:
        {
            "team1": {"name": "Manchester City", "logo_url": "..."},
            "team2": {"name": "Liverpool", "logo_url": "..."},
            "odds": {"win": 2.10, "draw": 3.40, "loss": 3.25},
            "key_factors": [
                "Form: MAN CITY WWD",
                "Injuries: LIVERPOOL Van Dijk OUT",
                "Head-to-Head: Evenly Matched"
            ],
            "analysis": "High-scoring game expected. Midfield battle crucial.",
            "prediction": "MAN CITY WIN",
            "date": "2026-04-10"
        }
        """
        
        # Create base image with dark background
        img = Image.new('RGB', (self.width, self.height), self.bg_dark)
        draw = ImageDraw.Draw(img)
        
        # Add gradient effect (simulate with rectangles)
        for i in range(self.height):
            opacity = int((i / self.height) * 30)
            color = (20 + opacity, 20 + opacity, 30 + opacity)
            draw.line([(0, i), (self.width, i)], fill=color)
        
        # Load fonts (fallback to default if not available)
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
            normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        except:
            title_font = ImageFont.load_default()
            large_font = ImageFont.load_default()
            medium_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        y_offset = 30
        
        # 1. Title banner (red)
        banner_height = 100
        draw.rectangle(
            [(40, y_offset), (self.width - 40, y_offset + banner_height)],
            fill=self.red
        )
        
        title_text = f"MATCH PREDICTION:\n{match_data['team1']['name'].upper()} vs {match_data['team2']['name'].upper()}"
        title_lines = title_text.split('\n')
        
        # Draw title text
        line_y = y_offset + 15
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) // 2
            draw.text((x, line_y), line, fill=self.white, font=title_font)
            line_y += 40
        
        y_offset += banner_height + 40
        
        # 2. Team logos and VS
        logo_size = 120
        logo_y = y_offset
        
        # Team 1 (left)
        team1_x = 100
        draw.text((team1_x - 20, logo_y + 50), match_data['team1']['name'].upper(), 
                 fill=self.white, font=medium_font)
        draw.ellipse(
            [(team1_x - logo_size//2, logo_y), (team1_x + logo_size//2, logo_y + logo_size)],
            outline=self.white, width=3
        )
        draw.text((team1_x - 30, logo_y + 40), "🏆", font=large_font)
        
        # VS in middle
        vs_x = self.width // 2
        draw.text((vs_x - 20, logo_y + 40), "VS", fill=self.red, font=large_font)
        
        # Team 2 (right)
        team2_x = self.width - 100
        draw.text((team2_x - 50, logo_y + 50), match_data['team2']['name'].upper(), 
                 fill=self.white, font=medium_font)
        draw.ellipse(
            [(team2_x - logo_size//2, logo_y), (team2_x + logo_size//2, logo_y + logo_size)],
            outline=self.white, width=3
        )
        draw.text((team2_x - 30, logo_y + 40), "⚽", font=large_font)
        
        y_offset += logo_size + 120
        
        # 3. Odds section
        odds_y = y_offset
        odds_box_height = 80
        
        # Draw odds box background
        draw.rectangle(
            [(40, odds_y), (self.width - 40, odds_y + odds_box_height)],
            fill=(40, 40, 50), outline=self.light_gray, width=2
        )
        
        # Odds values
        odds = match_data['odds']
        odds_items = [
            ("WIN", str(odds['win'])),
            ("DRAW", str(odds['draw'])),
            ("LOSS", str(odds['loss']))
        ]
        
        odds_x_positions = [150, 540, 930]
        for i, (label, value) in enumerate(odds_items):
            x = odds_x_positions[i]
            
            # Label
            draw.text((x - 30, odds_y + 10), label, fill=self.light_gray, font=small_font)
            
            # Value in red box
            draw.rectangle(
                [(x - 50, odds_y + 35), (x + 50, odds_y + 70)],
                fill=self.red
            )
            bbox = draw.textbbox((0, 0), value, font=large_font)
            text_width = bbox[2] - bbox[0]
            draw.text((x - text_width//2, odds_y + 38), value, fill=self.white, font=large_font)
        
        y_offset += odds_box_height + 30
        
        # 4. Key Factors section
        draw.text((50, y_offset), "KEY FACTORS:", fill=self.red, font=medium_font)
        y_offset += 45
        
        for factor in match_data['key_factors']:
            draw.text((70, y_offset), "• " + factor, fill=self.light_gray, font=normal_font)
            y_offset += 35
        
        y_offset += 15
        
        # 5. Analysis section
        draw.text((50, y_offset), "ANALYSIS:", fill=self.red, font=medium_font)
        y_offset += 45
        
        analysis_text = match_data['analysis']
        wrapped_analysis = textwrap.fill(analysis_text, width=60)
        for line in wrapped_analysis.split('\n'):
            draw.text((70, y_offset), line, fill=self.light_gray, font=normal_font)
            y_offset += 30
        
        y_offset += 20
        
        # 6. Expert Prediction (red banner)
        prediction_banner_height = 70
        draw.rectangle(
            [(40, y_offset), (self.width - 40, y_offset + prediction_banner_height)],
            fill=self.red
        )
        
        prediction_text = f"EXPERT PREDICTION: {match_data['prediction']}"
        bbox = draw.textbbox((0, 0), prediction_text, font=large_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, y_offset + 15), prediction_text, fill=self.white, font=large_font)
        
        y_offset += prediction_banner_height + 30
        
        # 7. Footboom Universe logo and CTA
        draw.text((self.width // 2 - 50, y_offset), "🏟️ FOOTBOOM UNIVERSE", 
                 fill=self.white, font=small_font)
        y_offset += 40
        
        draw.text((self.width // 2 - 80, y_offset), "What's your prediction?", 
                 fill=self.white, font=medium_font)
        
        # Save image
        filename = f"{match_data['team1']['name'].lower().replace(' ', '_')}_vs_{match_data['team2']['name'].lower().replace(' ', '_')}_{match_data['date']}.png"
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath)
        
        return filepath
    
    def generate_from_json(self, json_file):
        """Generate prediction posts from a JSON file"""
        with open(json_file, 'r') as f:
            matches = json.load(f)
        
        generated_files = []
        for match in matches:
            filepath = self.create_prediction_post(match)
            generated_files.append(filepath)
            print(f"✅ Generated: {filepath}")
        
        return generated_files


def create_sample_matches():
    """Create sample match data for testing"""
    sample_matches = [
        {
            "team1": {"name": "Manchester City", "logo_url": ""},
            "team2": {"name": "Liverpool", "logo_url": ""},
            "odds": {"win": 2.10, "draw": 3.40, "loss": 3.25},
            "key_factors": [
                "Form: MAN CITY WWD",
                "Injuries: LIVERPOOL Van Dijk OUT",
                "Head-to-Head: Evenly Matched"
            ],
            "analysis": "High-scoring game expected. Midfield battle crucial.",
            "prediction": "MAN CITY WIN",
            "date": "2026-04-10"
        },
        {
            "team1": {"name": "Real Madrid", "logo_url": ""},
            "team2": {"name": "Barcelona", "logo_url": ""},
            "odds": {"win": 1.95, "draw": 3.50, "loss": 3.80},
            "key_factors": [
                "Form: REAL MADRID WWW",
                "Injuries: BARCELONA Pedri DOUBTFUL",
                "Head-to-Head: Real Madrid Dominant"
            ],
            "analysis": "Real Madrid in excellent form. Barcelona struggling defensively.",
            "prediction": "REAL MADRID WIN",
            "date": "2026-04-11"
        },
        {
            "team1": {"name": "Bayern Munich", "logo_url": ""},
            "team2": {"name": "Borussia Dortmund", "logo_url": ""},
            "odds": {"win": 1.85, "draw": 3.60, "loss": 4.20},
            "key_factors": [
                "Form: BAYERN MUNICH WWD",
                "Injuries: DORTMUND Reus OUT",
                "Head-to-Head: Bayern Dominant"
            ],
            "analysis": "Bayern favored. Dortmund needs defensive reinforcement.",
            "prediction": "BAYERN WIN",
            "date": "2026-04-12"
        }
    ]
    
    return sample_matches


if __name__ == "__main__":
    # Initialize generator
    generator = MatchPredictionGenerator(output_dir="footboom_prediction_posts")
    
    # Create sample matches
    sample_matches = create_sample_matches()
    
    # Generate posts
    print("🚀 Generating match prediction posts...\n")
    for match in sample_matches:
        filepath = generator.create_prediction_post(match)
        print(f"✅ Generated: {filepath}")
    
    print("\n✨ All prediction posts generated successfully!")
    print(f"📁 Output directory: {generator.output_dir}")
    
    # Save sample JSON for reference
    with open("sample_matches.json", "w") as f:
        json.dump(sample_matches, f, indent=2)
    print("📄 Sample matches saved to: sample_matches.json")
