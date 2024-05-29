import os
import pyaudio
import wave
from datetime import datetime
import threading
import time

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 1  # Change based on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
CHUNK = 8192  # Reduced the chunk size for more frequent reads

p = pyaudio.PyAudio()

info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        device_name = p.get_device_info_by_host_api_device_index(0, i).get('name')
        if "ReSpeaker 4 Mic Array" in device_name:
            print("ReSpeaker 4 Mic Array found at device id:", i)
            RESPEAKER_INDEX = i

frames = []
start_check = False
check_filename = "/home/orin2/uci_data_recording/check.txt"

def check_file_for_string():
    try:
        with open(check_filename, 'r') as file:
            contents = file.read()
            return "true" in contents
    except FileNotFoundError:
        print(f"File '{check_filename}' not found.")
        return False

def callback(in_data, frame_count, time_info, status):
    global frames, start_check
    if start_check:
        frames.append(in_data)
    return (None, pyaudio.paContinue)

stream = p.open(
    rate=RESPEAKER_RATE,
    format=p.get_format_from_width(RESPEAKER_WIDTH),
    channels=RESPEAKER_CHANNELS,
    input=True,
    input_device_index=RESPEAKER_INDEX,
    frames_per_buffer=CHUNK,
    stream_callback=callback
)

print("*audio recording thread started")

# Create the main folder if it doesn't exist
home_folder = os.path.expanduser("~")
save_folder = os.path.join(home_folder, "orbbec_recordings")
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Create the subfolder for audio if it doesn't exist
audio_folder = os.path.join(save_folder, "audio")
if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)

current_recording_count = len(os.listdir(audio_folder))

def monitor_file():
    global start_check, frames, current_recording_count
    while True:
        if check_file_for_string():
            if not start_check:
                print("start")
                start_check = True
        else:
            if start_check:
                print("stop")
                start_check = False
                if frames:
                    # Save the audio recording with the epoch timestamp and count
                    current_recording_count += 1
                    timestamp = int((datetime.now() - datetime(1970, 1, 1)).total_seconds() * 1000)
                    audio_file_path = os.path.join(audio_folder, f"audio_{current_recording_count}_{timestamp}.wav")
                    wf = wave.open(audio_file_path, 'wb')
                    wf.setnchannels(RESPEAKER_CHANNELS)
                    wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
                    wf.setframerate(RESPEAKER_RATE)
                    wf.writeframes(b''.join(frames))
                    wf.close()
                    frames = []  # Reset frames for the next recording

        time.sleep(0.1)

monitor_thread = threading.Thread(target=monitor_file)
monitor_thread.daemon = True
monitor_thread.start()

stream.start_stream()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass

print("* done audio recording")

stream.stop_stream()
stream.close()
p.terminate()
