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
PREVIEW_DIR = r"C:\Users\likhi\.gemini\antigravity\brain\1d1ca0ff-6359-45f4-ae60-10ce4ab7893a\final_media_previews"

for d in [ENG_DIR, POSTERS_EN, POSTERS_TE, BANNERS_EN, BANNERS_TE, PREVIEW_DIR]:
    os.makedirs(d, exist_ok=True)

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_IMPACT = "C:/Windows/Fonts/impact.ttf"
FONT_SERIF = "C:/Windows/Fonts/georgiab.ttf"
FONT_SEGOE = "C:/Windows/Fonts/segoeuib.ttf"
FONT_TREBUC = "C:/Windows/Fonts/trebucbd.ttf"

def make_banner(poster_img, is_podcast=False):
    """Creates a high-production 1920x1080 cinematic banner from a 2:3 vertical poster."""
    bw, bh = 1920, 1080
    banner = Image.new("RGB", (bw, bh), (0, 0, 0))
    
    # 1. Background: Blurred, scaled poster with deep dark vignette
    bg = poster_img.resize((bw, int(bw * poster_img.height / poster_img.width)), Image.Resampling.LANCZOS)
    # Crop to banner height from center
    crop_top = max(0, (bg.height - bh) // 2)
    bg = bg.crop((0, crop_top, bw, crop_top + bh))
    bg = bg.filter(ImageFilter.GaussianBlur(35))
    
    # Darken background strongly
    dark_overlay = Image.new("RGBA", (bw, bh), (0, 0, 0, 175))
    bg = Image.alpha_composite(bg.convert("RGBA"), dark_overlay)
    
    # Left-to-right gradient overlay to pure OLED black on the left half
    grad_mask = Image.new("L", (bw, bh), 0)
    for x in range(bw):
        alpha = int(255 * max(0, min(1, (1.0 - (x / (bw * 0.75))))))
        grad_mask.paste(alpha, (x, 0, x + 1, bh))
    black_cover = Image.new("RGBA", (bw, bh), (0, 0, 0, 255))
    bg.paste(black_cover, (0, 0), grad_mask)
    
    banner.paste(bg.convert("RGB"), (0, 0))
    
    # 2. Hero Subject Placement on Right Half
    subject_h = int(bh * 0.94)
    subject_w = int(subject_h * (poster_img.width / poster_img.height))
    subject = poster_img.resize((subject_w, subject_h), Image.Resampling.LANCZOS)
    
    # Subtle drop shadow behind subject
    shadow_pad = 20
    shadow = Image.new("RGBA", (subject_w + shadow_pad * 2, subject_h + shadow_pad * 2), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rectangle([shadow_pad, shadow_pad, subject_w + shadow_pad, subject_h + shadow_pad], fill=(0, 0, 0, 200))
    shadow = shadow.filter(ImageFilter.GaussianBlur(15))
    
    sub_x = int(bw * 0.58)
    sub_y = (bh - subject_h) // 2
    
    banner.paste(shadow, (sub_x - shadow_pad, sub_y - shadow_pad), shadow)
    banner.paste(subject, (sub_x, sub_y))
    
    return banner

print("Banner engine initialized.")

def process_song_1():
    print("Processing Song 1...")
    src_path = os.path.join(SRC_DIR, "Song1.jpeg")
    im = Image.open(src_path)
    arr = np.array(im)
    
    # Inpaint Telugu text
    mask = np.zeros((6000, 4000), dtype=np.uint8)
    text_box = arr[700:2700, 300:3800]
    text_mask = ((text_box[:,:,0]>200) & (text_box[:,:,1]>200) & (text_box[:,:,2]>200)) | \
                ((text_box[:,:,0]>160) & (text_box[:,:,1]<60) & (text_box[:,:,2]<60))
    mask[700:2700, 300:3800] = text_mask.astype(np.uint8) * 255
    kernel = np.ones((25, 25), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    # Inpaint at full resolution in chunks or resize
    small_img = cv2.resize(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), (2000, 3000))
    small_mask = cv2.resize(dilated, (2000, 3000))
    inpainted = cv2.inpaint(small_img, small_mask, 5, cv2.INPAINT_TELEA)
    clean_im = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)).resize((4000, 6000), Image.Resampling.LANCZOS)
    
    # English typography
    draw = ImageDraw.Draw(clean_im)
    font_sub = ImageFont.truetype(FONT_SEGOE, 130)
    font_main = ImageFont.truetype(FONT_IMPACT, 340)
    font_line2 = ImageFont.truetype(FONT_BOLD, 170)
    font_badge = ImageFont.truetype(FONT_BOLD, 120)
    
    # In Memory of Comrade
    t1 = "IN MEMORY OF COMRADE"
    bbox1 = draw.textbbox((0, 0), t1, font=font_sub)
    w1 = bbox1[2] - bbox1[0]
    x1 = (4000 - w1) // 2
    draw.text((x1 + 4, 1104), t1, font=font_sub, fill=(0, 0, 0))
    draw.text((x1, 1100), t1, font=font_sub, fill=(255, 225, 120))
    
    # DAPPU RAMESH
    t2 = "DAPPU RAMESH"
    bbox2 = draw.textbbox((0, 0), t2, font=font_main)
    w2 = bbox2[2] - bbox2[0]
    x2 = (4000 - w2) // 2
    # Shadow and white stroke
    draw.text((x2 + 8, 1358), t2, font=font_main, fill=(0, 0, 0), stroke_width=16, stroke_fill=(0, 0, 0))
    draw.text((x2, 1350), t2, font=font_main, fill=(235, 30, 40), stroke_width=14, stroke_fill=(255, 255, 255))
    
    # ANNA SMRITHI
    t3 = "ANNA SMRITHI"
    bbox3 = draw.textbbox((0, 0), t3, font=font_line2)
    w3 = bbox3[2] - bbox3[0]
    x3 = (4000 - w3) // 2
    draw.text((x3 + 5, 1805), t3, font=font_line2, fill=(0, 0, 0), stroke_width=8, stroke_fill=(0, 0, 0))
    draw.text((x3, 1800), t3, font=font_line2, fill=(255, 255, 255), stroke_width=6, stroke_fill=(180, 20, 20))
    
    # JNM • CNM TRIBUTE SONG
    t4 = "JNM • CNM TRIBUTE SONG"
    bbox4 = draw.textbbox((0, 0), t4, font=font_badge)
    w4 = bbox4[2] - bbox4[0]
    x4 = (4000 - w4) // 2
    draw.text((x4 + 4, 2154), t4, font=font_badge, fill=(0, 0, 0))
    draw.text((x4, 2150), t4, font=font_badge, fill=(255, 255, 255), stroke_width=4, stroke_fill=(200, 0, 0))
    
    # Save master English
    eng_master_path = os.path.join(ENG_DIR, "Song_1_English.jpg")
    clean_im.save(eng_master_path, quality=95)
    
    # Web posters (800x1200)
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "song_1.jpg"), quality=90)
    im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_TE, "song_1.jpg"), quality=90)
    
    # Banners (1920x1080)
    make_banner(clean_im).save(os.path.join(BANNERS_EN, "song_1_banner.jpg"), quality=90)
    make_banner(im).save(os.path.join(BANNERS_TE, "song_1_banner.jpg"), quality=90)
    
    # Preview
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "song_1_preview.jpg"))
    print("Song 1 completed successfully.")

