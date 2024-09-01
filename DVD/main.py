import vlc
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import messagebox

class DVDHandler(FileSystemEventHandler):
    def __init__(self, vlc_instance):
        super().__init__()
        self.vlc_instance = vlc_instance

    def on_modified(self, event):
        # Vérifiez si le DVD est inséré
        drives = [f"/media/{os.getlogin()}/{d}" for d in os.listdir(f"/media/{os.getlogin()}")]
        for drive in drives:
            if os.path.exists(os.path.join(drive, "VIDEO_TS")):
                # Lance le film
                self.play_dvd(drive)

    def play_dvd(self, dvd_path):
        media = self.vlc_instance.media_new(f"dvd://{dvd_path}")
        player = self.vlc_instance.media_player_new()
        player.set_media(media)
        player.play()
        print("Lecture du DVD en cours...")

def start_watching(vlc_instance):
    path = f"/media/{os.getlogin()}"  # Répertoire où les DVD sont montés
    event_handler = DVDHandler(vlc_instance)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Surveillance du répertoire {path} pour les changements...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def create_gui():
    # Crée une fenêtre graphique simple
    root = tk.Tk()
    root.title("Lecteur de DVD Automatique")
    root.geometry("300x150")

    label = tk.Label(root, text="Insérez un DVD et il sera lu automatiquement.")
    label.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    # Initialise l'instance VLC
    vlc_instance = vlc.Instance()
    
    # Démarre l'interface graphique dans un thread séparé
    from threading import Thread
    gui_thread = Thread(target=create_gui)
    gui_thread.start()

    # Démarre la surveillance des DVD
    start_watching(vlc_instance)
