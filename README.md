# azure_recording_setup
## Clone this repo
   ```git clone https://github.com/UsamaArshad16/uci_data_recording.git -b orbbec_k4a_pcl```

## Scripts

### record_azure.cpp
This file records the rgb and point cloud. The folder maximum size is mentioned in the code (currently 35 GB). After reaching the limit the recording will be paused.
It creates a folder “azure_recordings” in the home and then creates “rgb_images” and “point_cloud” folders inside it, and saves the files with the timestamp.
If the person is detected it will start recording for 10 seconds. And after that, it will wait for the person. If it is detected again, the process will be on repeat.

### find_respeaker_id.py
This code tells what is the index_id of the respeaker_microphone_array. That will be mentioned in the “record_audio.py” file.

### record_audio.py
It records the chunks of audio, and the length of the chink is controlled by record_azure. It saves the recording in the “orbbec_recordings/audio” folder. 

### rgb_uploading.py
This file uploads the RGB images on the cloud and deletes the file that is successfully uploaded. 

### point_cloud_uploading.py
This file uploads the point cloud images on the cloud and deletes the file that is successfully uploaded. 

### audio_uploading.py
This file uploads the audio files on the cloud and deletes the file that is successfully uploaded. 

### setup_recording_nano.sh
This sh file runs all the scripts in a sequence on Jetson Nano.

### setup_recording_xavier.sh
This sh file runs all the scripts in a sequence on Jetson Xavier.

### k4a_orbbec_alteration.sh
This sh file installs and alters the k4a SDK and enables it for Orbbec Camera.

## Installation
pip3 ```sudo apt-get -y install python3-pip```\
open-cv ```pip3 install opencv-python```\
pyaudio ``` sudo apt-get install python3-pyaudio```\
pyusb ``` sudo pip3 install pyusb click```\
pcl ```sudo apt-get install libpcl-dev```

### k4a and orbbec alteration
``` cd uci_data_recording ```\
``` chmod +x k4a_orbbec_alteration.sh ```\
``` ./k4a_orbbec_alteration.sh ```
### Build the record_azure.cpp
```g++ record_azure.cpp -o record_azure -lk4a `pkg-config --cflags --libs opencv4` -lpcl_common -lpcl_io```

If the **above command does not work** then provide the paths as well.\
Assuming your PCL headers are located in a standard directory like **/usr/include/pcl-1.10**, you can modify your command like this\
```g++ record_azure.cpp -o record_azure -lk4a `pkg-config --cflags --libs opencv4` -l pcl_io -l pcl_common -I/usr/include/pcl-1.10 -I/usr/include/eigen3```

## Start the recordings
Make sure the files are executable and edit the code, set the parameters according to the desired values, and generate binaries using the command given above.\
``` chmod +x setup_recordings_xavier.sh ```\
``` ./setup_recordings_xavier.sh ```
