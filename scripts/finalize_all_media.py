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

for d in [ENG_DIR, POSTERS_EN, POSTERS_TE, BANNERS_EN, BANNERS_TE]:
    os.makedirs(d, exist_ok=True)

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_IMPACT = "C:/Windows/Fonts/impact.ttf"
FONT_SERIF = "C:/Windows/Fonts/georgiab.ttf"
FONT_SEGOE = "C:/Windows/Fonts/segoeuib.ttf"

def make_banner(poster_img, is_podcast=False):
    bw, bh = 1920, 1080
    banner = Image.new("RGB", (bw, bh), (0, 0, 0))
    bg = poster_img.resize((bw, int(bw * poster_img.height / poster_img.width)), Image.Resampling.LANCZOS)
    crop_top = max(0, (bg.height - bh) // 2)
    bg = bg.crop((0, crop_top, bw, crop_top + bh))
    bg = bg.filter(ImageFilter.GaussianBlur(35))
    
    dark_overlay = Image.new("RGBA", (bw, bh), (0, 0, 0, 175))
    bg = Image.alpha_composite(bg.convert("RGBA"), dark_overlay)
    
    grad_mask = Image.new("L", (bw, bh), 0)
    for x in range(bw):
        alpha = int(255 * max(0, min(1, (1.0 - (x / (bw * 0.75))))))
        grad_mask.paste(alpha, (x, 0, x + 1, bh))
    black_cover = Image.new("RGBA", (bw, bh), (0, 0, 0, 255))
    bg.paste(black_cover, (0, 0), grad_mask)
    banner.paste(bg.convert("RGB"), (0, 0))
    
    subject_h = int(bh * 0.94)
    subject_w = int(subject_h * (poster_img.width / poster_img.height))
    subject = poster_img.resize((subject_w, subject_h), Image.Resampling.LANCZOS)
    
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

def save_media(clean_en, raw_te, name_base, is_podcast=False):
    ext = ".png" if is_podcast else ".jpg"
    eng_master = os.path.join(ENG_DIR, f"{name_base}_English{ext}")
    if ext == ".png":
        clean_en.save(eng_master)
    else:
        clean_en.save(eng_master, quality=95)
        
    slug = name_base.lower()
    clean_en.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, f"{slug}.jpg"), quality=90)
    raw_te.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_TE, f"{slug}.jpg"), quality=90)
    
    make_banner(clean_en, is_podcast).save(os.path.join(BANNERS_EN, f"{slug}_banner.jpg"), quality=90)
    make_banner(raw_te, is_podcast).save(os.path.join(BANNERS_TE, f"{slug}_banner.jpg"), quality=90)
    print(f"Saved all formats for {slug}")

# ================= 1. SONG 1 =================
def build_song_1():
    src = Image.open(os.path.join(SRC_DIR, "Song1.jpeg"))
    arr = np.array(src)
    
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box = arr[700:2800, 300:3850]
    txt = ((box[:,:,0]>180) & (box[:,:,1]>180) & (box[:,:,2]>180)) | \
          ((box[:,:,0]>150) & (box[:,:,1]<70) & (box[:,:,2]<70))
    mask[700:2800, 300:3850] = txt.astype(np.uint8) * 255
    kernel = np.ones((35, 35), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    small_img = cv2.resize(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), (1000, 1500))
    small_mask = cv2.resize(dilated, (1000, 1500))
    inpainted = cv2.inpaint(small_img, small_mask, 5, cv2.INPAINT_TELEA)
    clean = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)).resize((4000, 6000), Image.Resampling.LANCZOS)
    
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
    
    save_media(clean, src, "song_1")

