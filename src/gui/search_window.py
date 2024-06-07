from video import Video
from gui.get_color import get_color
from gui.set_cursor import set_cursor
from gui.bind_children import bind_children
from gui.wraplabel import WrapLabel
import youtube
from log import log

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from tkfontawesome import icon_to_image

from PIL import ImageTk
from concurrent.futures import ThreadPoolExecutor
from threading import Thread


class SearchWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.search_bar = SearchBar(master=self, bootstyle=DEFAULT)
        self.search_bar.pack(side=TOP, fill=X, expand=False, padx=20, pady=(15,10))

        self.search_results_frame = SearchResults(master=self, bootstyle=SECONDARY)
        self.search_results_frame.pack(side=TOP, fill=BOTH, expand=True, padx=20, pady=(15,25))


    def search(self):
        set_cursor(self, "watch") # Set cursor to spinning wheel

        query = self.search_bar.get_query()

        log("Search", "Searching using query: "+query)

        results = youtube.search(query, limit=10)

        # Display search results
        self.search_results_frame.update_video_frames(videos=results)

        log("Search", "Retrieved results")

        set_cursor(self, "") # Set cursor to default



class SearchBar(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query_entry = QueryEntry(master=self, bootstyle=SECONDARY, placeholder="Search for a song...")
        self.query_entry.pack(side=LEFT, fill=BOTH, expand=True, padx=(0,10))

        # Needs to keep reference to the image
        self.ico_search = icon_to_image("search", fill=get_color("light"), scale_to_height=16)

        self.search_button = ttk.Button(master=self, bootstyle=PRIMARY+LINK, image=self.ico_search, command=self.master.search)
        self.search_button.pack(side=LEFT, fill=BOTH, expand=False)

    def get_query(self):
        return self.query_entry.get()



class QueryEntry(ttk.Entry):
    def __init__(self, placeholder, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.placeholder = placeholder

        self.bind("<FocusIn>", self.focus_in)
        self.bind("<FocusOut>", self.focus_out)

        self.put_placeholder()
    
    def put_placeholder(self):
        self.insert(0, self.placeholder)
    
    def focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, END)

    def focus_out(self, event):
        if not self.get():
            self.put_placeholder()



class SearchResults(ScrolledFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.container.config(bootstyle=kwargs["bootstyle"])

        self.video_frames = []

        self.container.bind("<Enter>", self.bind_mouse_wheel)
        self.container.bind("<Leave>", self.unbind_mouse_wheel)
        self.container.bind_all("<MouseWheel>", self.on_mouse_wheel)
    
    def bind_mouse_wheel(self, event):
        self.bind_all("<MouseWheel>", self.on_mouse_wheel)
        
    def unbind_mouse_wheel(self, event):
        self.unbind_all("<MouseWheel>")

    def on_mouse_wheel(self, event):
        # Use custom scroll height
        scroll_height = 4

        if event.delta > 0:
            self.yview_scroll(-scroll_height, "units")
        
        else:
            self.yview_scroll(scroll_height, "units")


    def update_video_frames(self, videos):
        # Delete all previous video frames
        for video_frame in self.video_frames:
            video_frame.destroy()
        self.video_frames.clear()

        # Get the thumbnail image for every video
        log("Search", "Fetching video thumbnails")
        with ThreadPoolExecutor() as thread_pool:
            for video in videos:
                thread_pool.submit(lambda video: video.get_thumbnail_image(edge_radius=15), video)

        for video in videos:
            video_frame = VideoFrame(master=self, video=video, bootstyle=DEFAULT)

            self.video_frames.append(video_frame)

            video_frame.pack(side=TOP, fill=X, expand=True, padx=10, pady=5)


class VideoFrame(ttk.Frame):
    def __init__(self, video:Video, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.args = args
        self.kwargs = kwargs

        self.video = video
        self.widgets = []

        if self.video.thumbnail_image == None:
            self.video.get_thumbnail_image()

        self.grid_columnconfigure(1, weight=1)

        self.download_progress_bar = ttk.Progressbar(master=self)

        self.thumb = ImageTk.PhotoImage(self.video.thumbnail_image)
        self.thumb_panel = ttk.Label(master=self, image=self.thumb)
        self.thumb_panel.grid(row=1, column=0, rowspan=3, padx=5, pady=5)

        self.title_label = WrapLabel(master=self, text=self.video.title, font=("", 13), bootstyle=DEFAULT)
        self.title_label.grid(row=1, column=1, sticky=W+S)

        self.views_label = WrapLabel(master=self, text=self.video.author + " ⋅ " + self.video.views, font=("", 10), bootstyle=DEFAULT)
        self.views_label.grid(row=2, column=1, sticky=W+N)

        self.desc_label = WrapLabel(master=self, text=self.video.description, font=("", 10), bootstyle=DEFAULT)
        self.desc_label.grid(row=3, column=1, sticky=W+N)

        bind_children(self, "<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_hover_on)
        self.bind("<Leave>", self.on_hover_off)

    
    def progress_hook(self, info):
        # https://github.com/yt-dlp/yt-dlp/blob/db50f19d76c6870a5a13d0cab9287d684fd7449a/yt_dlp/YoutubeDL.py#L364

        status = info["status"]

        if status == "downloading":
            self.download_progress_bar.config(mode=DETERMINATE, bootstyle=SUCCESS)
            # Stop auto increasing in case it previously failed to calculate progress
            self.download_progress_bar.stop()

            downloaded_bytes = info["downloaded_bytes"]
            total_bytes = info["total_bytes"]

            if total_bytes == None:
                total_bytes = info["total_bytes_estimate"]

                if total_bytes == None:
                    # If cant determite total size, set progress bar to indeterminate

                    self.download_progress_bar.config(mode=INDETERMINATE)
                    self.download_progress_bar.start()
                    return

            progress = (downloaded_bytes / total_bytes) * 100

            self.download_progress_bar.config(value=progress)
        
        if status == "finished":
            self.download_progress_bar.config(mode=DETERMINATE, bootstyle=SUCCESS)
            # Stop auto increasing in case it previously failed to calculate progress
            self.download_progress_bar.stop()

            self.download_progress_bar.config(value=100)
        
        if status == "error":
            self.download_progress_bar.config(mode=DETERMINATE, bootstyle=DANGER)
            # Stop auto increasing in case it previously failed to calculate progress
            self.download_progress_bar.stop()



    def on_hover_on(self, event):
        for widget in self.winfo_children():
            if not isinstance(widget, ttk.Progressbar):
                widget.config(bootstyle=LIGHT+INVERSE)

        self.config(bootstyle=LIGHT)
    
    def on_hover_off(self, event):
        for widget in self.winfo_children():
            if not isinstance(widget, ttk.Progressbar):
                widget.config(bootstyle=self.kwargs["bootstyle"])

        self.config(bootstyle=self.kwargs["bootstyle"])

    def on_click(self, event):
        self.download_progress_bar.grid(row=0, column=0, columnspan=2, padx=5, sticky=W+E, pady=(5,0))

        Thread(target=lambda:[log("Download", "Downloading "+self.video.title + ":"),
                              youtube.download_yt_mp3(self.video.url, "temp/song", progress_hook=self.progress_hook),
                              self.download_progress_bar.grid_forget(),
                              log("Download", "Finished downloading "+self.video.title)]).start()