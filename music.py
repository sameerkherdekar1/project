from fastapi import FastAPI
import threading, time, os, random, tempfile
from pydub import AudioSegment
import pygame

app = FastAPI()
is_running = False
current_song = None

# Fix ffmpeg
try:
    import imageio_ffmpeg

    AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe()
except:
    pass


def radio_loop():
    global is_running, current_song
    music_dir = r"E:\Music Files\3 Idiots"
    pygame.mixer.init()

    files = [os.path.join(music_dir, f) for f in os.listdir(music_dir) if f.lower().endswith(('.mp3', '.m4a', '.wav'))]
    random.shuffle(files)
    print(f"Found {len(files)} songs")

    for song in files:
        if not is_running:
            break
        current_song = song
        print(f"Playing: {song}")
        try:
            sound = AudioSegment.from_file(song)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                temp_path = tmp.name
            sound.export(temp_path, format="wav")
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and is_running:
                time.sleep(0.5)
            os.unlink(temp_path)
        except Exception as e:
            print(f"Error: {e}")


@app.get("/")
def home():
    return {"status": "Radio is Online", "now_playing": str(current_song), "hint": "Go to /docs and POST /start"}


@app.post("/start")
def start_radio():
    global is_running
    if not is_running:
        is_running = True
        threading.Thread(target=radio_loop, daemon=True).start()
        return {"message": "Radio Started - Check terminal for Playing logs"}
    return {"message": "Already Running"}


@app.post("/stop")
def stop_radio():
    global is_running
    is_running = False
    return {"message": "Stopped"}
