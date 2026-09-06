"""Deterministic social layouts using existing imagery; no invented product pictures."""
import hashlib
import json
import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
from .content import clip, local_image


def font_path():
    choices = [os.environ.get("SOCIAL_FONT", ""),
               "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]
    for choice in choices:
        if choice and Path(choice).is_file():
            return choice
    raise ValueError("日本語フォントが必要です。SOCIAL_FONTにNoto Sans CJKのパスを設定してください")


def lines(draw, text, font, width):
    result, current = [], ""
    for char in text:
        if current and draw.textlength(current + char, font=font) > width:
            result.append(current)
            current = char
        else:
            current += char
    return result + ([current] if current else [])


def card(source, title, description, size, brand, ai_image=False):
    w, h = size
    canvas = Image.new("RGB", size, "#081f2b")
    photo_h = int(h * .49)
    # Contain, not crop: retain the entire product or travel photograph.
    photo = ImageOps.contain(source, (w - 80, photo_h - 24))
    canvas.paste(photo, ((w - photo.width) // 2, 28 + (photo_h - photo.height) // 2))
    draw = ImageDraw.Draw(canvas)
    font = font_path()
    draw.line((48, photo_h + 44, w - 48, photo_h + 44), fill="#51d3cd", width=5)
    y = photo_h + 78
    brand_font = ImageFont.truetype(font, 30)
    draw.text((54, y), brand, font=brand_font, fill="#7eddd5")
    y += 58
    title_font = ImageFont.truetype(font, 48)
    title_lines = lines(draw, title, title_font, w - 108)
    while len(title_lines) > 4 and title_font.size > 32:
        title_font = ImageFont.truetype(font, title_font.size - 2)
        title_lines = lines(draw, title, title_font, w - 108)
    for i, line in enumerate(title_lines[:4]):
        if i == 3 and len(title_lines) > 4:
            line = line[:-1] + "…"
        draw.text((54, y), line, font=title_font, fill="white")
        y += title_font.size + 12
    y += 18
    body_font = ImageFont.truetype(font, 30)
    available = max(0, (h - 175 - y) // 44)
    wrapped = lines(draw, description, body_font, w - 108)
    for i, line in enumerate(wrapped[:available]):
        if i == available - 1 and len(wrapped) > available:
            line = clip(line, max(1, len(line) - 1)) + "…"
        draw.text((54, y), line, font=body_font, fill="#d2e2e8")
        y += 44
    draw.text((54, h - 120), "続きはブログで  www.axis-jp.net", font=brand_font, fill="#7eddd5")
    if ai_image:
        draw.text((54, h - 72), "※画像は生成イメージです", font=ImageFont.truetype(font, 24), fill="#d2e2e8")
    return canvas


def render(root, article, out, config):
    image = local_image(root, Path(article["path"]), article["image_ref"], config["site_url"])
    source_bytes = image.read_bytes()
    digest = hashlib.sha256(source_bytes + json.dumps(article, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
    folder = out / "assets" / "social" / article["id"]
    folder.mkdir(parents=True, exist_ok=True)
    with Image.open(image) as opened:
        source = ImageOps.exif_transpose(opened).convert("RGB")
    for name, size in (("instagram.jpg", (1080, 1350)), ("pinterest.jpg", (1000, 1500)), ("video-cover.jpg", (1080, 1920))):
        card(source, article["title"], article["description"], size, config["site_name"], article["ai_image"]).save(folder / name, quality=91)
    # A 12-second vertical slideshow, not a claim of original video footage.
    second = card(source, "記事で詳しく紹介しています", article["description"], (1080, 1920), config["site_name"], article["ai_image"])
    second.save(folder / "video-end.jpg", quality=91)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-loop", "1", "-framerate", "25", "-t", "6", "-i", str(folder / "video-cover.jpg"),
                    "-loop", "1", "-framerate", "25", "-t", "6", "-i", str(folder / "video-end.jpg"),
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                    "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
                    "-map", "[v]", "-map", "2:a", "-t", "12", "-c:v", "libx264", "-preset", "fast",
                    "-threads", "2", "-crf", "23", "-c:a", "aac", "-movflags", "+faststart",
                    str(folder / "tiktok.mp4")], check=True, timeout=180)
    base = config["site_url"].rstrip("/") + "/assets/social/" + article["id"]
    return {**article, "image_url": base + "/instagram.jpg", "pin_url": base + "/pinterest.jpg",
            "video_url": base + "/tiktok.mp4", "media_hash": digest}
