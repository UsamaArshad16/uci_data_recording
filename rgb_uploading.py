import os
import requests
import netifaces
from pathlib import Path
import argparse
import getpass
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
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if upload_file(url, file_path, token, patient_id, device_id) == True:
                delete_file(file_path)

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

# Function to delete a file after upload
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting '{file_path}': {e}")

if __name__ == "__main__":
    # Argument parsing to get the patient ID from the command line
    parser = argparse.ArgumentParser(description="Upload image files to a local server.")
    parser.add_argument("-p", "--patient_id", required=True, help="Specify the patient ID")
    args = parser.parse_args()

    # Set up the server URL and authorization token
    url = "http://172.27.130.93:3000/upload"
    token = "token1_here"

    # Get the MAC address to use as device ID
    device_id = get_mac_address()

    if device_id:
        # Get the current username and home directory
        username = os.environ.get('SUDO_USER', getpass.getuser())
        home_directory = Path(f"/home/{username}")

        # Define the path for the orbbec_recordings and rgb_images folders
        orbbec_recordings_path = home_directory / "orbbec_recordings"
        rgb_images_path = orbbec_recordings_path / "rgb_images"

        # Create directories if they don't exist
        orbbec_recordings_path.mkdir(parents=True, exist_ok=True)
        rgb_images_path.mkdir(parents=True, exist_ok=True)

        if os.path.exists(rgb_images_path):
            try:
                while True:
                    upload_files_in_folder(url, rgb_images_path, token, args.patient_id, device_id)
            except KeyboardInterrupt:
                print("\nLoop terminated by user.")
        else:
            print("rgb_images folder not found.")
    else:
        print("Unable to retrieve the MAC address.")
