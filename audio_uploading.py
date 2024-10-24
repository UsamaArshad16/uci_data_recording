import os
import requests
import time
import netifaces
from pathlib import Path
import argparse
import getpass

#############################

# Function to get the MAC address of the device
def get_mac_address():
    try:
        interface = 'eth0'  # Use the correct network interface on your Jetson
        mac_address = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
        return mac_address
    except Exception as e:
        print(f"An error occurred while fetching the MAC address: {e}")
        return None

# Function to upload files in the folder
def upload_files_in_folder(url, folder_path, token, patient_id, device_id):
    files = sorted(os.listdir(folder_path), key=lambda x: int(x.split('_')[1]))[:-1]  # Sorting and excluding the last file
    for file in files:
        file_path = os.path.join(folder_path, file)
        if upload_file(url, file_path, token, patient_id, device_id):
            delete_file(file_path)
        else:
            print(f"Failed to upload file '{file_path}'. Retrying in 10 seconds...")
            time.sleep(10)  # Wait for 10 seconds before retrying

# Function to upload a single file
def upload_file(url, file_path, token, patient_id, device_id):
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            data = {
                'patientId': patient_id,
                'deviceId': device_id
            }
            headers = {'Authorization': token}
            response = requests.post(url, files=files, data=data, headers=headers)

            if response.status_code == 200:
                print(f"File '{file_path}' uploaded successfully.")
                return True
            else:
                print(f"Failed to upload file '{file_path}'. Status code: {response.status_code}")
                return False
    except Exception as e:
        print(f"An error occurred while uploading '{file_path}': {e}")
        return False

# Function to delete a file after upload
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting '{file_path}': {e}")

if __name__ == "__main__":
    # Argument parsing to get the patient ID from the command line
    parser = argparse.ArgumentParser(description="Upload audio files to a local server.")
    parser.add_argument("-p", "--patient_id", required=True, help="Specify the patient ID")
    args = parser.parse_args()

    # Set up the server URL and authorization token
    url = "http://172.27.130.93:3000/upload"  # Local server URL
    token = "token1_here"  # Authorization token

    # Get the MAC address to use as device ID
    device_id = get_mac_address()

    if device_id:
        # Get the current username and home directory
        username = os.environ.get('SUDO_USER', getpass.getuser())
        home_directory = Path(f"/home/{username}")

        # Define the path for the orbbec_recordings and audio folders
        orbbec_recordings_path = home_directory / "orbbec_recordings"
        audio_path = orbbec_recordings_path / "audio"

        # Create directories if they don't exist
        orbbec_recordings_path.mkdir(parents=True, exist_ok=True)
        audio_path.mkdir(parents=True, exist_ok=True)

        if os.path.exists(audio_path):
            try:
                while True:
                    upload_files_in_folder(url, audio_path, token, args.patient_id, device_id)
                    time.sleep(10)  # Wait for 10 seconds before checking again
            except KeyboardInterrupt:
                print("\nLoop terminated by user.")
        else:
            print("Audio folder not found.")
    else:
        print("Unable to retrieve the MAC address.")
