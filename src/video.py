from thumbnail import Thumbnail
from PIL import ImageDraw, ImageFont

class Video:
    def __init__(self, raw_data):
        self.raw_data = raw_data

        self.url = raw_data["link"]
        self.id = raw_data["id"]

        self.title = raw_data["title"]

        self.author = raw_data["channel"]["name"]
        
        #Get highest resolution author pfp
        self.author_pfp = None
        author_pfps = raw_data["channel"]["thumbnails"]
        max_author_pfp_res = -1

        for author_pfp_data in author_pfps:
            c_pfp = Thumbnail(author_pfp_data)

            if c_pfp.pixel_count > max_author_pfp_res:
                max_author_pfp_res = c_pfp.pixel_count
                self.author_pfp = c_pfp
        
        self.duration = raw_data["duration"]

        #Get highest resolution thumbnail
        self.thumbnail = None
        thumbnails = raw_data["thumbnails"]
        max_thumbnail_res = -1

        for thumbnail_data in thumbnails:
            c_thumbnail = Thumbnail(thumbnail_data)

            if c_thumbnail.pixel_count > max_thumbnail_res:
                max_thumbnail_res = c_thumbnail.pixel_count
                self.thumbnail = c_thumbnail

        self.views = raw_data["viewCount"]["short"]

        self.thumbnail_image = None
    
    def get_thumbnail_image(self, edge_radius=0):
        image_width = 282
        image_height = 159

        corner_radius = 5

        text = self.duration

        image = self.thumbnail.get_image(edge_radius=edge_radius).resize((image_width, image_height))

        # Draw duration at bottom right corner
        draw = ImageDraw.Draw(image)

        font = ImageFont.load_default()

        # Calculate text size
        text_bbox = draw.textbbox((0,0), text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height  = text_bbox[3] - text_bbox[1]

        # Calculate rectangle height (some padding for the text)
        padding = 7
        rect_height = text_height + 2 * padding

        # Draw the rounded rectangle at the bottom right corner
        image_width, image_height = image.size
        rect_position = (image_width - text_width - padding, image_height - rect_height, image_width, image_height)
        draw.rounded_rectangle(rect_position, fill="black", radius=corner_radius)

        # Calculate text position
        text_x = image_width - text_width - padding / 2
        text_y = image_height - rect_height + padding / 2

        # Draw the text on top of the rectangle
        draw.text((text_x, text_y), text, font=font, fill="white")

        self.thumbnail_image = image
        return image