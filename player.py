import os, random, time, tempfile
from pydub import AudioSegment
import pygame
from dotenv import load_dotenv

load_dotenv()

# Fix ffmpeg for m4a
try:
    import imageio_ffmpeg
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    os.environ["FFMPEG_BINARY"] = ffmpeg_path
    AudioSegment.converter = ffmpeg_path
except:
    pass

class RadioPlayer:
    def __init__(self, music_dir=r"E:\Music Files\3 Idiots"):
        self.music_dir = music_dir
        pygame.mixer.init()
        self.playlist = self.load_playlist()

    def load_playlist(self):
        if not os.path.exists(self.music_dir):
            print(f"Folder not found: {self.music_dir}")
            return []
        files = [os.path.join(self.music_dir, f) for f in os.listdir(self.music_dir) if f.lower().endswith(('.mp3','.wav','.m4a','.mp4'))]
        random.shuffle(files)
        print(f"Found {len(files)} songs")
        return files

    def play_file(self, filepath):
        print(f"Playing: {filepath}")
        try:
            sound = AudioSegment.from_file(filepath)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                temp_path = tmp.name
            sound.export(temp_path, format="wav")
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.5)
            try:
                os.unlink(temp_path)
            except:
                pass
        except Exception as e:
            print(f"Play error: {e}")
