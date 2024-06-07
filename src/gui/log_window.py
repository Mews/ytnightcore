import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sys
from consoleio import ConsoleIO
from datetime import datetime

class LogWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text = ttk.ScrolledText(master=self, state=DISABLED)
        self.text.pack(expand=True, fill=BOTH)

        self.console_io = ConsoleIO(callback=self.update_text)
        # Redirect print statements to log window's console io
        sys.stdout = self.console_io
        sys.stderr = self.console_io

    def update_text(self):
        self.text.config(state=NORMAL)

        self.text.delete("1.0", END)

        #line = self.console_io.popline()

        #if not line == "\n":
            #current_time = datetime.now().strftime("%H:%M:%S")

            #self.text.insert(END, "( " + current_time + " ) " + line + "\n")
        
        self.text.insert(INSERT, self.console_io.getvalue())

        self.text.config(state=DISABLED)