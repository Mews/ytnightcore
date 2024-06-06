from PIL import Image, ImageDraw, ImageOps
import requests
from io import BytesIO

class Thumbnail:
    def __init__(self, raw_data):
        self.raw_data = raw_data

        self.height = raw_data["height"]
        self.width = raw_data["width"]
        self.url = raw_data["url"]
    
        self.pixel_count = self.height*self.width
    
    def get_image(self, edge_radius=0):
        image_data = requests.get(self.url).content
        image = Image.open(BytesIO(image_data))

        image = image.convert("RGBA")
        
        if not edge_radius == 0:
            mask = Image.new("L", image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle((0,0) + image.size, radius=edge_radius, fill=255)

            image = ImageOps.fit(image, mask.size, centering=(0.5,0.5))
            image.putalpha(mask)

        return image