def process_song_2():
    print("Processing Song 2...")
    src_path = os.path.join(SRC_DIR, "Song2.jpeg")
    im = Image.open(src_path)
    arr = np.array(im)
    
    left = arr[:3200, 150:151, :].astype(float)
    right = arr[:3200, 3850:3851, :].astype(float)
    base_col = (left + right) / 2.0
    x = np.arange(4000)
    dist = np.abs(x - 2000) / 2000.0
    factor = (1.0 + 0.08 * (1.0 - dist**2)).reshape(1, 4000, 1)
    clean_top = np.clip(base_col * factor, 0, 255).astype(np.uint8)
    
    arr_clean = arr.copy()
    # Replace background outside the circle apex (y < 3180)
    for y in range(3200):
        for xi in range(4000):
            # circle check: apex is at y=3190, x=2000
            # If above 3180, safe to replace, or if outside circle
            if y < 3180:
                arr_clean[y, xi] = clean_top[y, xi]
            elif (xi - 2000)**2 + (y - 4445)**2 >= (1255)**2:
                # Outside circle
                arr_clean[y, xi] = clean_top[min(y, 3199), xi]
                
    clean_im = Image.fromarray(arr_clean)
    draw = ImageDraw.Draw(clean_im)
    
    font_sub = ImageFont.truetype(FONT_SEGOE, 150)
    font_main = ImageFont.truetype(FONT_IMPACT, 340)
    font_line2 = ImageFont.truetype(FONT_IMPACT, 260)
    font_tag = ImageFont.truetype(FONT_BOLD, 120)
    
    # O ARUNA PATHAKAMA
    t1 = "O ARUNA PATHAKAMA"
    b1 = draw.textbbox((0, 0), t1, font=font_sub)
    draw.text(((4000 - (b1[2]-b1[0]))//2, 850), t1, font=font_sub, fill=(245, 179, 1))
    
    # RED SALUTES
    t2 = "RED SALUTES"
    b2 = draw.textbbox((0, 0), t2, font=font_main)
    x2 = (4000 - (b2[2]-b2[0]))//2
    draw.text((x2 + 8, 1208), t2, font=font_main, fill=(0, 0, 0), stroke_width=14, stroke_fill=(0, 0, 0))
    draw.text((x2, 1200), t2, font=font_main, fill=(255, 255, 255), stroke_width=6, stroke_fill=(40, 0, 0))
    
    # TO THE RED FLAG
    t3 = "TO THE RED FLAG"
    b3 = draw.textbbox((0, 0), t3, font=font_line2)
    x3 = (4000 - (b3[2]-b3[0]))//2
    draw.text((x3 + 8, 1658), t3, font=font_line2, fill=(0, 0, 0), stroke_width=12, stroke_fill=(0, 0, 0))
    draw.text((x3, 1650), t3, font=font_line2, fill=(255, 255, 255))
    
    # REVOLUTIONARY FOLK ANTHEM
    t4 = "REVOLUTIONARY FOLK ANTHEM"
    b4 = draw.textbbox((0, 0), t4, font=font_tag)
    draw.text(((4000 - (b4[2]-b4[0]))//2, 2100), t4, font=font_tag, fill=(245, 179, 1))
    
    # Save master English
    eng_master_path = os.path.join(ENG_DIR, "Song_2_English.jpg")
    clean_im.save(eng_master_path, quality=95)
    
    # Web posters
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "song_2.jpg"), quality=90)
    im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_TE, "song_2.jpg"), quality=90)
    
    # Banners
    make_banner(clean_im).save(os.path.join(BANNERS_EN, "song_2_banner.jpg"), quality=90)
    make_banner(im).save(os.path.join(BANNERS_TE, "song_2_banner.jpg"), quality=90)
    
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "song_2_preview.jpg"))
    print("Song 2 completed successfully.")

