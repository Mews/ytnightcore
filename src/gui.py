import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from consoleio import ConsoleIO
import sys

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
        

class SearchWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class PlayerWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LogWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text = ttk.ScrolledText(master=self, state=DISABLED)
        self.text.pack(expand=True, fill=BOTH)

        self.console_io = ConsoleIO(callback=self.update_text)
        #Redirect print statements to log window's console io
        sys.stdout = self.console_io

    def update_text(self):
        self.text.config(state=NORMAL)

        self.text.delete("1.0", END)

        self.text.insert(INSERT, self.console_io.getvalue())

        self.text.config(state=DISABLED)