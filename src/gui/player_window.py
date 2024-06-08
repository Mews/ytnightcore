from gui.progress_scale import ProgressScale
from gui.get_color import get_color

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkfontawesome import icon_to_image

from just_playback import Playback
from datetime import timedelta

class PlayerWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.playback_controller = PlaybackController(master=self)
        self.playback_controller.pack(side=TOP, fill=X, expand=True, anchor=N, pady=(30, 10))


class PlaybackController(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.playback = Playback()
        self.playback.loop_at_end(True)
        
        self.pause_ico = icon_to_image("pause", fill=get_color("light"), scale_to_height=32)
        self.resume_ico = icon_to_image("play", fill=get_color("light"), scale_to_height=32)

        frame_bg = ttk.Style().lookup("TFrame", "background")

        ttk.Style().configure("TButton", background=frame_bg, borderwidth=0)
        ttk.Style().map('TButton', background=[('active', frame_bg)]) # Stop button from changing color on hover

        self.paused = True
        self.pause_button = ttk.Button(master=self, command=self.toggle_pause, takefocus=False)
        self.pause_button.pack(side=TOP, padx=5, pady=5)

        self.playback_progress = PlaybackProgress(master=self)
        self.playback_progress.pack(side=TOP, fill=X, expand=True)
        
        self.load_audio("temp/song.mp3")

        self.loop()
    
    def loop(self):
        self.playback_progress.update_progress(timedelta(seconds=self.playback.curr_pos))

        self.after(10, self.loop)


    def pause(self):
        self.playback.pause()

        self.pause_button.config(image=self.resume_ico)

    def resume(self):
        self.playback.resume()

        self.pause_button.config(image=self.pause_ico)

    def toggle_pause(self):
        if self.paused:
            self.resume()
        else:
            self.pause()
        
        self.paused = not self.paused


    def load_audio(self, path_to_audio):
        self.playback.load_file(path_to_audio)
        self.playback.play()

        self.pause()

        self.playback.seek(0)

        self.playback_progress.update_progress(timedelta(seconds=self.playback.curr_pos))
        self.playback_progress.update_total_time(timedelta(seconds=self.playback.duration))
    
    def jump_to_percentage(self, percentage):
        # Jump to percentage of song
        # E.g percentage = 0.5 jumps to the middle of the song

        self.playback.seek(self.playback.duration*percentage)


class PlaybackProgress(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_progress = "0:00"
        self.total_time = "0:00"
        self.total_seconds = 1
        
        self.grid_columnconfigure(0, weight=15, uniform="xyz")
        self.grid_columnconfigure(1, weight=70, uniform="xyz")
        self.grid_columnconfigure(2, weight=15, uniform="xyz")

        self.current_progress_lbl = ttk.Label(master=self, text=self.current_progress)
        self.current_progress_lbl.grid(row=0, column=0, padx=10, sticky=E)

        self.progress_scale = ttk.Scale(master=self, from_=0, to=1, bootstyle=PRIMARY, command=self.on_scale_change)
        self.progress_scale.grid(row=0, column=1, padx=10, sticky=W+E)

        self.total_time_lbl = ttk.Label(master=self, text=self.total_time)
        self.total_time_lbl.grid(row=0, column=2, padx=10, sticky=W)


    def on_scale_change(self, value):
        self.master.jump_to_percentage(float(value))


    def update_progress(self, progress:timedelta):
        total_seconds = progress.total_seconds()

        # Calculate minutes and seconds
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        # Format the output
        formatted_time = f"{int(minutes)}:{int(seconds):02d}"

        self.current_progress = formatted_time

        self.current_progress_lbl.config(text=formatted_time)

        self.progress_scale.config(value=total_seconds/self.total_seconds)
    
    def update_total_time(self, total_time):
        total_seconds = total_time.total_seconds()

        # Calculate minutes and seconds
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        # Format the output
        formatted_time = f"{int(minutes)}:{int(seconds):02d}"

        self.total_time = formatted_time
        self.total_seconds = total_seconds

        self.total_time_lbl.config(text=formatted_time)