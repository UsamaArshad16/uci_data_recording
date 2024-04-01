#!/bin/bash
echo "Starting Installation from Script--------------------------------"

sudo curl -sSL -O https://packages.microsoft.com/config/ubuntu/18.04/multiarch/packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo apt-get update

# Installing Relevant k4a Packages
sudo apt-get install libk4a1.4
sudo apt-get install libk4a1.4-dev
sudo apt-get install k4a-tools

cd ~
git clone https://github.com/microsoft/Azure-Kinect-Sensor-SDK
cd Azure-Kinect-Sensor-SDK
sudo cp scripts/99-k4a.rules /etc/udev/rules.d/
cd ~
sudo rm -r Azure-Kinect-Sensor-SDK/

cd ~

# Step 1: Download and extract the OrbbecSDK_K4A_Wrapper
wget https://github.com/orbbec/OrbbecSDK-K4A-Wrapper/releases/download/v1.9.3/OrbbecSDK_K4A_Wrapper_v1.9.3_arm_64_release_2024_03_22.tar.gz
tar -xzvf OrbbecSDK_K4A_Wrapper_v1.9.3_arm_64_release_2024_03_22.tar.gz
cd OrbbecSDK_K4A_Wrapper_v1.9.3_arm_64_release_2024_03_22

# Make the installation script executable and run it
cd scripts
sudo chmod +x ./install_udev_rules.sh
sudo ./install_udev_rules.sh

# Step 2: Copy files from lib folder to desktop/test folder
cd ..
cd lib
rm -r cmake
sudo cp -r ./* /usr/lib/aarch64-linux-gnu/

# Step 3: Clean up downloaded file and extracted folder
cd ~
rm -rf OrbbecSDK_K4A_Wrapper_v1.9.3_arm_64_release_2024_03_22*
