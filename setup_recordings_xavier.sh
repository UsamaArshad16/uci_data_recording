#!/bin/bash
export DISPLAY=:0
sleep 3
# Run the record_azure command in the background and store the process ID
/home/orin2/uci_data_recording/record_azure & record_azure_pid=$!
python3 /home/orin2/uci_data_recording/record_audio.py & record_audio_pid=$!
# Wait for 15 seconds
sleep 5

# Run the python3 rgb_uploading.py command in the background and store the process ID
python3 /home/orin2/uci_data_recording/rgb_uploading.py & rgb_pid=$!
python3 /home/orin2/uci_data_recording/point_cloud_uploading.py & pc_pid=$!
python3 /home/orin2/uci_data_recording/audio_uploading.py & audio_pid=$!

# Trap Ctrl+C and forcefully terminate processes
trap 'kill -9 $record_azure_pid $record_audio_pid $rgb_pid $pc_pid $audio_pid' INT

# Wait for any background process to finish
wait
