import os, threading, time
from fastapi import FastAPI

app = FastAPI()
player = None
is_running = False
current_song = None

def get_player():
    global player
    if player is None:
        from player import RadioPlayer
        player = RadioPlayer(music_dir=r"E:\Music Files\3 Idiots")
    return player

def radio_loop():
    global is_running, current_song
    p = get_player()
    print(f"Radio started with {len(p.playlist)} songs")
    while is_running and p.playlist:
        current_song = p.playlist.pop(0)
        p.play_file(current_song)
        time.sleep(1)

@app.get("/")
def home():
    return {"status": "Running", "now_playing": str(current_song)}

@app.post("/start")
def start_radio():
    global is_running
    if not is_running:
        is_running = True
        threading.Thread(target=radio_loop, daemon=True).start()
    return {"message": "Radio Started"}

@app.post("/stop")
def stop_radio():
    global is_running
    is_running = False
    return {"message": "Stopped"}
