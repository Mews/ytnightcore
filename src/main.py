from gui.main import RootWindow
from settings import theme

root = RootWindow(themename=theme, title="Youtube Nightcore")

root.geometry("1100x850")
root.iconbitmap("assets/ytnightcore.ico")

root.mainloop()