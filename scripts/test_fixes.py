import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

SRC_DIR = "MADIGA -20261109T093322Z-1-001/MADIGA"
PREVIEW_DIR = r"C:\Users\likhi\.gemini\antigravity\brain\1d1ca0ff-6359-45f4-ae60-10ce4ab7893a\final_media_previews"

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_IMPACT = "C:/Windows/Fonts/impact.ttf"
FONT_SERIF = "C:/Windows/Fonts/georgiab.ttf"
FONT_SEGOE = "C:/Windows/Fonts/segoeuib.ttf"

# --- PODCAST 5 ---
def fix_podcast_5():
    im = Image.open(os.path.join(SRC_DIR, "podcast5.png"))
    clean = im.copy()
    
    # Create an opaque, textured dark studio wall patch to cleanly replace y: 240..500
    # Sample upper dark wall (y: 60..200)
    arr = np.array(im)
    wall_sample = arr[70:210, 150:874] # 140x724
    wall_img = Image.fromarray(wall_sample).resize((824, 260), Image.Resampling.LANCZOS)
    
    # Make mask with soft feathered borders
    mask = Image.new("L", (824, 260), 255)
    m_draw = ImageDraw.Draw(mask)
    for i in range(35):
        alpha = int(255 * (i / 35.0))
        m_draw.rectangle([i, i, 824 - i, 260 - i], outline=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(15))
    
    clean.paste(wall_img, (100, 240), mask)
    
    # Add dark vignette
    draw = ImageDraw.Draw(clean)
    font_sub = ImageFont.truetype(FONT_BOLD, 36)
    font_main = ImageFont.truetype(FONT_BOLD, 62)
    
    t1 = "UNTIRING STRUGGLE FOR MADIGA RIGHTS"
    b1 = draw.textbbox((0, 0), t1, font=font_sub)
    x1 = (1024 - (b1[2]-b1[0])) // 2
    draw.text((x1+2, 312), t1, font=font_sub, fill=(0, 0, 0))
    draw.text((x1, 310), t1, font=font_sub, fill=(255, 255, 255))
    
    t2 = "MANDA KRISHNA MADIGA"
    b2 = draw.textbbox((0, 0), t2, font=font_main)
    x2 = (1024 - (b2[2]-b2[0])) // 2
    draw.text((x2+4, 394), t2, font=font_main, fill=(0, 0, 0))
    draw.text((x2, 390), t2, font=font_main, fill=(245, 179, 1))
    
    clean.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "podcast_5_test.jpg"))
    print("Podcast 5 test saved.")

# --- PODCAST 4 (BOTTOM) ---
def fix_podcast_4():
    im = Image.open(os.path.join(SRC_DIR, "podcast4.png"))
    clean = im.copy()
    
    # Table wood patch for bottom name: y: 1250..1380
    table_sample = clean.crop((100, 1200, 924, 1240)).resize((824, 130), Image.Resampling.LANCZOS)
    mask = Image.new("L", (824, 130), 255)
    m_draw = ImageDraw.Draw(mask)
    for i in range(25):
        alpha = int(255 * (i / 25.0))
        m_draw.rectangle([i, i, 824 - i, 130 - i], outline=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(10))
    clean.paste(table_sample, (100, 1260), mask)
    
    # Top text patch: y: 90..230
    wall_sample = clean.crop((200, 20, 824, 80)).resize((624, 150), Image.Resampling.LANCZOS)
    mask_top = Image.new("L", (624, 150), 255)
    mt_draw = ImageDraw.Draw(mask_top)
    for i in range(25):
        alpha = int(255 * (i / 25.0))
        mt_draw.rectangle([i, i, 624 - i, 150 - i], outline=alpha)
    mask_top = mask_top.filter(ImageFilter.GaussianBlur(10))
    clean.paste(wall_sample, (200, 90), mask_top)
    
    draw = ImageDraw.Draw(clean)
    font_main = ImageFont.truetype(FONT_BOLD, 52)
    font_sub = ImageFont.truetype(FONT_BOLD, 44)
    font_bot = ImageFont.truetype(FONT_BOLD, 62)
    
    t1 = "EVERY SONG CARRIES"
    b1 = draw.textbbox((0, 0), t1, font=font_main)
    x1 = (1024 - (b1[2]-b1[0])) // 2
    draw.text((x1+2, 112), t1, font=font_main, fill=(0, 0, 0))
    draw.text((x1, 110), t1, font=font_main, fill=(255, 255, 255))
    
    t2 = "A MOVEMENT'S HISTORY!"
    b2 = draw.textbbox((0, 0), t2, font=font_sub)
    x2 = (1024 - (b2[2]-b2[0])) // 2
    draw.text((x2+2, 172), t2, font=font_sub, fill=(0, 0, 0))
    draw.text((x2, 170), t2, font=font_sub, fill=(255, 255, 255))
    
    draw.arc([350, 230, 674, 280], start=200, end=340, fill=(245, 179, 1), width=3)
    
    t3 = "DAPPU RAMESH"
    b3 = draw.textbbox((0, 0), t3, font=font_bot)
    x3 = (1024 - (b3[2]-b3[0])) // 2
    draw.text((x3+3, 1303), t3, font=font_bot, fill=(0, 0, 0))
    draw.text((x3, 1300), t3, font=font_bot, fill=(245, 179, 1))
    
    draw.arc([300, 1400, 724, 1450], start=20, end=160, fill=(220, 20, 20), width=4)
    clean.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "podcast_4_test.jpg"))
    print("Podcast 4 test saved.")

