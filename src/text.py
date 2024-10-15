from PIL import Image, ImageFont, ImageDraw
import PIL.ImageOps

def write_text(img : Image.Image, text, size = 30, intensity = 1.0):
    mask = Image.new("L", img.size)
    
    font = ImageFont.truetype("fonts/MinecraftTen.ttf", size)

    draw = ImageDraw.Draw(mask)

    _, _, w, h = draw.textbbox((0, 0), text, font=font)

    draw.text(((img.width - w) / 2, (img.height - h) / 2), text, font = font, align = "center", fill = int(intensity * 255))

    img.paste(PIL.ImageOps.invert(img), mask = mask)

if __name__ == "__main__":
    mosaic = Image.open("mosaic.png")
    mosaic = mosaic.resize((512, 512), Image.Resampling.NEAREST)
    # write_text(mosaic, "Realmers", 100, 0.75)
    mosaic.save("mosaic@512x.png")