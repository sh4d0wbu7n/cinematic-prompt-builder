from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
BASE_IMAGE = ASSETS / "camera_arri.jpg"
SIZE = (1024, 572)


def fit_base() -> Image.Image:
    img = Image.open(BASE_IMAGE).convert("RGB")
    return ImageOps.fit(img, SIZE, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def enhance(img, color=1.0, contrast=1.0, brightness=1.0, sharpness=1.0):
    img = ImageEnhance.Color(img).enhance(color)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    return img


def colorize(img, shadows=(0, 0, 0), highlights=(255, 255, 255), strength=0.35):
    gray = ImageOps.grayscale(img)
    mapped = ImageOps.colorize(gray, black=shadows, white=highlights).convert("RGB")
    return Image.blend(img, mapped, strength)


def overlay_color(img, color, alpha=0.2, mode="normal"):
    layer = Image.new("RGB", img.size, color)
    if mode == "multiply":
        mixed = Image.blend(img, ImageChops.multiply(img, layer), alpha)
    elif mode == "screen":
        mixed = Image.blend(img, ImageChops.screen(img, layer), alpha)
    else:
        mixed = Image.blend(img, layer, alpha)
    return mixed


def lift_blacks(img, amount=24):
    lut = [min(255, int(v * (255 - amount) / 255 + amount)) for v in range(256)]
    return img.point(lut * 3)


def crush_blacks(img, amount=16):
    lut = [0 if v < amount else min(255, int((v - amount) * 255 / (255 - amount))) for v in range(256)]
    return img.point(lut * 3)


def vignette(img, strength=0.45):
    w, h = img.size
    mask = Image.new("L", img.size, 0)
    px = mask.load()
    cx, cy = w / 2, h / 2
    max_d = (cx * cx + cy * cy) ** 0.5
    for y in range(h):
        for x in range(w):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / max_d
            px[x, y] = int(255 * min(1, max(0, (d - 0.2) / 0.8)) * strength)
    dark = Image.new("RGB", img.size, (0, 0, 0))
    return Image.composite(dark, img, mask)


def warm_highlights(img, color=(255, 170, 92), strength=0.28, threshold=165):
    gray = ImageOps.grayscale(img)
    mask = gray.point(lambda v: max(0, min(255, (v - threshold) * 4)))
    warm = Image.new("RGB", img.size, color)
    toned = Image.blend(img, warm, strength)
    return Image.composite(toned, img, mask)


def grade_kodak2383(base):
    img = enhance(base, color=1.16, contrast=1.22, brightness=1.02, sharpness=1.04)
    img = colorize(img, shadows=(16, 28, 38), highlights=(255, 226, 176), strength=0.18)
    return warm_highlights(img, strength=0.16)


def grade_bleach(base):
    img = enhance(base, color=0.32, contrast=1.55, brightness=0.96, sharpness=1.15)
    img = colorize(img, shadows=(28, 31, 34), highlights=(228, 224, 210), strength=0.24)
    return crush_blacks(img, 10)


def grade_daynight(base):
    img = enhance(base, color=0.58, contrast=1.08, brightness=0.48)
    img = colorize(img, shadows=(5, 15, 42), highlights=(88, 130, 182), strength=0.62)
    return vignette(img, 0.55)


def grade_rec709(base):
    return enhance(base, color=1.03, contrast=1.04, brightness=1.02, sharpness=1.05)


def grade_log(base):
    img = enhance(base, color=0.66, contrast=0.58, brightness=1.12, sharpness=0.88)
    return lift_blacks(img, 34)


def grade_aces(base):
    img = enhance(base, color=1.12, contrast=1.2, brightness=1.0)
    img = colorize(img, shadows=(8, 28, 45), highlights=(255, 232, 204), strength=0.2)
    return warm_highlights(img, strength=0.2)


def grade_cross(base):
    img = enhance(base, color=1.32, contrast=1.3, brightness=1.0, sharpness=1.08)
    img = colorize(img, shadows=(0, 74, 65), highlights=(255, 180, 228), strength=0.42)
    return crush_blacks(img, 8)


def grade_halation(base):
    img = enhance(base, color=1.08, contrast=1.08, brightness=1.02)
    gray = ImageOps.grayscale(img)
    mask = gray.point(lambda v: 255 if v > 178 else 0).filter(ImageFilter.GaussianBlur(10))
    glow = Image.new("RGB", img.size, (255, 92, 42))
    glow_img = Image.composite(glow, Image.new("RGB", img.size, (0, 0, 0)), mask)
    img = Image.blend(img, ImageChops.screen(img, glow_img), 0.35)
    return warm_highlights(img, strength=0.18)


def grade_lowkey(base):
    img = enhance(base, color=0.9, contrast=1.34, brightness=0.58, sharpness=1.03)
    img = colorize(img, shadows=(4, 8, 13), highlights=(198, 184, 154), strength=0.22)
    return vignette(crush_blacks(img, 18), 0.7)


def grade_highkey(base):
    img = enhance(base, color=0.82, contrast=0.68, brightness=1.38, sharpness=0.88)
    img = lift_blacks(img, 46)
    img = colorize(img, shadows=(198, 208, 214), highlights=(255, 246, 232), strength=0.18)
    return img.filter(ImageFilter.GaussianBlur(0.25))


def main():
    base = fit_base()
    graders = {
        "kodak2383": grade_kodak2383,
        "bleach": grade_bleach,
        "daynight": grade_daynight,
        "rec709": grade_rec709,
        "log": grade_log,
        "aces": grade_aces,
        "cross": grade_cross,
        "halation": grade_halation,
        "lowkey": grade_lowkey,
        "highkey": grade_highkey,
    }
    created = []
    for key, fn in graders.items():
        out = ASSETS / f"grading_{key}.jpg"
        if out.exists():
            continue
        fn(base).save(out, "JPEG", quality=88, optimize=True)
        created.append(out.name)
    print("created " + ", ".join(created) if created else "all grading previews already exist")


if __name__ == "__main__":
    from PIL import ImageChops

    main()
