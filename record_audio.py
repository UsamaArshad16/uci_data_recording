import os
import pyaudio
import wave
from datetime import datetime, timedelta
import time

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 6  # Change based on firmwares, 1_channel_firmware.bin as 1 or 6_channels_firmware.bin as 6
RESPEAKER_WIDTH = 2
# Run getDeviceInfo.py to get the index
RESPEAKER_INDEX = 0  # Refer to the input device id
CHUNK = 8192  # Increase the CHUNK size further

filename = "check.txt"

p = pyaudio.PyAudio()

info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        device_name = p.get_device_info_by_host_api_device_index(0, i).get('name')
        if "ReSpeaker 4 Mic Array" in device_name:
            print("ReSpeaker 4 Mic Array found at device id:", i)
            RESPEAKER_INDEX = i




stream = p.open(
    rate=RESPEAKER_RATE,
    format=p.get_format_from_width(RESPEAKER_WIDTH),
    channels=RESPEAKER_CHANNELS,
    input=True,
    input_device_index=RESPEAKER_INDEX,
)

print("* recording")

# Create the main folder if it doesn't exist
home_folder = os.path.expanduser("~")
save_folder = os.path.join(home_folder, "orbbec_recordings")
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Create the subfolder for audio if it doesn't exist
audio_folder = os.path.join(save_folder, "audio")
if not os.path.exists(audio_folder):
    os.makedirs(audio_folder)

frames = []
start_check = 0
check_filename = "check.txt"
def check_file_for_string():
    try:
        with open(check_filename, 'r') as file:
            contents = file.read()
            if "true" in contents:
                return True
            else:
                return False
    except FileNotFoundError:
        print(f"File '{check_filename}' not found.")
        return False

current_recording_count = len(os.listdir(audio_folder))
try:
    while True:
        try:
            if check_file_for_string()==True:
                start_check = 1
                # Get audio data
                data = stream.read(CHUNK)
                frames.append(data)

        except OSError as e:
            if e.errno == -9981:  # Input overflow error
                #print("Input overflowed. Continuing...")
                frames = []
            elif e.errno == -9988:  # Stream closed error
                #print("Stream closed. Reopening...")
                stream = p.open(
                    rate=RESPEAKER_RATE,
                    format=p.get_format_from_width(RESPEAKER_WIDTH),
                    channels=RESPEAKER_CHANNELS,
                    input=True,
                    input_device_index=RESPEAKER_INDEX,
                )
            else:
                raise e
            
        if check_file_for_string()==False and start_check == 1:

            # Save the audio recording with the epoch timestamp and count
            current_recording_count = current_recording_count + 1
            timestamp = int((datetime.now() - datetime(1970, 1, 1)).total_seconds() * 1000)
            audio_file_path = os.path.join(audio_folder, f"audio_{current_recording_count}_{timestamp}.wav")
            wf = wave.open(audio_file_path, 'wb')
            wf.setnchannels(RESPEAKER_CHANNELS)
            wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
            wf.setframerate(RESPEAKER_RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            frames = []  # Reset frames for the next recording
            start_check = 0

except KeyboardInterrupt:
    pass

print("* done audio recording")

stream.stop_stream()
stream.close()
p.terminate()