# --- SONG 4 ---
def fix_song_4():
    im = Image.open(os.path.join(SRC_DIR, "Song4.jpeg"))
    clean = im.copy()
    
    # Opaque dark amber patch over y: 450..1800, x: 200..3800
    # Left sample x: 100..450, y: 500..1800
    patch = clean.crop((100, 500, 450, 1800)).resize((3600, 1400), Image.Resampling.LANCZOS)
    patch = patch.filter(ImageFilter.GaussianBlur(30))
    
    mask = Image.new("L", (3600, 1400), 255)
    m_draw = ImageDraw.Draw(mask)
    for i in range(120):
        alpha = int(255 * (i / 120.0))
        m_draw.rectangle([i, i, 3600 - i, 1400 - i], outline=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(50))
    
    clean.paste(patch, (200, 450), mask)
    
    draw = ImageDraw.Draw(clean)
    font_main = ImageFont.truetype(FONT_IMPACT, 320)
    font_sub = ImageFont.truetype(FONT_IMPACT, 260)
    font_eyebrow = ImageFont.truetype(FONT_BOLD, 130)
    
    t0 = "RHYTHM OF THE DURA"
    b0 = draw.textbbox((0, 0), t0, font=font_eyebrow)
    draw.text(((4000 - (b0[2]-b0[0]))//2, 550), t0, font=font_eyebrow, fill=(255, 240, 180))
    
    t1 = "AADUDAM"
    b1 = draw.textbbox((0, 0), t1, font=font_main)
    x1 = (4000 - (b1[2]-b1[0]))//2
    draw.text((x1+8, 808), t1, font=font_main, fill=(0, 40, 20), stroke_width=16, stroke_fill=(0, 40, 20))
    draw.text((x1, 800), t1, font=font_main, fill=(245, 179, 1), stroke_width=10, stroke_fill=(6, 78, 59))
    
    t2 = "DAPPULO DARUVEYYARA"
    b2 = draw.textbbox((0, 0), t2, font=font_sub)
    x2 = (4000 - (b2[2]-b2[0]))//2
    draw.text((x2+8, 1258), t2, font=font_sub, fill=(0, 40, 20), stroke_width=14, stroke_fill=(0, 40, 20))
    draw.text((x2, 1250), t2, font=font_sub, fill=(245, 179, 1), stroke_width=8, stroke_fill=(6, 78, 59))
    
    clean.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "song_4_test.jpg"))
    print("Song 4 test saved.")

# --- SONG 5 ---
def fix_song_5():
    im = Image.open(os.path.join(SRC_DIR, "song5.jpeg"))
    clean = im.copy()
    
    # Red gradient patch over y: 2650..3550, x: 200..3800
    patch = clean.crop((80, 2650, 480, 3550)).resize((3600, 900), Image.Resampling.LANCZOS)
    patch = patch.filter(ImageFilter.GaussianBlur(30))
    
    mask = Image.new("L", (3600, 900), 255)
    m_draw = ImageDraw.Draw(mask)
    for i in range(120):
        alpha = int(255 * (i / 120.0))
        m_draw.rectangle([i, i, 3600 - i, 900 - i], outline=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(50))
    
    clean.paste(patch, (200, 2650), mask)
    
    draw = ImageDraw.Draw(clean)
    font_main = ImageFont.truetype(FONT_IMPACT, 310)
    font_sub = ImageFont.truetype(FONT_BOLD, 130)
    
    t1 = "DALITHA PULULAMMA"
    b1 = draw.textbbox((0, 0), t1, font=font_main)
    x1 = (4000 - (b1[2]-b1[0]))//2
    draw.text((x1+8, 2908), t1, font=font_main, fill=(0, 0, 0), stroke_width=18, stroke_fill=(0, 0, 0))
    draw.text((x1, 2900), t1, font=font_main, fill=(245, 179, 1), stroke_width=10, stroke_fill=(50, 0, 0))
    
    t2 = "TIGERS OF DALIT RESISTANCE"
    b2 = draw.textbbox((0, 0), t2, font=font_sub)
    x2 = (4000 - (b2[2]-b2[0]))//2
    draw.text((x2+4, 3324), t2, font=font_sub, fill=(0, 0, 0))
    draw.text((x2, 3320), t2, font=font_sub, fill=(255, 255, 255))
    
    clean.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "song_5_test.jpg"))
    print("Song 5 test saved.")

