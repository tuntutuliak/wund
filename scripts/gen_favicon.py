from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _pick_font() -> str | None:
    candidates = [
        "C:/Windows/Fonts/seguisb.ttf",  # Segoe UI Semibold
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return p
    return None


def main() -> None:
    out_dir = Path(__file__).resolve().parent.parent / "static" / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "favicon.ico"

    sizes = [16, 32, 48, 64, 128, 256]
    font_path = _pick_font()

    images: list[Image.Image] = []
    for s in sizes:
        img = Image.new("RGBA", (s, s), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)

        font_size = int(s * 0.78)
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()

        text = "W"
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (s - tw) // 2 - bbox[0]
        y = (s - th) // 2 - bbox[1]

        # Green #16A34A
        draw.text((x, y), text, font=font, fill=(22, 163, 74, 255))
        images.append(img)

    images[0].save(out_path, format="ICO", sizes=[(s, s) for s in sizes])
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()

