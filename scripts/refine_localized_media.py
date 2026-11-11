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

# ----------------- REFINED SONG 1 -----------------
def refine_song_1():
    print("Refining Song 1 with ultra-smooth sunset sky...")
    src_path = os.path.join(SRC_DIR, "Song1.jpeg")
    im = Image.open(src_path)
    arr = np.array(im)
    
    # Smooth horizontal gradient for y: 500..2600
    # Sample undisturbed left x: 80..180 and right x: 3820..3920
    clean_arr = arr.copy()
    left_sample = arr[500:2650, 100:150, :].mean(axis=1) # (2150, 3)
    right_sample = arr[500:2650, 3850:3900, :].mean(axis=1) # (2150, 3)
    
    # Interpolate horizontally across 4000 columns
    t = np.linspace(0, 1, 4000).reshape(1, 4000, 1)
    sky_patch = (left_sample.reshape(-1, 1, 3) * (1 - t) + right_sample.reshape(-1, 1, 3) * t).astype(np.uint8)
    
    # Singer hair starts at x: 200..1200, y > 2450
    # Blend sky patch with feathering
    patch_img = Image.fromarray(sky_patch)
    # Mask with feathered edges
    mask = Image.new("L", (4000, 2150), 255)
    m_draw = ImageDraw.Draw(mask)
    # top feather
    for y in range(80):
        m_draw.line([(0, y), (4000, y)], fill=int(255 * (y / 80)))
    # bottom feather avoiding singer head
    for y in range(2150 - 150, 2150):
        ratio = (2150 - y) / 150.0
        m_draw.line([(0, y), (4000, y)], fill=int(255 * ratio))
    # Cut out singer's head area on bottom-left
    m_draw.ellipse([0, 1800, 1250, 2500], fill=0)
    mask = mask.filter(ImageFilter.GaussianBlur(30))
    
    clean_im = Image.fromarray(arr)
    clean_im.paste(patch_img, (0, 500), mask)
    
    # Typography
    draw = ImageDraw.Draw(clean_im)
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
    
    clean_im.save(os.path.join(ENG_DIR, "Song_1_English.jpg"), quality=95)
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "song_1.jpg"), quality=90)
    make_banner(clean_im).save(os.path.join(BANNERS_EN, "song_1_banner.jpg"), quality=90)
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "song_1_preview.jpg"))
    print("Song 1 refined perfectly.")

# ----------------- REFINED SONG 2 -----------------
def refine_song_2():
    print("Refining Song 2 removing bottom fragments...")
    src_path = os.path.join(SRC_DIR, "Song2.jpeg")
    im = Image.open(src_path)
    arr = np.array(im)
    
    # Build clean red gradient
    clean_top = np.zeros((3400, 4000, 3), dtype=np.uint8)
    left = arr[:3400, 150:151, :].astype(float)
    right = arr[:3400, 3850:3851, :].astype(float)
    base_col = (left + right) / 2.0
    x = np.arange(4000)
    dist = np.abs(x - 2000) / 2000.0
    factor = (1.0 + 0.08 * (1.0 - dist**2)).reshape(1, 4000, 1)
    clean_top = np.clip(base_col * factor, 0, 255).astype(np.uint8)
    
    arr_clean = arr.copy()
    # Replace background outside the white circle ring
    for y in range(3400):
        for xi in range(4000):
            if y < 3180:
                arr_clean[y, xi] = clean_top[y, xi]
            elif (xi - 2000)**2 + (y - 4445)**2 >= (1255)**2:
                arr_clean[y, xi] = clean_top[min(y, 3399), xi]
                
    clean_im = Image.fromarray(arr_clean)
    draw = ImageDraw.Draw(clean_im)
    
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
    
    clean_im.save(os.path.join(ENG_DIR, "Song_2_English.jpg"), quality=95)
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "song_2.jpg"), quality=90)
    make_banner(clean_im).save(os.path.join(BANNERS_EN, "song_2_banner.jpg"), quality=90)
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "song_2_preview.jpg"))
    print("Song 2 refined perfectly.")