def process_song_3():
    print("Processing Song 3...")
    src_path = os.path.join(SRC_DIR, "Song3.jpeg")
    im = Image.open(src_path)
    arr = np.array(im)
    
    mask = np.zeros((6000, 4000), dtype=np.uint8)
    box = arr[3000:4800, 300:3300]
    blue_mask = (box[:,:,2].astype(int) - box[:,:,0].astype(int) > 20) & (box[:,:,2] > 50)
    dark_line = (box[1300:1800, :] < 60).all(axis=-1)
    blue_mask[1300:1800, :] |= dark_line
    mask[3000:4800, 300:3300] = blue_mask.astype(np.uint8) * 255
    kernel = np.ones((25, 25), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    small_img = cv2.resize(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), (2000, 3000))
    small_mask = cv2.resize(dilated, (2000, 3000))
    inpainted = cv2.inpaint(small_img, small_mask, 5, cv2.INPAINT_TELEA)
    clean_im = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)).resize((4000, 6000), Image.Resampling.LANCZOS)
    
    # Draw soft white backing cloud to ensure crisp typography
    cloud = Image.new("RGBA", (4000, 6000), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(cloud)
    c_draw.ellipse([400, 3100, 3500, 4600], fill=(255, 255, 255, 140))
    cloud = cloud.filter(ImageFilter.GaussianBlur(80))
    clean_im.paste(cloud, (0, 0), cloud)
    
    draw = ImageDraw.Draw(clean_im)
    font_main = ImageFont.truetype(FONT_SERIF, 280)
    font_sub = ImageFont.truetype(FONT_SEGOE, 220)
    font_desc = ImageFont.truetype(FONT_BOLD, 120)
    
    # MADIGA DANDORA
    t1 = "MADIGA DANDORA"
    b1 = draw.textbbox((0, 0), t1, font=font_main)
    draw.text(((4000 - (b1[2]-b1[0]))//2, 3250), t1, font=font_main, fill=(15, 32, 67))
    
    # CULTURAL TROUPE
    t2 = "CULTURAL TROUPE"
    b2 = draw.textbbox((0, 0), t2, font=font_sub)
    draw.text(((4000 - (b2[2]-b2[0]))//2, 3620), t2, font=font_sub, fill=(20, 45, 95))
    
    # Decorative line
    draw.line([900, 3960, 3100, 3960], fill=(15, 32, 67), width=8)
    
    # DAPPU • DARUVU • BEATS OF RESISTANCE
    t3 = "DAPPU • DARUVU • BEATS OF RESISTANCE"
    b3 = draw.textbbox((0, 0), t3, font=font_desc)
    draw.text(((4000 - (b3[2]-b3[0]))//2, 4030), t3, font=font_desc, fill=(15, 32, 67))
    
    eng_master_path = os.path.join(ENG_DIR, "Song_3_English.jpg")
    clean_im.save(eng_master_path, quality=95)
    
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "song_3.jpg"), quality=90)
    im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_TE, "song_3.jpg"), quality=90)
    
    make_banner(clean_im).save(os.path.join(BANNERS_EN, "song_3_banner.jpg"), quality=90)
    make_banner(im).save(os.path.join(BANNERS_TE, "song_3_banner.jpg"), quality=90)
    
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "song_3_preview.jpg"))
    print("Song 3 completed successfully.")

def process_song_4():
    print("Processing Song 4...")
    src_path = os.path.join(SRC_DIR, "Song4.jpeg")
    im = Image.open(src_path)
    arr = np.array(im)
    
    mask = np.zeros((6000, 4000), dtype=np.uint8)
    box = arr[300:2100, 300:3700]
    yellow_text = (box[:,:,0]>160) & (box[:,:,1]>140) & (box[:,:,2]<80)
    dark_stroke = (box[:,:,0]<50) & (box[:,:,1]>40) & (box[:,:,2]<50)
    mask[300:2100, 300:3700] = (yellow_text | dark_stroke).astype(np.uint8) * 255
    kernel = np.ones((25, 25), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    small_img = cv2.resize(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), (2000, 3000))
    small_mask = cv2.resize(dilated, (2000, 3000))
    inpainted = cv2.inpaint(small_img, small_mask, 5, cv2.INPAINT_TELEA)
    clean_im = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)).resize((4000, 6000), Image.Resampling.LANCZOS)
    
    draw = ImageDraw.Draw(clean_im)
    font_main = ImageFont.truetype(FONT_IMPACT, 320)
    font_sub = ImageFont.truetype(FONT_IMPACT, 260)
    font_eyebrow = ImageFont.truetype(FONT_BOLD, 130)
    
    # Eyebrow
    t0 = "RHYTHM OF THE DURA"
    b0 = draw.textbbox((0, 0), t0, font=font_eyebrow)
    draw.text(((4000 - (b0[2]-b0[0]))//2, 550), t0, font=font_eyebrow, fill=(255, 240, 180))
    
    # AADUDAM
    t1 = "AADUDAM"
    b1 = draw.textbbox((0, 0), t1, font=font_main)
    x1 = (4000 - (b1[2]-b1[0]))//2
    draw.text((x1+8, 808), t1, font=font_main, fill=(0, 40, 20), stroke_width=16, stroke_fill=(0, 40, 20))
    draw.text((x1, 800), t1, font=font_main, fill=(245, 179, 1), stroke_width=10, stroke_fill=(6, 78, 59))
    
    # DAPPULO DARUVEYYARA
    t2 = "DAPPULO DARUVEYYARA"
    b2 = draw.textbbox((0, 0), t2, font=font_sub)
    x2 = (4000 - (b2[2]-b2[0]))//2
    draw.text((x2+8, 1258), t2, font=font_sub, fill=(0, 40, 20), stroke_width=14, stroke_fill=(0, 40, 20))
    draw.text((x2, 1250), t2, font=font_sub, fill=(245, 179, 1), stroke_width=8, stroke_fill=(6, 78, 59))
    
    eng_master_path = os.path.join(ENG_DIR, "Song_4_English.jpg")
    clean_im.save(eng_master_path, quality=95)
    
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "song_4.jpg"), quality=90)
    im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_TE, "song_4.jpg"), quality=90)
    
    make_banner(clean_im).save(os.path.join(BANNERS_EN, "song_4_banner.jpg"), quality=90)
    make_banner(im).save(os.path.join(BANNERS_TE, "song_4_banner.jpg"), quality=90)
    
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "song_4_preview.jpg"))
    print("Song 4 completed successfully.")

