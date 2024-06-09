from gui.progress_scale import ProgressScale
from gui.get_color import get_color
from log import log

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkfontawesome import icon_to_image

from just_playback import Playback
from datetime import timedelta
from simplestretch import speedup_audio
import soundfile

class PlayerWindow(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.playback_controller = PlaybackController(master=self)
        self.playback_controller.pack(side=TOP, fill=X, anchor=N, pady=(30, 10))

        self.options_menu = OptionsMenu(master=self)
        self.options_menu.pack(side=TOP, fill=X, expand=True, anchor=N, pady=(45, 10))


class PlaybackController(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.song_is_loaded = False

        self.playback = Playback()
        self.playback.loop_at_end(True)
        
        self.pause_ico = icon_to_image("pause", fill=get_color("light"), scale_to_height=32)
        self.resume_ico = icon_to_image("play", fill=get_color("light"), scale_to_height=32)

        frame_bg = ttk.Style().lookup("TFrame", "background")

        ttk.Style().configure("TButton", background=frame_bg, borderwidth=0)
        ttk.Style().map('TButton', background=[('active', frame_bg)]) # Stop button from changing color on hover

        self.paused = True
        self.pause_button = ttk.Button(master=self, command=self.toggle_pause, takefocus=False, image=self.resume_ico)
        self.pause_button.pack(side=TOP, padx=5, pady=5)

        self.playback_progress = PlaybackProgress(master=self)
        self.playback_progress.pack(side=TOP, fill=X, expand=True)

        self.loop()
    
    def loop(self):
        if self.song_is_loaded:
            self.playback_progress.update_progress(timedelta(seconds=self.get_progress_on_og_audio()))

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


    def get_progress_on_og_audio(self):
        speed = self.get_current_speed()

        current_duration = self.og_sound_duration / speed

        return (self.playback.curr_pos * self.og_sound_duration) / current_duration


    def load_audio(self):
        log("Player", "Loaded new audio")

        self.og_audio_data, self.og_audio_samplerate = soundfile.read("temp/song.mp3")
        self.og_sound_duration = soundfile.info("temp/song.mp3").duration

        self.set_speed(self.get_current_speed())

        self.reload_audio()

        self.pause()
        self.paused = True

        self.playback_progress.update_progress(timedelta(seconds=self.playback.curr_pos))
        self.playback_progress.update_total_time(timedelta(seconds=self.og_sound_duration))

        self.song_is_loaded = True
        
    
    def reload_audio(self):
        self.playback.load_file("temp/out.wav")
        self.playback.play()
        self.playback.loop_at_end(True)

        if self.paused:
            self.pause()
        else:
            self.resume()

        self.playback.set_volume(self.get_current_volume())


    def jump_to_percentage(self, percentage):
        # Jump to percentage of song
        # E.g percentage = 0.5 jumps to the middle of the song

        self.playback.seek(self.playback.duration*percentage)
    
    def set_volume(self, volume_normal):
        self.playback.set_volume(volume_normal)

    
    def set_speed(self, speed_normal):
        self.playback = Playback()

        speedup_audio(audio=self.og_audio_data, samplerate=self.og_audio_samplerate, factor=speed_normal, output="temp/out.wav")

        self.reload_audio()
    
    def get_current_speed(self):
        return self.master.options_menu.get_current_speed()

    def get_current_volume(self):
        return self.master.options_menu.get_current_volume()


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



class OptionsMenu(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.volume_lbl = ttk.Label(master=self)
        self.volume_lbl.pack(side=TOP, fill=X, expand=True, anchor=N, padx=225)

        self.volume_scale = ttk.Scale(master=self, from_=0, to=1, command=self.on_volume_change)
        self.volume_scale.set(0.5)
        self.volume_scale.pack(side=TOP, fill=X, expand=True, anchor=N, padx=225)


        self.speed_lbl = ttk.Label(master=self, text="Playback speed: 1.00")
        self.speed_lbl.pack(side=TOP, fill=X, expand=True, anchor=N, padx=225, pady=(20,0))

        self.speed_scale = ttk.Scale(master=self, from_=0.25, to=2, command=self.on_speed_change, value=1)
        self.speed_scale.pack(side=TOP, fill=X, expand=True, anchor=N, padx=225)

    
    def on_volume_change(self, value):
        self.master.playback_controller.set_volume(float(value))

        self.volume_lbl.config(text="Volume: "+str(int(float(value)*100)))

    def on_speed_change(self, value):
        self.master.playback_controller.set_speed(float(value))

        self.speed_lbl.config(text="Playback speed: "+value[:4])
    
    def get_current_speed(self):
        return self.speed_scale.get()

    def get_current_volume(self):
        return self.volume_scale.get()