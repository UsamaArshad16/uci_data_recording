#!/bin/bash
export DISPLAY=:0
sleep 3

# Get the current username
USERNAME=$(whoami)
echo "$USERNAME"

# Run the record_azure_display command in the background and store the process ID
/home/$USERNAME/uci_data_recording/record_azure_display & record_azure_display_pid=$!
python3 /home/$USERNAME/uci_data_recording/record_audio.py & record_audio_pid=$!
# Wait for 15 seconds
sleep 5

# Run the python3 rgb_uploading.py command in the background and store the process ID
python3 /home/$USERNAME/uci_data_recording/rgb_uploading.py & rgb_pid=$!
python3 /home/$USERNAME/uci_data_recording/point_cloud_uploading.py & pc_pid=$!
python3 /home/$USERNAME/uci_data_recording/audio_uploading.py & audio_pid=$!

# Trap Ctrl+C and forcefully terminate processes
trap 'kill -9 $record_azure_pid $record_audio_pid $rgb_pid $pc_pid $audio_pid' INT

# Wait for any background process to finish
wait