def process_song_5():
    print("Processing Song 5...")
    src_path = os.path.join(SRC_DIR, "song5.jpeg")
    im = Image.open(src_path)
    arr = np.array(im)
    
    mask = np.zeros((6000, 4000), dtype=np.uint8)
    box = arr[2700:3600, 300:3900]
    yellow_text = (box[:,:,0]>180) & (box[:,:,1]>160) & (box[:,:,2]<50)
    dark_stroke = (box[:,:,0]<50) & (box[:,:,1]<50) & (box[:,:,2]<50)
    mask[2700:3600, 300:3900] = (yellow_text | dark_stroke).astype(np.uint8) * 255
    kernel = np.ones((25, 25), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    small_img = cv2.resize(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), (2000, 3000))
    small_mask = cv2.resize(dilated, (2000, 3000))
    inpainted = cv2.inpaint(small_img, small_mask, 5, cv2.INPAINT_TELEA)
    clean_im = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)).resize((4000, 6000), Image.Resampling.LANCZOS)
    
    # Soft crimson glow over inpaint area
    glow = Image.new("RGBA", (4000, 6000), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([400, 2750, 3600, 3550], fill=(160, 10, 15, 180))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    clean_im.paste(glow, (0, 0), glow)
    
    draw = ImageDraw.Draw(clean_im)
    font_main = ImageFont.truetype(FONT_IMPACT, 310)
    font_sub = ImageFont.truetype(FONT_BOLD, 130)
    
    # DALITHA PULULAMMA
    t1 = "DALITHA PULULAMMA"
    b1 = draw.textbbox((0, 0), t1, font=font_main)
    x1 = (4000 - (b1[2]-b1[0]))//2
    draw.text((x1+8, 2908), t1, font=font_main, fill=(0, 0, 0), stroke_width=18, stroke_fill=(0, 0, 0))
    draw.text((x1, 2900), t1, font=font_main, fill=(245, 179, 1), stroke_width=10, stroke_fill=(50, 0, 0))
    
    # TIGERS OF DALIT RESISTANCE
    t2 = "TIGERS OF DALIT RESISTANCE"
    b2 = draw.textbbox((0, 0), t2, font=font_sub)
    x2 = (4000 - (b2[2]-b2[0]))//2
    draw.text((x2+4, 3324), t2, font=font_sub, fill=(0, 0, 0))
    draw.text((x2, 3320), t2, font=font_sub, fill=(255, 255, 255))
    
    eng_master_path = os.path.join(ENG_DIR, "Song_5_English.jpg")
    clean_im.save(eng_master_path, quality=95)
    
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "song_5.jpg"), quality=90)
    im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_TE, "song_5.jpg"), quality=90)
    
    make_banner(clean_im).save(os.path.join(BANNERS_EN, "song_5_banner.jpg"), quality=90)
    make_banner(im).save(os.path.join(BANNERS_TE, "song_5_banner.jpg"), quality=90)
    
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "song_5_preview.jpg"))
    print("Song 5 completed successfully.")

