import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sys
from consoleio import ConsoleIO

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