# ================= 2. SONG 2 =================
def build_song_2():
    src = Image.open(os.path.join(SRC_DIR, "Song2.jpeg"))
    arr = np.array(src)
    
    clean_arr = arr.copy()
    left = arr[:3400, 150:151, :].astype(float)
    right = arr[:3400, 3850:3851, :].astype(float)
    base_col = (left + right) / 2.0
    x = np.arange(4000)
    dist = np.abs(x - 2000) / 2000.0
    factor = (1.0 + 0.08 * (1.0 - dist**2)).reshape(1, 4000, 1)
    clean_top = np.clip(base_col * factor, 0, 255).astype(np.uint8)
    
    for y in range(3350):
        for xi in range(4000):
            if y < 3180:
                clean_arr[y, xi] = clean_top[y, xi]
            elif (xi - 2000)**2 + (y - 4445)**2 >= (1255)**2:
                clean_arr[y, xi] = clean_top[min(y, 3349), xi]
                
    clean = Image.fromarray(clean_arr)
    draw = ImageDraw.Draw(clean)
    
    font_sub = ImageFont.truetype(FONT_SEGOE, 150)
    font_main = ImageFont.truetype(FONT_IMPACT, 340)
    font_line2 = ImageFont.truetype(FONT_IMPACT, 260)
    font_tag = ImageFont.truetype(FONT_BOLD, 120)
    
    t1 = "O ARUNA PATHAKAMA"
    b1 = draw.textbbox((0, 0), t1, font=font_sub)
    draw.text(((4000 - (b1[2]-b1[0]))//2, 850), t1, font=font_sub, fill=(245, 179, 1))
    
    t2 = "RED SALUTES"
    b2 = draw.textbbox((0, 0), t2, font=font_main)
    x2 = (4000 - (b2[2]-b2[0]))//2
    draw.text((x2+8, 1208), t2, font=font_main, fill=(0, 0, 0), stroke_width=14, stroke_fill=(0, 0, 0))
    draw.text((x2, 1200), t2, font=font_main, fill=(255, 255, 255), stroke_width=6, stroke_fill=(40, 0, 0))
    
    t3 = "TO THE RED FLAG"
    b3 = draw.textbbox((0, 0), t3, font=font_line2)
    x3 = (4000 - (b3[2]-b3[0]))//2
    draw.text((x3+8, 1658), t3, font=font_line2, fill=(0, 0, 0), stroke_width=12, stroke_fill=(0, 0, 0))
    draw.text((x3, 1650), t3, font=font_line2, fill=(255, 255, 255))
    
    t4 = "REVOLUTIONARY FOLK ANTHEM"
    b4 = draw.textbbox((0, 0), t4, font=font_tag)
    draw.text(((4000 - (b4[2]-b4[0]))//2, 2100), t4, font=font_tag, fill=(245, 179, 1))
    
    save_media(clean, src, "song_2")

# ================= 3. SONG 3 =================
def build_song_3():
    src = Image.open(os.path.join(SRC_DIR, "Song3.jpeg"))
    arr = np.array(src)
    
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box = arr[3000:4950, 250:3500]
    blue_mask = (box[:,:,2].astype(int) - box[:,:,0].astype(int) > 15) & (box[:,:,2] > 40)
    dark_line = (box[1200:1900, :] < 80).all(axis=-1)
    blue_mask[1200:1900, :] |= dark_line
    mask[3000:4950, 250:3500] = blue_mask.astype(np.uint8) * 255
    mask[4500:4880, 400:3000] = (arr[4500:4880, 400:3000] < 80).all(axis=-1).astype(np.uint8) * 255
    kernel = np.ones((35, 35), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    small_img = cv2.resize(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), (1000, 1500))
    small_mask = cv2.resize(dilated, (1000, 1500))
    inpainted = cv2.inpaint(small_img, small_mask, 5, cv2.INPAINT_TELEA)
    clean = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)).resize((4000, 6000), Image.Resampling.LANCZOS)
    
    cloud = Image.new("RGBA", (4000, 6000), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(cloud)
    c_draw.ellipse([300, 3100, 3700, 4700], fill=(255, 255, 255, 170))
    cloud = cloud.filter(ImageFilter.GaussianBlur(80))
    clean.paste(cloud, (0, 0), cloud)
    
    draw = ImageDraw.Draw(clean)
    font_main = ImageFont.truetype(FONT_SERIF, 280)
    font_sub = ImageFont.truetype(FONT_SEGOE, 220)
    font_desc = ImageFont.truetype(FONT_BOLD, 120)
    
    t1 = "MADIGA DANDORA"
    b1 = draw.textbbox((0, 0), t1, font=font_main)
    draw.text(((4000 - (b1[2]-b1[0]))//2, 3250), t1, font=font_main, fill=(15, 32, 67))
    
    t2 = "CULTURAL TROUPE"
    b2 = draw.textbbox((0, 0), t2, font=font_sub)
    draw.text(((4000 - (b2[2]-b2[0]))//2, 3620), t2, font=font_sub, fill=(20, 45, 95))
    
    draw.line([900, 3960, 3100, 3960], fill=(15, 32, 67), width=8)
    
    t3 = "DAPPU • DARUVU • BEATS OF RESISTANCE"
    b3 = draw.textbbox((0, 0), t3, font=font_desc)
    draw.text(((4000 - (b3[2]-b3[0]))//2, 4030), t3, font=font_desc, fill=(15, 32, 67))
    
    save_media(clean, src, "song_3")

# ================= 4. SONG 4 =================
def build_song_4():
    im = Image.open(os.path.join(SRC_DIR, "Song4.jpeg"))
    arr = np.array(im)
    
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box = arr[350:2050, 250:3750]
    txt = ((box[:,:,0]>140) & (box[:,:,1]>120) & (box[:,:,2]<90)) | \
          ((box[:,:,0]<50) & (box[:,:,1]>40) & (box[:,:,2]<60)) | \
          ((box[:,:,0]<40) & (box[:,:,1]<40) & (box[:,:,2]<40))
    mask[350:2050, 250:3750] = txt.astype(np.uint8) * 255
    kernel = np.ones((35, 35), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    small_img = cv2.resize(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), (1000, 1500))
    small_mask = cv2.resize(dilated, (1000, 1500))
    inpainted = cv2.inpaint(small_img, small_mask, 5, cv2.INPAINT_TELEA)
    clean = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)).resize((4000, 6000), Image.Resampling.LANCZOS)
    
    vig = Image.new("RGBA", (4000, 6000), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vig)
    v_draw.ellipse([400, 450, 3600, 1950], fill=(45, 32, 5, 220))
    vig = vig.filter(ImageFilter.GaussianBlur(70))
    clean.paste(vig, (0, 0), vig)
    
    draw = ImageDraw.Draw(clean)
    font_main = ImageFont.truetype(FONT_IMPACT, 320)
    font_sub = ImageFont.truetype(FONT_IMPACT, 260)
    font_eyebrow = ImageFont.truetype(FONT_BOLD, 130)
    
    t0 = "RHYTHM OF TELANGANA"
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
    
    save_media(clean, im, "song_4")

# ================= 5. SONG 5 =================
def build_song_5():
    im = Image.open(os.path.join(SRC_DIR, "song5.jpeg"))
    arr = np.array(im)
    
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box = arr[2750:3550, 350:3900]
    txt = (box[:,:,0]>140) & (box[:,:,1]>120) & (box[:,:,2]<80)
    dark = (box[:,:,0]<50) & (box[:,:,1]<50) & (box[:,:,2]<50)
    mask[2750:3550, 350:3900] = (txt | dark).astype(np.uint8) * 255
    kernel = np.ones((25, 25), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    small_img = cv2.resize(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), (1000, 1500))
    small_mask = cv2.resize(dilated, (1000, 1500))
    inpainted = cv2.inpaint(small_img, small_mask, 5, cv2.INPAINT_TELEA)
    clean = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)).resize((4000, 6000), Image.Resampling.LANCZOS)
    
    glow = Image.new("RGBA", (4000, 6000), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.ellipse([400, 2800, 3600, 3450], fill=(160, 5, 15, 255))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    clean.paste(glow, (0, 0), glow)
    
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
    
    save_media(clean, im, "song_5")

# ================= 6. PODCAST 1 =================
def build_podcast_1():
    src = Image.open(os.path.join(SRC_DIR, "podcast1.png"))
    arr = np.array(src)
    
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box = arr[140:420, 70:950]
    white_text = (box[:,:,0]>200) & (box[:,:,1]>200) & (box[:,:,2]>200)
    yellow_text = (box[:,:,0]>180) & (box[:,:,1]>130) & (box[:,:,2]<50)
    mask[140:420, 70:950] = (white_text | yellow_text).astype(np.uint8) * 255
    kernel = np.ones((9, 9), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    inpainted = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), dilated, 5, cv2.INPAINT_TELEA)
    clean = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
    
    draw = ImageDraw.Draw(clean)
    font_top = ImageFont.truetype(FONT_SERIF, 48)
    font_name = ImageFont.truetype(FONT_BOLD, 54)
    
    t1 = "1994 – THE GENESIS OF MRPS!"
    b1 = draw.textbbox((0, 0), t1, font=font_top)
    x1 = (1024 - (b1[2]-b1[0])) // 2
    draw.text((x1+2, 172), t1, font=font_top, fill=(0, 0, 0))
    draw.text((x1, 170), t1, font=font_top, fill=(255, 255, 255))
    
    t2 = "DANDU VEERAYYA MADIGA"
    b2 = draw.textbbox((0, 0), t2, font=font_name)
    x2 = (1024 - (b2[2]-b2[0])) // 2
    draw.text((x2+2, 242), t2, font=font_name, fill=(0, 0, 0))
    draw.text((x2, 240), t2, font=font_name, fill=(245, 179, 1))
    
    draw.arc([300, 320, 724, 380], start=200, end=340, fill=(245, 179, 1), width=3)
    save_media(clean, src, "podcast_1", is_podcast=True)

# ================= 7. PODCAST 2 =================
def build_podcast_2():
    src = Image.open(os.path.join(SRC_DIR, "podcast2.png"))
    arr = np.array(src)
    
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
    clean = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
    
    draw = ImageDraw.Draw(clean)
    font_main = ImageFont.truetype(FONT_BOLD, 54)
    font_sub = ImageFont.truetype(FONT_BOLD, 48)
    font_badge = ImageFont.truetype(FONT_BOLD, 38)
    
    t1 = "MADIGA CORPORATION"
    b1 = draw.textbbox((0, 0), t1, font=font_main)
    x1 = (1024 - (b1[2]-b1[0])) // 2
    draw.text((x1+2, 142), t1, font=font_main, fill=(0, 0, 0))
    draw.text((x1, 140), t1, font=font_main, fill=(245, 179, 1))
    
    t2 = "THE UNTOLD STORY!"
    b2 = draw.textbbox((0, 0), t2, font=font_sub)
    x2 = (1024 - (b2[2]-b2[0])) // 2
    draw.text((x2+2, 212), t2, font=font_sub, fill=(0, 0, 0))
    draw.text((x2, 210), t2, font=font_sub, fill=(255, 255, 255))
    
    draw.arc([300, 275, 724, 335], start=200, end=340, fill=(245, 179, 1), width=3)
    
    t3 = "KOMMURI KANAKARAO MADIGA"
    b3 = draw.textbbox((0, 0), t3, font=font_badge)
    x3 = (1024 - (b3[2]-b3[0])) // 2
    draw.text((x3, 1395), t3, font=font_badge, fill=(255, 255, 255))
    
    save_media(clean, src, "podcast_2", is_podcast=True)

# ================= 8. PODCAST 3 =================
def build_podcast_3():
    src = Image.open(os.path.join(SRC_DIR, "podcast3.png"))
    arr = np.array(src)
    
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box_top = arr[110:520, 100:950]
    white_top = (box_top[:,:,0]>200) & (box_top[:,:,1]>200) & (box_top[:,:,2]>200)
    yellow_top = (box_top[:,:,0]>180) & (box_top[:,:,1]>130) & (box_top[:,:,2]<60)
    mask[110:520, 100:950] = (yellow_top | white_top).astype(np.uint8) * 255
    kernel = np.ones((9, 9), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    inpainted = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), dilated, 5, cv2.INPAINT_TELEA)
    clean = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
    
    draw = ImageDraw.Draw(clean)
    font_main = ImageFont.truetype(FONT_SERIF, 50)
    font_sub = ImageFont.truetype(FONT_BOLD, 46)
    font_name = ImageFont.truetype(FONT_BOLD, 44)
    
    t1 = "1994: THE EMERGENCE OF MRPS"
    b1 = draw.textbbox((0, 0), t1, font=font_main)
    x1 = (1024 - (b1[2]-b1[0])) // 2
    draw.text((x1+2, 142), t1, font=font_main, fill=(0, 0, 0))
    draw.text((x1, 140), t1, font=font_main, fill=(255, 255, 255))
    
    t2 = "HOW THE MOVEMENT BEGAN?"
    b2 = draw.textbbox((0, 0), t2, font=font_sub)
    x2 = (1024 - (b2[2]-b2[0])) // 2
    draw.text((x2+2, 212), t2, font=font_sub, fill=(0, 0, 0))
    draw.text((x2, 210), t2, font=font_sub, fill=(245, 179, 1))
    
    t3 = "KRUPAKAR MADIGA"
    b3 = draw.textbbox((0, 0), t3, font=font_name)
    x3 = (1024 - (b3[2]-b3[0])) // 2
    draw.text((x3+2, 282), t3, font=font_name, fill=(0, 0, 0))
    draw.text((x3, 280), t3, font=font_name, fill=(255, 255, 255))
    
    draw.line([x3, 335, x3 + (b3[2]-b3[0]), 335], fill=(245, 179, 1), width=3)
    save_media(clean, src, "podcast_3", is_podcast=True)

# ================= 9. PODCAST 4 =================
def build_podcast_4():
    src = Image.open(os.path.join(SRC_DIR, "podcast4.png"))
    clean = src.copy()
    
    # 1. Clean top text using inpaint
    arr = np.array(clean)
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box_top = arr[80:350, 200:900]
    white_top = (box_top[:,:,0]>180) & (box_top[:,:,1]>180) & (box_top[:,:,2]>180)
    mask[80:350, 200:900] = white_top.astype(np.uint8) * 255
    kernel = np.ones((11, 11), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    inpainted = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), dilated, 5, cv2.INPAINT_TELEA)
    clean = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
    
    # 2. Clean table text at bottom: replace y: 1250..1430 with table wood plate
    table_sample = clean.crop((100, 1190, 924, 1240)).resize((824, 180), Image.Resampling.LANCZOS)
    mask_bot = Image.new("L", (824, 180), 255)
    mb_draw = ImageDraw.Draw(mask_bot)
    for i in range(25):
        alpha = int(255 * (i / 25.0))
        mb_draw.rectangle([i, i, 824 - i, 180 - i], outline=alpha)
    mask_bot = mask_bot.filter(ImageFilter.GaussianBlur(12))
    clean.paste(table_sample, (100, 1250), mask_bot)
    
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
    save_media(clean, src, "podcast_4", is_podcast=True)

# ================= 10. PODCAST 5 =================
def build_podcast_5():
    src = Image.open(os.path.join(SRC_DIR, "podcast5.png"))
    arr = np.array(src)
    
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box = arr[100:580, 70:960]
    txt = ((box[:,:,0]>140) & (box[:,:,1]>110)) | \
          ((box[:,:,0]<45) & (box[:,:,1]<45) & (box[:,:,2]<45))
    mask[100:580, 70:960] = txt.astype(np.uint8) * 255
    kernel = np.ones((11, 11), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    inpainted = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), dilated, 5, cv2.INPAINT_TELEA)
    clean = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
    
    # Sleek dark backing plate behind name
    plate = Image.new("RGBA", (1024, 1536), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(plate)
    p_draw.rounded_rectangle([80, 260, 944, 490], radius=30, fill=(15, 10, 8, 240))
    plate = plate.filter(ImageFilter.GaussianBlur(12))
    clean.paste(plate, (0, 0), plate)
    
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
    
    save_media(clean, src, "podcast_5", is_podcast=True)

if __name__ == "__main__":
    print("Building and saving all 10 finalized media assets...")
    build_song_1()
    build_song_2()
    build_song_3()
    build_song_4()
    build_song_5()
    build_podcast_1()
    build_podcast_2()
    build_podcast_3()
    build_podcast_4()
    build_podcast_5()
    print("ALL 10 MEDIA ASSETS SAVED TO ENG AND ASSETS DIRECTORIES!")