def process_podcast_1():
    print("Processing Podcast 1...")
    src_path = os.path.join(SRC_DIR, "podcast1.png")
    im = Image.open(src_path)
    arr = np.array(im)
    
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box = arr[140:420, 70:950]
    white_text = (box[:,:,0]>200) & (box[:,:,1]>200) & (box[:,:,2]>200)
    yellow_text = (box[:,:,0]>180) & (box[:,:,1]>130) & (box[:,:,2]<50)
    mask[140:420, 70:950] = (white_text | yellow_text).astype(np.uint8) * 255
    kernel = np.ones((9, 9), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    inpainted = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), dilated, 5, cv2.INPAINT_TELEA)
    clean_im = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
    
    draw = ImageDraw.Draw(clean_im)
    font_top = ImageFont.truetype(FONT_SERIF, 48)
    font_name = ImageFont.truetype(FONT_BOLD, 54)
    
    # 1994 – THE GENESIS OF MRPS!
    t1 = "1994 – THE GENESIS OF MRPS!"
    b1 = draw.textbbox((0, 0), t1, font=font_top)
    x1 = (1024 - (b1[2]-b1[0])) // 2
    draw.text((x1+2, 172), t1, font=font_top, fill=(0, 0, 0))
    draw.text((x1, 170), t1, font=font_top, fill=(255, 255, 255))
    
    # DANDU VEERAYYA MADIGA
    t2 = "DANDU VEERAYYA MADIGA"
    b2 = draw.textbbox((0, 0), t2, font=font_name)
    x2 = (1024 - (b2[2]-b2[0])) // 2
    draw.text((x2+2, 242), t2, font=font_name, fill=(0, 0, 0))
    draw.text((x2, 240), t2, font=font_name, fill=(245, 179, 1))
    
    # Golden arc
    draw.arc([300, 320, 724, 380], start=200, end=340, fill=(245, 179, 1), width=3)
    
    eng_master_path = os.path.join(ENG_DIR, "podcast_1_English.png")
    clean_im.save(eng_master_path)
    
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "podcast_1.jpg"), quality=90)
    im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_TE, "podcast_1.jpg"), quality=90)
    
    make_banner(clean_im, is_podcast=True).save(os.path.join(BANNERS_EN, "podcast_1_banner.jpg"), quality=90)
    make_banner(im, is_podcast=True).save(os.path.join(BANNERS_TE, "podcast_1_banner.jpg"), quality=90)
    
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "podcast_1_preview.jpg"))
    print("Podcast 1 completed successfully.")

