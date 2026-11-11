import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC_DIR = "MADIGA -20261109T093322Z-1-001/MADIGA"
PREVIEW_DIR = r"C:\Users\likhi\.gemini\antigravity\brain\1d1ca0ff-6359-45f4-ae60-10ce4ab7893a\final_media_previews"

FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_IMPACT = "C:/Windows/Fonts/impact.ttf"
FONT_SERIF = "C:/Windows/Fonts/georgiab.ttf"
FONT_SEGOE = "C:/Windows/Fonts/segoeuib.ttf"

# 1. Clean Song 5
def clean_song_5():
    im = Image.open(os.path.join(SRC_DIR, "song5.jpeg"))
    arr = np.array(im)
    
    # Inpaint mask for y: 2750..3550, x: 350..3900
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
    
    # Smooth red glow over y: 2850..3450 to remove any micro-texture
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
    
    clean.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "clean_song_5.jpg"))
    print("clean_song_5 saved")

# 2. Clean Song 4
def clean_song_4():
    im = Image.open(os.path.join(SRC_DIR, "Song4.jpeg"))
    arr = np.array(im)
    
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)
    box = arr[350:2050, 250:3750]
    # Any text pixel in this box
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
    
    # Smooth warm dark golden vignette
    vig = Image.new("RGBA", (4000, 6000), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vig)
    v_draw.ellipse([400, 450, 3600, 1950], fill=(45, 32, 5, 220))
    vig = vig.filter(ImageFilter.GaussianBlur(70))
    clean.paste(vig, (0, 0), vig)
    
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
    
    clean.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "clean_song_4.jpg"))
    print("clean_song_4 saved")

# 3. Clean Podcast 5
def clean_podcast_5():
    im = Image.open(os.path.join(SRC_DIR, "podcast5.png"))
    arr = np.array(im)
    
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
    
    clean.resize((600, 900), Image.Resampling.LANCZOS).save(os.path.join(PREVIEW_DIR, "clean_podcast_5.jpg"))
    print("clean_podcast_5 saved")

clean_song_5()
clean_song_4()
clean_podcast_5()
