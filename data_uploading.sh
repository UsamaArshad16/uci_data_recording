#!/bin/bash

# Get the current username
# USERNAME=$(whoami)
# echo "$USERNAME"

echo "Starting data uploading Script--------------------------------"

# Start the Python scripts with the dynamic username
python3 /home/orin2/uci_data_recording/rgb_uploading.py & rgb_pid=$!
python3 /home/orin2/uci_data_recording/point_cloud_uploading.py & pc_pid=$!
python3 /home/orin2/uci_data_recording/audio_uploading.py & audio_pid=$!

# Trap Ctrl+C and forcefully terminate processes
trap 'kill -9 $rgb_pid $pc_pid $audio_pid' INT

# Wait for any background process to finish
wait
