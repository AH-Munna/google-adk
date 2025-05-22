import pygame
import time
import os
import threading
import queue
from contextlib import redirect_stdout

# Initialize pygame mixer quietly
with open(os.devnull, 'w') as f:
    with redirect_stdout(f):
        pygame.mixer.init()

# Create a queue that will hold tuples of (audio_path, event)
# If event is None, the caller isn't waiting for playback to complete.
audio_queue = queue.Queue()

def audio_worker():
    """Background worker that processes the audio queue sequentially."""
    while True:
        item = audio_queue.get()  # Blocks until an item is available
        if item is None:
            break  # Allows for graceful shutdown if needed
        audio_path, event = item
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            # Wait until the current audio finishes playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except Exception as e:
            print(f"Error playing audio {audio_path}: {e}")
        finally:
            # If an event was provided, signal that playback is complete
            if event is not None:
                event.set()
            audio_queue.task_done()

# Start the worker thread as a daemon so it exits when the main program does
worker_thread = threading.Thread(target=audio_worker, daemon=True)
worker_thread.start()

def play_audio(audio_path, wait=False):
    """
    Queues an audio file for playback.
    
    Parameters:
      audio_path (str): Path to the audio file.
      wait (bool): If True, block until the audio has finished playing.
      
    The function enqueues the audio file for sequential playback.
    If wait is True, it uses a threading.Event to block the caller until
    the playback is finished.
    """
    event = threading.Event() if wait else None
    audio_queue.put((audio_path, event))
    if wait:
        # Wait for the audio to finish playing (the worker thread will set the event)
        event.wait()