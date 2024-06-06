from gui.search_window import SearchWindow
from gui.log_window import LogWindow
from gui.player_window import PlayerWindow
from gui.get_color import get_color

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkfontawesome import icon_to_image

class RootWindow(ttk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mainui = MainUi(master=self, padding=0, bootstyle=DEFAULT)
        self.mainui.pack(expand=True, fill=BOTH)



class MainUi(ttk.Notebook):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.search_window = SearchWindow(master=self)
        self.search_window.pack(expand=True, fill=BOTH)

        self.player_window = PlayerWindow(master=self)
        self.player_window.pack(expand=True, fill=BOTH)

        self.log_window = LogWindow(master=self)
        self.log_window.pack(expand=True, fill=BOTH)

        #Needs to keep reference to images
        self.ico_yt = icon_to_image("youtube", fill="red", scale_to_width=16)
        self.ico_vol = icon_to_image("headphones", fill=get_color("light"), scale_to_width=16)
        self.ico_log = icon_to_image("scroll", fill=get_color("light"), scale_to_width=16)

        self.add(self.search_window, text=" Search", image=self.ico_yt, compound=LEFT)
        self.add(self.player_window, text=" Player", image=self.ico_vol, compound=LEFT)
        self.add(self.log_window, text=" Logs", image=self.ico_log, compound=LEFT)