from PIL import Image
import random
import numpy as np

def add_noise(img: Image.Image, color):
    row, col = img.size
    
    img = np.copy(np.array(img))

    # 50%
    number_of_pixels = row * col // 2
    
    for i in range(number_of_pixels):
        
        y_coord = random.randint(0, row - 1)

        x_coord = random.randint(0, col - 1)

        img[y_coord][x_coord] = color

    return Image.fromarray(img)

def create_vignette(w, h):
    # Create solid red image
    im = Image.new(mode='RGBA', size=(w, h))

    # Create radial alpha/transparency layer. 255 in centre, 0 at edge
    dark = 100
    Y = np.linspace(-1, 1, h)[None, :] * dark
    X = np.linspace(-1, 1, w)[:, None] * dark
    alpha = np.sqrt(X**2 + Y**2)
    alpha = np.clip(0,255,alpha)

    # Push that radial gradient transparency onto red image and save
    im.putalpha(Image.fromarray(alpha.astype(np.uint8)))
    
    return im

if __name__ == "__main__":
    bg_color = (36, 9, 4)
    
    bg = Image.new("RGB", (96, 96), bg_color)
    
    vignette = create_vignette(96, 96)
    
    bg_color2 = (69, 3, 3)
    
    bg = add_noise(bg, bg_color2)
    
    mosaic = Image.open("mosaic@768x.png")
    bg = bg.resize(mosaic.size, Image.Resampling.NEAREST)
    
    heart = Image.open("heart.png").resize(mosaic.size, Image.Resampling.NEAREST)
    mosaic.paste(heart, (0, 0), heart)
    
    bg.paste(mosaic, (0, 0), mosaic)
    
    vignette = vignette.resize(mosaic.size, Image.Resampling.NEAREST)
    
    bg.paste(vignette, (0, 0), vignette)
    
    bg.save("overlaid.png")