# ----------------- REFINED SONG 3 -----------------
def refine_song_3():
    print("Refining Song 3 removing remaining spots...")
    src_path = os.path.join(SRC_DIR, "Song3.jpeg")
    im = Image.open(src_path)
    arr = np.array(im)
    
    # Inpaint mask covering text + bottom dots
    mask = np.zeros((6000, 4000), dtype=np.uint8)
    box = arr[3000:4900, 250:3500]
    blue_mask = (box[:,:,2].astype(int) - box[:,:,0].astype(int) > 15) & (box[:,:,2] > 40)
    dark_line = (box[1200:1900, :] < 70).all(axis=-1)
    blue_mask[1200:1900, :] |= dark_line
    mask[3000:4900, 250:3500] = blue_mask.astype(np.uint8) * 255
    # Explicitly mask the 3 dots near y: 4600..4850
    mask[4500:4850, 400:3000] = (arr[4500:4850, 400:3000] < 80).all(axis=-1).astype(np.uint8) * 255
    kernel = np.ones((30, 30), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    small_img = cv2.resize(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), (2000, 3000))
    small_mask = cv2.resize(dilated, (2000, 3000))
    inpainted = cv2.inpaint(small_img, small_mask, 7, cv2.INPAINT_TELEA)
    clean_im = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB)).resize((4000, 6000), Image.Resampling.LANCZOS)
    
    # Subtle soft mist cloud
    cloud = Image.new("RGBA", (4000, 6000), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(cloud)
    c_draw.ellipse([300, 3100, 3700, 4700], fill=(255, 255, 255, 170))
    cloud = cloud.filter(ImageFilter.GaussianBlur(80))
    clean_im.paste(cloud, (0, 0), cloud)
    
    draw = ImageDraw.Draw(clean_im)
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
    
    clean_im.save(os.path.join(ENG_DIR, "Song_3_English.jpg"), quality=95)
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "song_3.jpg"), quality=90)
    make_banner(clean_im).save(os.path.join(BANNERS_EN, "song_3_banner.jpg"), quality=90)
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "song_3_preview.jpg"))
    print("Song 3 refined perfectly.")

# ----------------- REFINED SONG 4 -----------------
def refine_song_4():
    print("Refining Song 4 with seamless golden spotlight background...")
    src_path = os.path.join(SRC_DIR, "Song4.jpeg")
    im = Image.open(src_path)
    arr = np.array(im)
    
    # Smooth spotlight in y: 400..1800
    # Clean warm dark backdrop
    spotlight = Image.new("RGBA", (4000, 6000), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(spotlight)
    # Dark brown-amber radial gradient
    s_draw.rectangle([200, 400, 3800, 1800], fill=(28, 18, 5, 230))
    s_draw.ellipse([1000, 300, 3000, 1900], fill=(70, 45, 10, 200))
    spotlight = spotlight.filter(ImageFilter.GaussianBlur(90))
    
    clean_im = Image.fromarray(arr)
    clean_im.paste(spotlight, (0, 0), spotlight)
    
    draw = ImageDraw.Draw(clean_im)
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
    
    clean_im.save(os.path.join(ENG_DIR, "Song_4_English.jpg"), quality=95)
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "song_4.jpg"), quality=90)
    make_banner(clean_im).save(os.path.join(BANNERS_EN, "song_4_banner.jpg"), quality=90)
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "song_4_preview.jpg"))
    print("Song 4 refined perfectly.")

