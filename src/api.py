import requests
from PIL import Image

def to_uuid(username : str):
    res = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")

    if res.status_code != 200:
        return None
    
    return res.json()["id"]

def get_face(uuid : str, size = 8, overlay = False) -> Image.Image:
    # Retrieve face from crafatar
    url = f"https://crafatar.com/avatars/{uuid}?size={size}"

    if overlay: url += "&overlay"
    
    img_data = requests.get(url, stream=True).raw
    
    return Image.open(img_data)