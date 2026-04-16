import pygame
import os

class MusicPlayer:
    def __init__(self, music_dir):
        self.music_dir = music_dir
        # Загружаем список всех MP3
        self.playlist = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
        self.current_pos = 0
        self.paused = False

    def play(self):
        if self.playlist:
            path = os.path.join(self.music_dir, self.playlist[self.current_pos])
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            self.paused = False

    def stop(self):
        pygame.mixer.music.stop()

    def toggle_pause(self):
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.paused = True

    def next_track(self):
        if self.playlist:
            self.current_pos = (self.current_pos + 1) % len(self.playlist)
            self.play()

    def prev_track(self):
        if self.playlist:
            self.current_pos = (self.current_pos - 1) % len(self.playlist)
            self.play()

    def get_current_name(self):
        if self.playlist:
            return self.playlist[self.current_pos]
        return "No music found"