# ----------------- REFINED SONG 5 -----------------
def refine_song_5():
    print("Refining Song 5 with smooth crimson glow...")
    src_path = os.path.join(SRC_DIR, "song5.jpeg")
    im = Image.open(src_path)
    arr = np.array(im)
    
    glow = Image.new("RGBA", (4000, 6000), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.rectangle([200, 2750, 3800, 3550], fill=(160, 5, 15, 240))
    g_draw.ellipse([800, 2700, 3200, 3600], fill=(210, 20, 25, 230))
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    
    clean_im = Image.fromarray(arr)
    clean_im.paste(glow, (0, 0), glow)
    
    draw = ImageDraw.Draw(clean_im)
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
    
    clean_im.save(os.path.join(ENG_DIR, "Song_5_English.jpg"), quality=95)
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "song_5.jpg"), quality=90)
    make_banner(clean_im).save(os.path.join(BANNERS_EN, "song_5_banner.jpg"), quality=90)
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "song_5_preview.jpg"))
    print("Song 5 refined perfectly.")

# ----------------- REFINED PODCAST 4 -----------------
def refine_podcast_4():
    print("Refining Podcast 4 removing bottom residual text...")
    src_path = os.path.join(SRC_DIR, "podcast4.png")
    im = Image.open(src_path)
    arr = np.array(im)
    
    # Top text inpaint
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box_top = arr[80:380, 200:900]
    white_top = (box_top[:,:,0]>180) & (box_top[:,:,1]>180) & (box_top[:,:,2]>180)
    mask[80:380, 200:900] = white_top.astype(np.uint8) * 255
    kernel = np.ones((9, 9), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=1)
    
    inpainted = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), dilated, 5, cv2.INPAINT_TELEA)
    clean_im = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))
    
    # Clean bottom table wood texture for y: 1240..1380
    wood = Image.new("RGBA", (1024, 1536), (0, 0, 0, 0))
    w_draw = ImageDraw.Draw(wood)
    # Sample table color around y=1220: rich dark walnut
    w_draw.rectangle([150, 1260, 874, 1370], fill=(22, 12, 8, 235))
    wood = wood.filter(ImageFilter.GaussianBlur(18))
    clean_im.paste(wood, (0, 0), wood)
    
    draw = ImageDraw.Draw(clean_im)
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
    
    clean_im.save(os.path.join(ENG_DIR, "podcast_4_English.png"))
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "podcast_4.jpg"), quality=90)
    make_banner(clean_im, is_podcast=True).save(os.path.join(BANNERS_EN, "podcast_4_banner.jpg"), quality=90)
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "podcast_4_preview.jpg"))
    print("Podcast 4 refined perfectly.")

# ----------------- REFINED PODCAST 5 -----------------
def refine_podcast_5():
    print("Refining Podcast 5 with pristine studio card backing...")
    src_path = os.path.join(SRC_DIR, "podcast5.png")
    im = Image.open(src_path)
    
    # Sleek dark cinematic atmospheric backing for the text region
    card = Image.new("RGBA", (1024, 1536), (0, 0, 0, 0))
    c_draw = ImageDraw.Draw(card)
    c_draw.rounded_rectangle([100, 240, 924, 490], radius=24, fill=(18, 12, 10, 225))
    card = card.filter(ImageFilter.GaussianBlur(15))
    
    clean_im = im.convert("RGBA")
    clean_im.paste(card, (0, 0), card)
    clean_im = clean_im.convert("RGB")
    
    draw = ImageDraw.Draw(clean_im)
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
    
    clean_im.save(os.path.join(ENG_DIR, "podcast_5_English.png"))
    clean_im.resize((800, 1200), Image.Resampling.LANCZOS).save(os.path.join(POSTERS_EN, "podcast_5.jpg"), quality=90)
    make_banner(clean_im, is_podcast=True).save(os.path.join(BANNERS_EN, "podcast_5_banner.jpg"), quality=90)
    clean_im.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "podcast_5_preview.jpg"))
    print("Podcast 5 refined perfectly.")

if __name__ == "__main__":
    refine_song_1()
    refine_song_2()
    refine_song_3()
    refine_song_4()
    refine_song_5()
    refine_podcast_4()
    refine_podcast_5()
    print("ALL REFINED ASSETS GENERATED!")