def process_podcast_2():
    print("Processing Podcast 2...")
    src_path = os.path.join(SRC_DIR, "podcast2.png")
    im = Image.open(src_path)
    arr = np.array(im)
    
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box_top = arr[110:440, 100:950]
    yellow_top = (box_top[:,:,0]>180) & (box_top[:,:,1]>130) & (box_top[:,:,2]<60)
    white_top = (box_top[:,:,0]>200) & (box_top[:,:,1]>200) & (box_top[:,:,2]>200)
    mask[110:440, 100:950] = (yellow_top | white_top).astype(np.uint8) * 255
    
    box_bot = arr[1350:1460, 150:850]
    white_bot = (box_bot[:,:,0]>180) & (box_bot[:,:,1]>180) & (box_bot[:,:,2]>180)
    mask[1350:1460, 150:850] = white_bot.astype(np.uint8) * 255
    
    kernel = np.ones((9, 9), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    inpainted = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), dilated, 5, cv2.INPAINT_TELEA)
    clean_im = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
    
    draw = ImageDraw.Draw(clean_im)
    font_main = ImageFont.truetype(FONT_BOLD, 54)
    font_sub = ImageFont.truetype(FONT_BOLD, 48)
    font_badge = ImageFont.truetype(FONT_BOLD, 38)
    
    # MADIGA CORPORATION
    t1 = "MADIGA CORPORATION"
    b1 = draw.textbbox((0, 0), t1, font=font_main)
    x1 = (1024 - (b1[2]-b1[0])) // 2
    draw.text((x1+2, 142), t1, font=font_main, fill=(0, 0, 0))
    draw.text((x1, 140), t1, font=font_main, fill=(245, 179, 1))
    
    # THE UNTOLD STORY!
    t2 = "THE UNTOLD STORY!"
    b2 = draw.textbbox((0, 0), t2, font=font_sub)
    x2 = (1024 - (b2[2]-b2[0])) // 2
    draw.text((x2+2, 212), t2, font=font_sub, fill=(0, 0, 0))
    draw.text((x2, 210), t2, font=font_sub, fill=(255, 255, 255))
    
    # Golden arc
    draw.arc([300, 275, 724, 335], start=200, end=340, fill=(245, 179, 1), width=3)
    
    # Bottom badge: KOMMURI KANAKARAO MADIGA
    t3 = "KOMMURI KANAKARAO MADIGA"
    b3 = draw.textbbox((0, 0), t3, font=font_badge)
    x3 = (1024 - (b3[2]-b3[0])) // 2
    draw.text((x3, 1395), t3, font=font_badge, fill=(255, 255, 255))
    
    eng_master_path = os.path.join(ENG_DIR, "podcast_2_English.png")
    clean_im.save(eng_master_path)
    
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "podcast_2.jpg"), quality=90)
    im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_TE, "podcast_2.jpg"), quality=90)
    
    make_banner(clean_im, is_podcast=True).save(os.path.join(BANNERS_EN, "podcast_2_banner.jpg"), quality=90)
    make_banner(im, is_podcast=True).save(os.path.join(BANNERS_TE, "podcast_2_banner.jpg"), quality=90)
    
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "podcast_2_preview.jpg"))
    print("Podcast 2 completed successfully.")