# --- SONG 1 ---
def fix_song_1():
    im = Image.open(os.path.join(SRC_DIR, "Song1.jpeg"))
    clean = im.copy()
    
    # Sunset sky patch over y: 700..2600, x: 200..3800
    # Left sample x: 80..380, right sample x: 3620..3920
    left_crop = clean.crop((80, 700, 380, 2650)).resize((1800, 1950), Image.Resampling.LANCZOS)
    right_crop = clean.crop((3620, 700, 3920, 2650)).resize((1800, 1950), Image.Resampling.LANCZOS)
    sky_patch = Image.new("RGB", (3600, 1950))
    sky_patch.paste(left_crop, (0, 0))
    sky_patch.paste(right_crop, (1800, 0))
    sky_patch = sky_patch.filter(ImageFilter.GaussianBlur(80))
    
    mask = Image.new("L", (3600, 1950), 255)
    m_draw = ImageDraw.Draw(mask)
    for i in range(120):
        alpha = int(255 * (i / 120.0))
        m_draw.rectangle([i, i, 3600 - i, 1950 - i], outline=alpha)
    # Exclude singer hair at bottom-left of patch
    m_draw.ellipse([-200, 1500, 900, 2400], fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(40))
    
    clean.paste(sky_patch, (200, 700), mask)
    
    draw = ImageDraw.Draw(clean)
    font_sub = ImageFont.truetype(FONT_SEGOE, 130)
    font_main = ImageFont.truetype(FONT_IMPACT, 340)
    font_line2 = ImageFont.truetype(FONT_BOLD, 170)
    font_badge = ImageFont.truetype(FONT_BOLD, 120)
    
    t1 = "IN MEMORY OF COMRADE"
    b1 = draw.textbbox((0, 0), t1, font=font_sub)
    draw.text(((4000 - (b1[2]-b1[0]))//2, 1100), t1, font=font_sub, fill=(255, 230, 140))
    
    t2 = "DAPPU RAMESH"
    b2 = draw.textbbox((0, 0), t2, font=font_main)
    x2 = (4000 - (b2[2]-b2[0]))//2
    draw.text((x2+8, 1358), t2, font=font_main, fill=(0, 0, 0), stroke_width=16, stroke_fill=(0, 0, 0))
    draw.text((x2, 1350), t2, font=font_main, fill=(235, 30, 40), stroke_width=14, stroke_fill=(255, 255, 255))
    
    t3 = "ANNA SMRITHI"
    b3 = draw.textbbox((0, 0), t3, font=font_line2)
    x3 = (4000 - (b3[2]-b3[0]))//2
    draw.text((x3+5, 1805), t3, font=font_line2, fill=(0, 0, 0), stroke_width=8, stroke_fill=(0, 0, 0))
    draw.text((x3, 1800), t3, font=font_line2, fill=(255, 255, 255), stroke_width=6, stroke_fill=(180, 20, 20))
    
    t4 = "JNM • CNM TRIBUTE SONG"
    b4 = draw.textbbox((0, 0), t4, font=font_badge)
    x4 = (4000 - (b4[2]-b4[0]))//2
    draw.text((x4+4, 2154), t4, font=font_badge, fill=(0, 0, 0))
    draw.text((x4, 2150), t4, font=font_badge, fill=(255, 255, 255), stroke_width=4, stroke_fill=(200, 0, 0))
    
    clean.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "song_1_test.jpg"))
    print("Song 1 test saved.")

fix_podcast_5()
fix_podcast_4()
fix_song_4()
fix_song_5()
fix_song_1()
