# azure_recording_setup

## Dependencies
[k4a](https://github.com/microsoft/Azure_Kinect_ROS_Driver/blob/melodic/docs/building.md
)\
Opencv \
pyaudio ``` sudo apt-get install python3-pyaudio```\
pyusb ``` sudo pip3 install pyusb click```

## Clone this repo
   ```   git clone https://github.com/UsamaArshad16/uci_data_recording.git ```

## Scripts

### record_azure.cpp
This file records the rgb and point cloud. The folder maximum size is mentioned in the code (currently 35 GB). After reaching the limit the recording will be paused.
It creates a folder “azure_recordings” in the home and then creates “rgb_images” and “point_cloud” folders inside it, and saves the files with the timestamp.
If the person detected it will start recording for 10 seconds. And after that it will wait for person. If it detected again, the procoess will be on repeat.
### recod_azure
This file was generated from record_azure.cpp using the command \
``` g++ record_azure.cpp -o record_azure -lk4a `pkg-config --cflags --libs opencv4` ```
### find_respeaker_id.py
This code tells what is the index_id of the respeaker_microphone_array. That will be mentioned in the “record_audio.py” file.

### record_audio.py

It records the chunks of audio, the length of the chink is controlled by record_azure. It saves the recording in the “azure_recordings/audio” folder. 

### rgb_uploading.py

This file uploads the rgb images on the cloud and deletes the file that is successfully uploaded. 

### point_cloud_uploading.py

This file uploads the point cloud images on the cloud and deletes the file that is successfully uploaded. 

### audio_uploading.py

This file uploads the audio files on the cloud and deletes the file that is successfully uploaded. 

### setup_recording_nano.sh
This sh file runs all the scripts in a sequence on Jetson Nano.

### setup_recording_xavier.sh
This sh file runs all the scripts in a sequence on Jetson Xavier.

### k4a_orbbec_alteration.sh
This sh file alters the k4a SDK and enable it for Orbbec Camera.
``` chmod +x k4a_orbbec_alteration.sh ```\
``` ./k4a_orbbec_alteration.sh ```

## Start the recordings
Make sure the files are executable and edit the code, set the parameters according to the desired values and generate binaries using command given above.\
Open the terminal and use the commands below \
``` cd uci_data_recording ```\
``` chmod +x setup_recordings_xavier.sh ```\
``` ./setup_recordings_xavier.sh ```