def process_podcast_3():
    print("Processing Podcast 3...")
    src_path = os.path.join(SRC_DIR, "podcast3.png")
    im = Image.open(src_path)
    arr = np.array(im)
    
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box_top = arr[110:520, 100:950]
    white_top = (box_top[:,:,0]>200) & (box_top[:,:,1]>200) & (box_top[:,:,2]>200)
    yellow_top = (box_top[:,:,0]>180) & (box_top[:,:,1]>130) & (box_top[:,:,2]<60)
    mask[110:520, 100:950] = (yellow_top | white_top).astype(np.uint8) * 255
    kernel = np.ones((9, 9), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    inpainted = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), dilated, 5, cv2.INPAINT_TELEA)
    clean_im = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
    
    draw = ImageDraw.Draw(clean_im)
    font_main = ImageFont.truetype(FONT_SERIF, 50)
    font_sub = ImageFont.truetype(FONT_BOLD, 46)
    font_name = ImageFont.truetype(FONT_BOLD, 44)
    
    # 1994: THE EMERGENCE OF MRPS
    t1 = "1994: THE EMERGENCE OF MRPS"
    b1 = draw.textbbox((0, 0), t1, font=font_main)
    x1 = (1024 - (b1[2]-b1[0])) // 2
    draw.text((x1+2, 142), t1, font=font_main, fill=(0, 0, 0))
    draw.text((x1, 140), t1, font=font_main, fill=(255, 255, 255))
    
    # HOW THE MOVEMENT BEGAN?
    t2 = "HOW THE MOVEMENT BEGAN?"
    b2 = draw.textbbox((0, 0), t2, font=font_sub)
    x2 = (1024 - (b2[2]-b2[0])) // 2
    draw.text((x2+2, 212), t2, font=font_sub, fill=(0, 0, 0))
    draw.text((x2, 210), t2, font=font_sub, fill=(245, 179, 1))
    
    # KRUPAKAR MADIGA
    t3 = "KRUPAKAR MADIGA"
    b3 = draw.textbbox((0, 0), t3, font=font_name)
    x3 = (1024 - (b3[2]-b3[0])) // 2
    draw.text((x3+2, 282), t3, font=font_name, fill=(0, 0, 0))
    draw.text((x3, 280), t3, font=font_name, fill=(255, 255, 255))
    
    # Gold line
    draw.line([x3, 335, x3 + (b3[2]-b3[0]), 335], fill=(245, 179, 1), width=3)
    
    eng_master_path = os.path.join(ENG_DIR, "podcast_3_English.png")
    clean_im.save(eng_master_path)
    
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "podcast_3.jpg"), quality=90)
    im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_TE, "podcast_3.jpg"), quality=90)
    
    make_banner(clean_im, is_podcast=True).save(os.path.join(BANNERS_EN, "podcast_3_banner.jpg"), quality=90)
    make_banner(im, is_podcast=True).save(os.path.join(BANNERS_TE, "podcast_3_banner.jpg"), quality=90)
    
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "podcast_3_preview.jpg"))
    print("Podcast 3 completed successfully.")

def process_podcast_4():
    print("Processing Podcast 4...")
    src_path = os.path.join(SRC_DIR, "podcast4.png")
    im = Image.open(src_path)
    arr = np.array(im)
    
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box_top = arr[80:380, 200:900]
    white_top = (box_top[:,:,0]>180) & (box_top[:,:,1]>180) & (box_top[:,:,2]>180)
    mask[80:380, 200:900] = white_top.astype(np.uint8) * 255
    
    box_bot = arr[1250:1440, 180:850]
    yellow_bot = (box_bot[:,:,0]>180) & (box_bot[:,:,1]>130) & (box_bot[:,:,2]<60)
    mask[1250:1440, 180:850] = yellow_bot.astype(np.uint8) * 255
    
    kernel = np.ones((9, 9), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    inpainted = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), dilated, 5, cv2.INPAINT_TELEA)
    clean_im = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
    
    draw = ImageDraw.Draw(clean_im)
    font_main = ImageFont.truetype(FONT_BOLD, 52)
    font_sub = ImageFont.truetype(FONT_BOLD, 44)
    font_bot = ImageFont.truetype(FONT_BOLD, 62)
    
    # EVERY SONG CARRIES
    t1 = "EVERY SONG CARRIES"
    b1 = draw.textbbox((0, 0), t1, font=font_main)
    x1 = (1024 - (b1[2]-b1[0])) // 2
    draw.text((x1+2, 112), t1, font=font_main, fill=(0, 0, 0))
    draw.text((x1, 110), t1, font=font_main, fill=(255, 255, 255))
    
    # A MOVEMENT'S HISTORY!
    t2 = "A MOVEMENT'S HISTORY!"
    b2 = draw.textbbox((0, 0), t2, font=font_sub)
    x2 = (1024 - (b2[2]-b2[0])) // 2
    draw.text((x2+2, 172), t2, font=font_sub, fill=(0, 0, 0))
    draw.text((x2, 170), t2, font=font_sub, fill=(255, 255, 255))
    
    # Arc
    draw.arc([350, 230, 674, 280], start=200, end=340, fill=(245, 179, 1), width=3)
    
    # Bottom name: DAPPU RAMESH
    t3 = "DAPPU RAMESH"
    b3 = draw.textbbox((0, 0), t3, font=font_bot)
    x3 = (1024 - (b3[2]-b3[0])) // 2
    draw.text((x3+3, 1303), t3, font=font_bot, fill=(0, 0, 0))
    draw.text((x3, 1300), t3, font=font_bot, fill=(245, 179, 1))
    
    # Red accent arc below
    draw.arc([300, 1400, 724, 1450], start=20, end=160, fill=(220, 20, 20), width=4)
    
    eng_master_path = os.path.join(ENG_DIR, "podcast_4_English.png")
    clean_im.save(eng_master_path)
    
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "podcast_4.jpg"), quality=90)
    im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_TE, "podcast_4.jpg"), quality=90)
    
    make_banner(clean_im, is_podcast=True).save(os.path.join(BANNERS_EN, "podcast_4_banner.jpg"), quality=90)
    make_banner(im, is_podcast=True).save(os.path.join(BANNERS_TE, "podcast_4_banner.jpg"), quality=90)
    
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "podcast_4_preview.jpg"))
    print("Podcast 4 completed successfully.")

