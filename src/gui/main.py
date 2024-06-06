from gui.search_window import SearchWindow
from gui.log_window import LogWindow
from gui.player_window import PlayerWindow

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

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

        self.add(self.search_window, text="Search")
        self.add(self.player_window, text="Player")
        self.add(self.log_window, text="Logs")