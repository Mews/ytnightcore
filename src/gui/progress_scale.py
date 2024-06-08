import ttkbootstrap as ttk

class ProgressScale(ttk.Canvas):
    def __init__(self, master=None, width=300, height=30, bgcolor="lightgray", fgcolor="lightblue", handle_radius=15, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.progress = 0  # Progress as a percentage (0 to 100)
        self.trail_color = bgcolor
        self.progress_color = fgcolor
        self.handle_color = fgcolor
        self.trail = self.create_rectangle(0, self.height * 0.65, width, height * 0.35, fill=self.trail_color)
        self.rect = self.create_rectangle(0, self.height * 0.65, 0, height * 0.35, fill=self.progress_color)
        self.handle_radius = handle_radius
        self.handle = self.create_oval(
            0, 0, handle_radius * 2, handle_radius * 2, fill=self.handle_color
        )
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        self.bind("<Configure>", self.update_progress_bar)

    def start_drag(self, event):
        self.update_progress(event.x)

    def on_drag(self, event):
        self.update_progress(event.x)

    def stop_drag(self, event):
        self.update_progress(event.x)

    def update_progress(self, x):
        # Clamp x within the bounds of the canvas
        x = max(0, min(self.width, x))
        self.progress = (x / self.width) * 100
        self.update_progress_bar()

    def update_progress_bar(self, event=None):
        self.coords(self.trail, 0, self.height * 0.65, self.width, self.height * 0.35)
        self.coords(self.rect, 0, self.height * 0.65, (self.progress / 100) * self.width, self.height * 0.35)
        handle_center = (self.progress / 100) * self.width
        handle_radius = self.handle_radius
        self.coords(
            self.handle,
            handle_center - handle_radius, (self.height / 2) - handle_radius,
            handle_center + handle_radius, (self.height / 2) + handle_radius,
        )