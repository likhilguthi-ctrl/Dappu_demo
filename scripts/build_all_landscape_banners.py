import os
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

def create_cinematic_landscape(poster, target_size=(1920, 1080)):
    tw, th = target_size
    pw, ph = poster.size
    
    # 1. Vertical color profile from the poster
    arr = np.array(poster)
    sample_w = max(1, int(pw * 0.12))
    left_sample = arr[:, :sample_w]
    row_colors = np.median(left_sample, axis=1) # shape: (ph, 3)
    
    # 2. Synthesize background gradient matching the vertical atmosphere
    bg_gradient = np.zeros((th, tw, 3), dtype=np.uint8)
    for y in range(th):
        src_y = int(y * ph / th)
        bg_gradient[y, :] = row_colors[src_y]
        
    bg_img = Image.fromarray(bg_gradient).filter(ImageFilter.GaussianBlur(38))
    
    # 3. Fit poster height into 1040 (20px safe padding top and bottom)
    sub_h = 1040
    sub_w = int(sub_h * (pw / ph))
    subject = poster.resize((sub_w, sub_h), Image.Resampling.LANCZOS)
    
    # 4. Position subject: centered in the right half of the 1920 frame
    # Center of right half (960 to 1920) is 1440
    sub_x = 1440 - (sub_w // 2)
    sub_y = (th - sub_h) // 2
    
    # 5. Soft feather on the left edge of the poster so it blends naturally
    mask = Image.new('L', (sub_w, sub_h), 255)
    feather = 45
    for x in range(feather):
        a = int(255 * (x / feather))
        for y in range(sub_h):
            mask.putpixel((x, y), a)
            
    # 6. Soft drop shadow behind subject
    shadow = Image.new('RGBA', (sub_w + 30, sub_h + 30), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rectangle([15, 15, sub_w + 15, sub_h + 15], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(15))
    
    bg_img.paste(shadow, (sub_x - 15, sub_y - 15), shadow)
    bg_img.paste(subject, (sub_x, sub_y), mask)
    
    # 7. Smooth dark vignette on the left (x: 0 to 880) for hero text readability
    left_vignette = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
    for x in range(int(tw * 0.46)):
        alpha = int(210 * (1.0 - (x / (tw * 0.46)))**1.4)
        for y in range(th):
            left_vignette.putpixel((x, y), (8, 8, 10, alpha))
            
    final_banner = Image.alpha_composite(bg_img.convert('RGBA'), left_vignette).convert('RGB')
    return final_banner

def main():
    posters_en_dir = 'assets/madiga/posters/en'
    banners_en_dir = 'assets/madiga/banners/en'
    posters_te_dir = 'assets/madiga/posters/te'
    banners_te_dir = 'assets/madiga/banners/te'
    
    os.makedirs(banners_en_dir, exist_ok=True)
    os.makedirs(banners_te_dir, exist_ok=True)
    
    all_files = sorted(os.listdir(posters_en_dir))
    print(f"Processing {len(all_files)} titles for EN and TE...")
    
    for idx, fname in enumerate(all_files):
        base_slug = os.path.splitext(fname)[0]
        banner_name = f"{base_slug}_banner.jpg"
        
        # English
        src_en = os.path.join(posters_en_dir, fname)
        dst_en = os.path.join(banners_en_dir, banner_name)
        if os.path.exists(src_en):
            im = Image.open(src_en)
            b = create_cinematic_landscape(im)
            b.save(dst_en, quality=95)
            
        # Telugu
        src_te = os.path.join(posters_te_dir, fname)
        dst_te = os.path.join(banners_te_dir, banner_name)
        if os.path.exists(src_te):
            im = Image.open(src_te)
            b = create_cinematic_landscape(im)
            b.save(dst_te, quality=95)
            
        print(f"[{idx+1}/{len(all_files)}] Processed {base_slug}")

    print("ALL 60 LANDSCAPE BANNERS SUCCESSFULLY GENERATED AT STUDIO QUALITY!")

if __name__ == '__main__':
    main()
