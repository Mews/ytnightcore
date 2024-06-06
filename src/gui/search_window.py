from video import Video

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame

class SearchWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.query_entry = QueryEntry(master=self, bootstyle=SECONDARY, placeholder="Search for a song...")
        self.query_entry.pack(side=TOP, fill=X, expand=False, padx=20, pady=15)



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



class VideoFrame(ttk.Frame):
    def __init__(self, video:Video, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.video = video