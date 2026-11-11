import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC_DIR = "MADIGA -20261109T093322Z-1-001/MADIGA"
ENG_DIR = "ENG-20261110T042858Z-1-001/ENG"
POSTERS_EN = "assets/madiga/posters/en"
POSTERS_TE = "assets/madiga/posters/te"
BANNERS_EN = "assets/madiga/banners/en"
BANNERS_TE = "assets/madiga/banners/te"
PREVIEW_DIR = "C:/Users/likhi/.gemini/antigravity/brain/1d1ca0ff-6359-45f4-ae60-10ce4ab7893a/preview_songs_eng"

os.makedirs(PREVIEW_DIR, exist_ok=True)
os.makedirs(ENG_DIR, exist_ok=True)
os.makedirs(POSTERS_EN, exist_ok=True)
os.makedirs(POSTERS_TE, exist_ok=True)
os.makedirs(BANNERS_EN, exist_ok=True)
os.makedirs(BANNERS_TE, exist_ok=True)

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_IMPACT = "C:/Windows/Fonts/impact.ttf"
FONT_SERIF = "C:/Windows/Fonts/georgiab.ttf"
FONT_SEGOE = "C:/Windows/Fonts/segoeuib.ttf"

def draw_text_with_shadow(draw, text, pos, font, fill=(255, 255, 255), shadow_color=(0, 0, 0), shadow_offset=(4, 4), stroke_width=0, stroke_fill=(0, 0, 0)):
    x, y = pos
    if shadow_offset != (0, 0):
        draw.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=shadow_color, stroke_width=stroke_width, stroke_fill=shadow_color)
    draw.text(pos, text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)

print("Setup completed successfully.")
