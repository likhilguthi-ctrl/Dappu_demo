import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def make_banner(poster_img):
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

def draw_centered_text(draw, y, text, font, fill, w, shadow_offset=(3, 3), shadow_fill=(0, 0, 0, 230), stroke_w=0, stroke_fill=None):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (w - tw) // 2
    if shadow_offset:
        draw.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=shadow_fill)
    if stroke_w > 0 and stroke_fill:
        for dx in range(-stroke_w, stroke_w + 1):
            for dy in range(-stroke_w, stroke_w + 1):
                if dx*dx + dy*dy <= stroke_w*stroke_w:
                    draw.text((x + dx, y + dy), text, font=font, fill=stroke_fill)
    draw.text((x, y), text, font=font, fill=fill)
    return x, y, tw, th

def generate_education_assets():
    print("Generating Education 1 (Gogu Shyamala)...")
    src1_path = r"MADIGA -20261109T093322Z-1-001\MADIGA\Education.png"
    img1 = cv2.imread(src1_path)
    h1, w1, _ = img1.shape
    
    # Inpaint text
    roi1 = img1[960:1385, 45:975]
    b = roi1[:, :, 0].astype(float)
    g = roi1[:, :, 1].astype(float)
    r = roi1[:, :, 2].astype(float)
    
    is_yellow = (r > 150) & (g > 110) & (b < 90)
    is_white = (r > 150) & (g > 150) & (b > 150)
    is_red = (r > 130) & (g < 45) & (b < 45)
    is_dark = (r < 25) & (g < 15) & (b < 15)
    
    text_mask1 = (is_yellow | is_white | is_red | is_dark).astype(np.uint8) * 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    dilated1 = cv2.dilate(text_mask1, kernel, iterations=2)
    
    mask1 = np.zeros((h1, w1), dtype=np.uint8)
    mask1[960:1385, 45:975] = dilated1
    inp1 = cv2.inpaint(img1, mask1, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
    
    # Synthesize clean vertical gradient for banner
    banner_y1, banner_y2 = 970, 1375
    banner_x1, banner_x2 = 50, 974
    grad_v = np.zeros((banner_y2 - banner_y1, 3), dtype=np.float32)
    for i in range(banner_y2 - banner_y1):
        frac = i / float(banner_y2 - banner_y1)
        r_val = 68.0 - 15.0 * np.sin(np.pi * frac)
        g_val = 14.0 - 4.0 * np.sin(np.pi * frac)
        b_val = 10.0 - 2.0 * np.sin(np.pi * frac)
        grad_v[i] = [b_val, g_val, r_val]
        
    plate1 = np.zeros((banner_y2 - banner_y1, banner_x2 - banner_x1, 3), dtype=np.float32)
    for i in range(banner_y2 - banner_y1):
        plate1[i, :] = grad_v[i]
    np.random.seed(42)
    plate1 += np.random.normal(0, 2.5, plate1.shape)
    plate1 = np.clip(plate1, 0, 255)
    
    alpha1 = np.ones((banner_y2 - banner_y1, banner_x2 - banner_x1), dtype=np.float32)
    fade1 = 25
    for i in range(fade1):
        alpha1[i, :] *= (i / float(fade1))
        alpha1[-(i+1), :] *= (i / float(fade1))
        alpha1[:, i] *= (i / float(fade1))
        alpha1[:, -(i+1)] *= (i / float(fade1))
        
    clean_area1 = inp1[banner_y1:banner_y2, banner_x1:banner_x2].astype(float)
    inp1[banner_y1:banner_y2, banner_x1:banner_x2] = np.clip(clean_area1 * (1.0 - alpha1[:, :, None]) + plate1 * alpha1[:, :, None], 0, 255).astype(np.uint8)
    
    # Render typography
    pil1 = Image.fromarray(cv2.cvtColor(inp1, cv2.COLOR_BGR2RGB))
    draw1 = ImageDraw.Draw(pil1)
    
    font1_l1 = ImageFont.truetype('C:/Windows/Fonts/segoeprb.ttf', 44)
    font1_l2 = ImageFont.truetype('C:/Windows/Fonts/impact.ttf', 104)
    font1_l3 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 72)
    
    draw_centered_text(draw1, 990, 'The Voice of Madiga Women...', font1_l1, fill=(255, 255, 255), w=w1, shadow_offset=(3, 3), shadow_fill=(15, 0, 0))
    x2, y2_pos, tw2, th2 = draw_centered_text(draw1, 1075, 'GOGU SHYAMALA', font1_l2, fill=(255, 215, 0), w=w1, shadow_offset=(5, 5), shadow_fill=(15, 0, 0), stroke_w=2, stroke_fill=(50, 5, 5))
    
    # Red brush line
    line_y = 1215
    line_x1 = (w1 - tw2) // 2 + 15
    line_x2 = line_x1 + tw2 - 30
    for offset_y in range(-3, 4):
        factor = 1.0 - abs(offset_y) / 4.0
        r_val = int(225 * factor)
        draw1.line([(line_x1, line_y + offset_y), (line_x2, line_y + offset_y)], fill=(r_val, 15, 15), width=1)
        
    draw_centered_text(draw1, 1255, 'THE STRUGGLE', font1_l3, fill=(255, 255, 255), w=w1, shadow_offset=(4, 4), shadow_fill=(15, 0, 0))
    
    # -----------------
    # 2. EDU 2: Prof. Endluri Sudhakar
    # -----------------
    print("Generating Education 2 (Prof. Endluri Sudhakar)...")
    src2_path = r"MADIGA -20261109T093322Z-1-001\Education2.png"
    img2 = cv2.imread(src2_path)
    h2, w2, _ = img2.shape
    
    roi2 = img2[940:1390, 40:984]
    b = roi2[:, :, 0].astype(float)
    g = roi2[:, :, 1].astype(float)
    r = roi2[:, :, 2].astype(float)
    
    is_text2 = (b > 120) & (g > 120) & (r > 120)
    is_text2 |= (r > 140) & (g > 110) & (b < 100)
    is_text2 |= (r < 18) & (g < 18) & (b < 25)
    
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    mask_roi2 = cv2.dilate(is_text2.astype(np.uint8) * 255, kernel2, iterations=2)
    mask2 = np.zeros((h2, w2), dtype=np.uint8)
    mask2[940:1390, 40:984] = mask_roi2
    
    inp2 = cv2.inpaint(img2, mask2, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
    
    # Smooth dark vignette
    y_start = 880
    y_end = 1450
    v_alpha2 = np.zeros((h2, w2), dtype=np.float32)
    for y in range(y_start, y_end):
        if y < 980:
            val = 0.5 * (1.0 - np.cos(np.pi * (y - y_start) / (980.0 - y_start)))
        elif y > 1390:
            val = 1.0 - 0.2 * ((y - 1390) / 60.0)
        else:
            val = 1.0
        v_alpha2[y, :] = val
    v_alpha2 = cv2.GaussianBlur(v_alpha2, (61, 61), 0)
    
    dark_col2 = np.array([20, 20, 22], dtype=np.float32)
    plate2 = np.zeros((h2, w2, 3), dtype=np.float32)
    plate2[:] = dark_col2
    np.random.seed(42)
    plate2 += np.random.normal(0, 1.8, plate2.shape)
    
    clean2 = inp2.astype(float) * (1.0 - v_alpha2[:, :, None]) + plate2 * v_alpha2[:, :, None]
    clean2 = np.clip(clean2, 0, 255).astype(np.uint8)
    
    pil2 = Image.fromarray(cv2.cvtColor(clean2, cv2.COLOR_BGR2RGB))
    draw2 = ImageDraw.Draw(pil2)
    
    font2_l1 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 54)
    font2_l2 = ImageFont.truetype('C:/Windows/Fonts/impact.ttf', 92)
    font2_l3 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 62)
    
    draw_centered_text(draw2, 970, 'A NEW VOICE FOR', font2_l1, fill=(255, 255, 255), w=w2, shadow_offset=(4, 4), shadow_fill=(0, 0, 0))
    draw_centered_text(draw2, 1070, 'DALIT LITERATURE!', font2_l2, fill=(255, 215, 0), w=w2, shadow_offset=(5, 5), shadow_fill=(0, 0, 0), stroke_w=2, stroke_fill=(15, 15, 15))
    draw_centered_text(draw2, 1220, 'PROF. ENDLURI SUDHAKAR', font2_l3, fill=(255, 255, 255), w=w2, shadow_offset=(4, 4), shadow_fill=(0, 0, 0))
    
    # -----------------
    # Save High-Resolution English Masters
    # -----------------
    eng_dir = r"ENG-20261110T042858Z-1-001\ENG"
    os.makedirs(eng_dir, exist_ok=True)
    
    pil1.save(os.path.join(eng_dir, "Education_1_English.png"))
    pil1.save(os.path.join(eng_dir, "Education_1_English.jpg"), quality=98)
    pil1.save(os.path.join(eng_dir, "Education_English.png"))
    
    pil2.save(os.path.join(eng_dir, "Education_2_English.png"))
    pil2.save(os.path.join(eng_dir, "Education_2_English.jpg"), quality=98)
    print("Saved high-res masters to", eng_dir)
    
    # -----------------
    # Generate Web Posters (800x1200) & Banners (1920x1080)
    # -----------------
    posters_en_dir = r"assets\madiga\posters\en"
    posters_te_dir = r"assets\madiga\posters\te"
    banners_en_dir = r"assets\madiga\banners\en"
    banners_te_dir = r"assets\madiga\banners\te"
    
    for d in [posters_en_dir, posters_te_dir, banners_en_dir, banners_te_dir]:
        os.makedirs(d, exist_ok=True)
        
    pw, ph = 800, 1200
    
    # English Web Posters
    p1_en = pil1.resize((pw, ph), Image.Resampling.LANCZOS)
    p1_en.save(os.path.join(posters_en_dir, "education_1.jpg"), quality=94)
    
    p2_en = pil2.resize((pw, ph), Image.Resampling.LANCZOS)
    p2_en.save(os.path.join(posters_en_dir, "education_2.jpg"), quality=94)
    
    # Telugu Web Posters (Originals resized)
    raw1_te = Image.open(src1_path)
    p1_te = raw1_te.resize((pw, ph), Image.Resampling.LANCZOS)
    p1_te.convert("RGB").save(os.path.join(posters_te_dir, "education_1.jpg"), quality=94)
    
    raw2_te = Image.open(src2_path)
    p2_te = raw2_te.resize((pw, ph), Image.Resampling.LANCZOS)
    p2_te.convert("RGB").save(os.path.join(posters_te_dir, "education_2.jpg"), quality=94)
    
    print("Saved web posters.")
    
    # English Banners (1920x1080)
    b1_en = make_banner(pil1)
    b1_en.save(os.path.join(banners_en_dir, "education_1_banner.jpg"), quality=92)
    
    b2_en = make_banner(pil2)
    b2_en.save(os.path.join(banners_en_dir, "education_2_banner.jpg"), quality=92)
    
    # Telugu Banners (1920x1080)
    b1_te = make_banner(raw1_te.convert("RGB"))
    b1_te.save(os.path.join(banners_te_dir, "education_1_banner.jpg"), quality=92)
    
    b2_te = make_banner(raw2_te.convert("RGB"))
    b2_te.save(os.path.join(banners_te_dir, "education_2_banner.jpg"), quality=92)
    
    print("Saved widescreen banners.")

if __name__ == "__main__":
    generate_education_assets()