def process_podcast_5():
    print("Processing Podcast 5...")
    src_path = os.path.join(SRC_DIR, "podcast5.png")
    im = Image.open(src_path)
    arr = np.array(im)
    
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box = arr[180:580, 100:950]
    txt = (box[:,:,0]>140) | ((box[:,:,0]<40) & (box[:,:,1]<40) & (box[:,:,2]<40))
    mask[180:580, 100:950] = txt.astype(np.uint8) * 255
    kernel = np.ones((15, 15), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    inpainted = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), dilated, 7, cv2.INPAINT_TELEA)
    clean_im = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
    
    # Soft dark vignette over the top text area to ensure deep contrast
    dark_shade = Image.new("RGBA", (1024, 1536), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(dark_shade)
    s_draw.rectangle([100, 200, 950, 560], fill=(0, 0, 0, 90))
    dark_shade = dark_shade.filter(ImageFilter.GaussianBlur(30))
    clean_im.paste(dark_shade, (0, 0), dark_shade)
    
    draw = ImageDraw.Draw(clean_im)
    font_sub = ImageFont.truetype(FONT_BOLD, 36)
    font_main = ImageFont.truetype(FONT_BOLD, 62)
    
    # UNTIRING STRUGGLE FOR MADIGA RIGHTS
    t1 = "UNTIRING STRUGGLE FOR MADIGA RIGHTS"
    b1 = draw.textbbox((0, 0), t1, font=font_sub)
    x1 = (1024 - (b1[2]-b1[0])) // 2
    draw.text((x1+2, 312), t1, font=font_sub, fill=(0, 0, 0))
    draw.text((x1, 310), t1, font=font_sub, fill=(255, 255, 255))
    
    # MANDA KRISHNA MADIGA
    t2 = "MANDA KRISHNA MADIGA"
    b2 = draw.textbbox((0, 0), t2, font=font_main)
    x2 = (1024 - (b2[2]-b2[0])) // 2
    draw.text((x2+4, 404), t2, font=font_main, fill=(0, 0, 0))
    draw.text((x2, 400), t2, font=font_main, fill=(245, 179, 1))
    
    eng_master_path = os.path.join(ENG_DIR, "podcast_5_English.png")
    clean_im.save(eng_master_path)
    
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "podcast_5.jpg"), quality=90)
    im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_TE, "podcast_5.jpg"), quality=90)
    
    make_banner(clean_im, is_podcast=True).save(os.path.join(BANNERS_EN, "podcast_5_banner.jpg"), quality=90)
    make_banner(im, is_podcast=True).save(os.path.join(BANNERS_TE, "podcast_5_banner.jpg"), quality=90)
    
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "podcast_5_preview.jpg"))
    print("Podcast 5 completed successfully.")

if __name__ == "__main__":
    print("Starting generation of all 5 Songs and 5 Podcasts...")
    process_song_1()
    process_song_2()
    process_song_3()
    process_song_4()
    process_song_5()
    process_podcast_1()
    process_podcast_2()
    process_podcast_3()
    process_podcast_4()
    process_podcast_5()
    print("ALL MEDIA GENERATED SUCCESSFULLY!")
