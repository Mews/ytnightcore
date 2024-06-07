from thumbnail import Thumbnail
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
        img = self.thumbnail.get_image(edge_radius=edge_radius)

        self.thumbnail_image = img
        return img