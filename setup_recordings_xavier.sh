#!/bin/bash
export DISPLAY=:0
sleep 3

# Get the current username
USERNAME=$(whoami)
echo "$USERNAME"

# Check if an argument was passed, if not, exit with an error message
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <patient_id>"
  exit 1
fi

# Assign the first argument as the patient_id
PATIENT_ID=$1

# Run the record_azure command in the background and store the process ID
/home/$USERNAME/uci_data_recording/record_azure & record_azure_pid=$!
python3 /home/$USERNAME/uci_data_recording/record_audio.py & record_audio_pid=$!
# Wait for 5 seconds
sleep 5

# Pass the patient_id to the Python scripts when running them in the background
python3 /home/$USERNAME/uci_data_recording/rgb_uploading.py --patient_id $PATIENT_ID & rgb_pid=$!
python3 /home/$USERNAME/uci_data_recording/point_cloud_uploading.py --patient_id $PATIENT_ID & pc_pid=$!
python3 /home/$USERNAME/uci_data_recording/audio_uploading.py --patient_id $PATIENT_ID & audio_pid=$!

# Trap Ctrl+C and forcefully terminate processes
trap 'kill -9 $record_azure_pid $record_audio_pid $rgb_pid $pc_pid $audio_pid' INT

# Wait for any background process to finish
wait
