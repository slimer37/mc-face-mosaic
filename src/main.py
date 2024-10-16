import api
from PIL import Image

with open("names.txt") as f:
    usernames = [l.strip() for l in f.readlines() if not l.startswith("#") and l.strip() != '']

face_size = 8
minimum_size = 512

# Whether to only save after done
in_rush = True

# side length of empty middle region
empty_center_side = 0

output_directory = "output"

placeholder_face_img = Image.open("src/placeholder/missing-face.png")

def printerr(text):
    print(f"\033[31m{text}\033[0m")

def grab_face(username):
    uuid = api.to_uuid(username)

    if uuid is None:
        printerr(f"Couldn't find UUID for {username}.")
        return placeholder_face_img
    
    return api.get_face(uuid, face_size, overlay = True)

if __name__ == "__main__":
    player_count = len(usernames)
    space_count = player_count + empty_center_side * empty_center_side

    # Find minimum square to fit
    i = 0
    while i * i < space_count:
        i += 1
    
    width = i
    dimension = width * face_size

    mosaic = Image.new("RGBA", (dimension, dimension))

    print("Created", dimension, "x", dimension, f'({width} wide)', "image for", player_count, "faces")
    print("There will be", width * width - space_count, "blank spaces.", f"(Optimally {width * width - empty_center_side * empty_center_side} faces)")

    x = 0
    y = 0
    
    empty_start = (width - empty_center_side) // 2 - 1
    empty_end = (width + empty_center_side) // 2

    for username in usernames:
        
        while empty_start < x < empty_end and empty_start < y < empty_end:
            print((x, y), "skipped")
            
            x += 1
        
            if x >= width:
                y += 1
                x = 0
            
        face_img = grab_face(username)

        if face_img:
            print("Placing", username, "at", (x, y))
        else:
            printerr(f"@ {(x, y)}: Failed to find {username}'s face.")

        mosaic.paste(face_img, (x * face_size, y * face_size))
        
        if not in_rush:
            mosaic.save(f"{output_directory}/mosaic.png")

        x += 1
        
        if x >= width:
            y += 1
            x = 0

    while dimension < minimum_size:
        dimension *= 2

    new_size = (dimension, dimension)
    
    mosaic.save(f"{output_directory}/mosaic.png")

    print("Resizing to", new_size)

    mosaic = mosaic.resize(new_size, Image.Resampling.NEAREST)

    mosaic.save(f"{output_directory}/mosaic@{dimension}x.png")

    print("Done!")