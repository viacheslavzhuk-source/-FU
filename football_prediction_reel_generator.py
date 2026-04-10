#!/usr/bin/env python3
"""
Football Prediction Reels Generator for Instagram
Generates animated video reels with match predictions, odds, and analysis
Optimized for Instagram Reels format (9:16 aspect ratio, 1080x1920 or 1440x2560)
"""

import json
import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
from datetime import datetime
import math

class FootballPredictionReelGenerator:
    def __init__(self, output_dir="prediction_reels"):
        """Initialize the prediction reel generator"""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Instagram Reels dimensions (9:16 aspect ratio)
        self.width = 1080
        self.height = 1920
        
        # Colors
        self.bg_dark = (15, 15, 25)
        self.bg_darker = (10, 10, 20)
        self.red = (239, 68, 68)
        self.red_dark = (220, 50, 50)
        self.white = (255, 255, 255)
        self.light_gray = (200, 200, 200)
        self.dark_gray = (100, 100, 100)
        self.accent_blue = (59, 130, 246)
        
        # FPS and duration settings
        self.fps = 30
        self.duration_seconds = 30  # Standard Instagram Reel
        self.total_frames = self.fps * self.duration_seconds
        
        # Frame timing (in frames)
        self.frame_timings = {
            'intro': (0, 60),           # 0-2 seconds: Intro animation
            'teams': (60, 180),         # 2-6 seconds: Team logos and VS
            'odds': (180, 300),         # 6-10 seconds: Odds display
            'key_factors': (300, 480),  # 10-16 seconds: Key factors
            'analysis': (480, 660),     # 16-22 seconds: Analysis
            'prediction': (660, 840),   # 22-28 seconds: Prediction banner
            'outro': (840, 900)         # 28-30 seconds: Outro with CTA
        }
    
    def create_frame(self, frame_num, match_data):
        """Create a single frame for the video"""
        img = Image.new('RGB', (self.width, self.height), self.bg_dark)
        draw = ImageDraw.Draw(img)
        
        # Load fonts
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
            large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
            medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
            normal_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
        except:
            title_font = ImageFont.load_default()
            large_font = ImageFont.load_default()
            medium_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Add animated gradient background
        self._draw_animated_background(draw, frame_num)
        
        # Determine which section to display based on frame number
        if frame_num < self.frame_timings['teams'][1]:
            self._draw_intro_section(draw, frame_num, match_data, title_font, large_font)
        elif frame_num < self.frame_timings['odds'][1]:
            self._draw_teams_section(draw, frame_num, match_data, large_font, medium_font)
        elif frame_num < self.frame_timings['key_factors'][1]:
            self._draw_odds_section(draw, frame_num, match_data, large_font, medium_font, normal_font)
        elif frame_num < self.frame_timings['analysis'][1]:
            self._draw_key_factors_section(draw, frame_num, match_data, medium_font, normal_font)
        elif frame_num < self.frame_timings['prediction'][1]:
            self._draw_analysis_section(draw, frame_num, match_data, medium_font, normal_font)
        elif frame_num < self.frame_timings['outro'][1]:
            self._draw_prediction_section(draw, frame_num, match_data, large_font, medium_font)
        else:
            self._draw_outro_section(draw, frame_num, match_data, medium_font, normal_font)
        
        return img
    
    def _draw_animated_background(self, draw, frame_num):
        """Draw animated background with gradient and effects"""
        # Animated gradient
        for i in range(self.height):
            # Create wave effect
            wave = math.sin((i / self.height + frame_num / 30) * math.pi * 2) * 10
            opacity = int((i / self.height) * 40 + wave)
            color = (
                15 + min(opacity, 40),
                15 + min(opacity, 40),
                25 + min(opacity, 40)
            )
            draw.line([(0, i), (self.width, i)], fill=color)
        
        # Add animated accent lines
        line_pos = (frame_num % 60) * (self.width / 60)
        draw.line([(line_pos - 100, 0), (line_pos, self.height)], fill=(239, 68, 68, 30), width=2)
    
    def _draw_intro_section(self, draw, frame_num, match_data, title_font, large_font):
        """Draw intro animation section"""
        progress = (frame_num - self.frame_timings['intro'][0]) / (self.frame_timings['intro'][1] - self.frame_timings['intro'][0])
        
        # Fade in title
        alpha = int(255 * min(progress * 2, 1))
        
        # Draw title banner with animation
        banner_y = 200 + (1 - progress) * 50
        banner_height = 120
        
        draw.rectangle(
            [(40, banner_y), (self.width - 40, banner_y + banner_height)],
            fill=self.red
        )
        
        title_text = f"MATCH PREDICTION"
        bbox = draw.textbbox((0, 0), title_text, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, banner_y + 20), title_text, fill=self.white, font=title_font)
        
        # Draw match info
        match_text = f"{match_data['team1']['name'].upper()} vs {match_data['team2']['name'].upper()}"
        bbox = draw.textbbox((0, 0), match_text, font=large_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, banner_y + 70), match_text, fill=self.white, font=large_font)
    
    def _draw_teams_section(self, draw, frame_num, match_data, large_font, medium_font):
        """Draw teams logos and VS section"""
        progress = (frame_num - self.frame_timings['teams'][0]) / (self.frame_timings['teams'][1] - self.frame_timings['teams'][0])
        
        # Animate team positions
        team1_x = 150 - (1 - progress) * 100
        team2_x = self.width - 150 + (1 - progress) * 100
        
        logo_size = 140
        logo_y = 400
        
        # Team 1 (left)
        draw.ellipse(
            [(team1_x - logo_size//2, logo_y), (team1_x + logo_size//2, logo_y + logo_size)],
            outline=self.red, width=4
        )
        draw.text((team1_x - 50, logo_y + 50), "⚽", font=large_font)
        
        # Team name
        team1_name = match_data['team1']['name'].upper()
        bbox = draw.textbbox((0, 0), team1_name, font=medium_font)
        text_width = bbox[2] - bbox[0]
        draw.text((team1_x - text_width//2, logo_y + 160), team1_name, fill=self.white, font=medium_font)
        
        # VS in middle
        vs_scale = 0.8 + progress * 0.4
        vs_size = int(60 * vs_scale)
        vs_x = self.width // 2
        draw.text((vs_x - 25, 480), "VS", fill=self.red, font=large_font)
        
        # Team 2 (right)
        draw.ellipse(
            [(team2_x - logo_size//2, logo_y), (team2_x + logo_size//2, logo_y + logo_size)],
            outline=self.red, width=4
        )
        draw.text((team2_x - 50, logo_y + 50), "⚽", font=large_font)
        
        # Team name
        team2_name = match_data['team2']['name'].upper()
        bbox = draw.textbbox((0, 0), team2_name, font=medium_font)
        text_width = bbox[2] - bbox[0]
        draw.text((team2_x - text_width//2, logo_y + 160), team2_name, fill=self.white, font=medium_font)
    
    def _draw_odds_section(self, draw, frame_num, match_data, large_font, medium_font, normal_font):
        """Draw odds display section"""
        progress = (frame_num - self.frame_timings['odds'][0]) / (self.frame_timings['odds'][1] - self.frame_timings['odds'][0])
        
        odds_y = 700
        odds_box_height = 140
        
        # Draw odds box background
        draw.rectangle(
            [(40, odds_y), (self.width - 40, odds_y + odds_box_height)],
            fill=(30, 30, 45), outline=self.red, width=3
        )
        
        # Draw title
        draw.text((60, odds_y + 10), "BETTING ODDS", fill=self.red, font=medium_font)
        
        # Odds values with animation
        odds = match_data['odds']
        odds_items = [
            ("WIN", str(odds['win'])),
            ("DRAW", str(odds['draw'])),
            ("LOSS", str(odds['loss']))
        ]
        
        odds_x_positions = [200, 540, 880]
        for i, (label, value) in enumerate(odds_items):
            x = odds_x_positions[i]
            
            # Animate scale
            scale = 0.8 + (progress * 0.2) if i == int(progress * 3) else 1.0
            
            # Label
            draw.text((x - 40, odds_y + 50), label, fill=self.light_gray, font=normal_font)
            
            # Value in red box
            draw.rectangle(
                [(x - 60, odds_y + 80), (x + 60, odds_y + 130)],
                fill=self.red
            )
            bbox = draw.textbbox((0, 0), value, font=large_font)
            text_width = bbox[2] - bbox[0]
            draw.text((x - text_width//2, odds_y + 85), value, fill=self.white, font=large_font)
    
    def _draw_key_factors_section(self, draw, frame_num, match_data, medium_font, normal_font):
        """Draw key factors section"""
        progress = (frame_num - self.frame_timings['key_factors'][0]) / (self.frame_timings['key_factors'][1] - self.frame_timings['key_factors'][0])
        
        y_offset = 700
        
        # Title
        draw.text((60, y_offset), "KEY FACTORS", fill=self.red, font=medium_font)
        y_offset += 60
        
        # Animate factors appearance
        for i, factor in enumerate(match_data['key_factors']):
            factor_progress = max(0, min(1, (progress - i * 0.3) * 3))
            alpha = int(255 * factor_progress)
            
            # Draw factor with fade in effect
            x_offset = (1 - factor_progress) * 50
            draw.text((60 + x_offset, y_offset), "• " + factor, fill=self.light_gray, font=normal_font)
            y_offset += 80
    
    def _draw_analysis_section(self, draw, frame_num, match_data, medium_font, normal_font):
        """Draw analysis section"""
        progress = (frame_num - self.frame_timings['analysis'][0]) / (self.frame_timings['analysis'][1] - self.frame_timings['analysis'][0])
        
        y_offset = 700
        
        # Title
        draw.text((60, y_offset), "ANALYSIS", fill=self.red, font=medium_font)
        y_offset += 60
        
        # Analysis text with word-by-word reveal effect
        analysis_text = match_data['analysis']
        wrapped_analysis = textwrap.fill(analysis_text, width=50)
        
        for line in wrapped_analysis.split('\n'):
            draw.text((60, y_offset), line, fill=self.light_gray, font=normal_font)
            y_offset += 50
    
    def _draw_prediction_section(self, draw, frame_num, match_data, large_font, medium_font):
        """Draw expert prediction section"""
        progress = (frame_num - self.frame_timings['prediction'][0]) / (self.frame_timings['prediction'][1] - self.frame_timings['prediction'][0])
        
        # Scale animation
        scale = 0.8 + progress * 0.2
        
        prediction_y = 900
        prediction_banner_height = 140
        
        # Draw prediction banner
        draw.rectangle(
            [(40, prediction_y), (self.width - 40, prediction_y + prediction_banner_height)],
            fill=self.red
        )
        
        # Title
        draw.text((60, prediction_y + 15), "EXPERT PREDICTION", fill=self.white, font=medium_font)
        
        # Prediction text
        prediction_text = match_data['prediction']
        bbox = draw.textbbox((0, 0), prediction_text, font=large_font)
        text_width = bbox[2] - bbox[0]
        x = (self.width - text_width) // 2
        draw.text((x, prediction_y + 70), prediction_text, fill=self.white, font=large_font)
    
    def _draw_outro_section(self, draw, frame_num, match_data, medium_font, normal_font):
        """Draw outro section with CTA"""
        progress = (frame_num - self.frame_timings['outro'][0]) / (self.frame_timings['outro'][1] - self.frame_timings['outro'][0])
        
        # Fade effect
        alpha = int(255 * (1 - progress))
        
        # Logo and branding
        y_offset = 900
        draw.text((self.width // 2 - 150, y_offset), "🏟️ FOOTBOOM UNIVERSE", 
                 fill=self.white, font=normal_font)
        y_offset += 80
        
        # CTA
        cta_text = "What's your prediction?"
        bbox = draw.textbbox((0, 0), cta_text, font=medium_font)
        text_width = bbox[2] - bbox[0]
        draw.text((self.width // 2 - text_width // 2, y_offset), cta_text, 
                 fill=self.red, font=medium_font)
        
        # Follow/Subscribe message
        y_offset += 100
        follow_text = "Follow for more predictions"
        bbox = draw.textbbox((0, 0), follow_text, font=normal_font)
        text_width = bbox[2] - bbox[0]
        draw.text((self.width // 2 - text_width // 2, y_offset), follow_text, 
                 fill=self.light_gray, font=normal_font)
    
    def generate_video_from_frames(self, frames_dir, output_video_path, fps=30):
        """Generate MP4 video from frames using ffmpeg"""
        # Create ffmpeg command
        input_pattern = os.path.join(frames_dir, "frame_%06d.png")
        
        cmd = [
            'ffmpeg',
            '-framerate', str(fps),
            '-i', input_pattern,
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'medium',
            '-crf', '23',
            output_video_path,
            '-y'  # Overwrite output file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error generating video: {e}")
            return False
    
    def create_prediction_reel(self, match_data, add_audio=False):
        """
        Create a complete prediction reel video
        
        match_data format:
        {
            "team1": {"name": "Manchester City"},
            "team2": {"name": "Liverpool"},
            "odds": {"win": 2.10, "draw": 3.40, "loss": 3.25},
            "key_factors": ["Form: ...", "Injuries: ...", "Head-to-Head: ..."],
            "analysis": "High-scoring game expected...",
            "prediction": "MAN CITY WIN",
            "date": "2026-04-10"
        }
        """
        
        # Create frames directory
        team1_name = match_data['team1']['name'].lower().replace(' ', '_')
        team2_name = match_data['team2']['name'].lower().replace(' ', '_')
        match_id = f"{team1_name}_vs_{team2_name}_{match_data['date']}"
        
        frames_dir = os.path.join(self.output_dir, f"frames_{match_id}")
        if not os.path.exists(frames_dir):
            os.makedirs(frames_dir)
        
        # Generate all frames
        print(f"🎬 Generating frames for {match_id}...")
        for frame_num in range(self.total_frames):
            if frame_num % 30 == 0:
                print(f"  Frame {frame_num}/{self.total_frames}")
            
            frame = self.create_frame(frame_num, match_data)
            frame_path = os.path.join(frames_dir, f"frame_{frame_num:06d}.png")
            frame.save(frame_path)
        
        # Generate video
        video_path = os.path.join(self.output_dir, f"prediction_reel_{match_id}.mp4")
        print(f"🎥 Generating video...")
        
        if self.generate_video_from_frames(frames_dir, video_path, self.fps):
            print(f"✅ Video created: {video_path}")
            return video_path
        else:
            print(f"❌ Failed to generate video")
            return None
    
    def create_reels_from_json(self, json_file):
        """Generate prediction reels from a JSON file"""
        with open(json_file, 'r') as f:
            matches = json.load(f)
        
        generated_videos = []
        for match in matches:
            video_path = self.create_prediction_reel(match)
            if video_path:
                generated_videos.append(video_path)
        
        return generated_videos


def main():
    """Main function to demonstrate usage"""
    # Initialize generator
    generator = FootballPredictionReelGenerator(output_dir="football_prediction_reels")
    
    # Sample match data
    sample_match = {
        "team1": {"name": "Manchester City"},
        "team2": {"name": "Liverpool"},
        "odds": {"win": 2.10, "draw": 3.40, "loss": 3.25},
        "key_factors": [
            "Form: MAN CITY WWD",
            "Injuries: LIVERPOOL Van Dijk OUT",
            "Head-to-Head: Evenly Matched"
        ],
        "analysis": "High-scoring game expected. Midfield battle will be crucial for both teams.",
        "prediction": "MAN CITY WIN",
        "date": "2026-04-10"
    }
    
    # Generate reel
    print("🚀 Starting Football Prediction Reel Generator...\n")
    video_path = generator.create_prediction_reel(sample_match)
    
    if video_path:
        print(f"\n✨ Reel generated successfully!")
        print(f"📁 Output: {video_path}")
    else:
        print("\n❌ Failed to generate reel")


if __name__ == "__main__":
    main()
