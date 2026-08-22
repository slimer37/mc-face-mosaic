import api
import os

from PIL import Image
from argparse import ArgumentParser

face_size = 8

placeholder_face_img = Image.open("src/placeholder/missing-face.png")

def print_error(text):
    print(f"\033[31m{text}\033[0m")

def grab_face(username):
    uuid = api.to_uuid(username)

    if uuid is None:
        print_error(f"Couldn't find UUID for {username}.")
        return placeholder_face_img
    
    return api.get_face(uuid, face_size, overlay=True)

def main():
    argparser = ArgumentParser()
    
    argparser.add_argument("--min-size", "-s", help="Minimum size to use when resizing the output mosaic", default=512, type=int)
    argparser.add_argument("--live", "-l", action="store_true", help="Whether to save the image to mosaic.png as each face is added")
    argparser.add_argument("--empty-center-size", "-e", help="The size of a center square to leave empty for an image to be added later", default=0, type=int)
    argparser.add_argument("--out", "-o", help="The output directory", default="output", type=str)
    argparser.add_argument("namefile", help="The file containing the list of names to use.", type=str)
    
    args = argparser.parse_args()
    
    if os.path.exists(args.namefile) and not os.path.isdir(args.namefile):
        with open(args.namefile) as f:
            usernames = [l.strip() for l in f.readlines() if not l.startswith("#") and l.strip() != '']
    else:
        print_error(f"File {args.namefile} does not exist or is a directory.")
        return

    minimum_size = args.min_size
    is_live = args.live
    empty_center_side = args.empty_center_size
    output_directory = args.out
    
    player_count = len(usernames)
    space_count = player_count + empty_center_side * empty_center_side

    # Find minimum square
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
            print_error(f"@ {(x, y)}: Failed to find {username}'s face.")

        mosaic.paste(face_img, (x * face_size, y * face_size))
        
        if is_live:
            mosaic.save(f"{output_directory}/mosaic.png")

        x += 1
        
        if x >= width:
            y += 1
            x = 0

    while dimension < minimum_size:
        dimension *= 2

    new_size = (dimension, dimension)

    os.makedirs(output_directory, exist_ok=True)
    
    mosaic.save(f"{output_directory}/mosaic.png")

    print("Resizing to", new_size)

    mosaic = mosaic.resize(new_size, Image.Resampling.NEAREST)

    mosaic.save(f"{output_directory}/mosaic@{dimension}x.png")

    print("Done!")
    
if __name__ == "__main__":
    main()