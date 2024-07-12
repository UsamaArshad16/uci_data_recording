import os
import requests
import time
from pathlib import Path

#############################
# Get the username of the original user who invoked sudo
# original_user = os.environ.get('SUDO_USER')
# print("USERNAME:", original_user)

# Get the current username
import getpass
username = getpass.getuser()
#print("USERNAME:", username)

# If the script is run without sudo, use the current user's home directory
if username is None:
    home_directory = Path.home()
else:
    home_directory = Path(f"/home/{username}")

# Define the path for orbbec_recordings folder
orbbec_recordings_path = home_directory / "orbbec_recordings"

# Define the path for audio folder inside orbbec_recordings
audio_path = orbbec_recordings_path / "audio"

# Create the orbbec_recordings folder if it doesn't exist
if not orbbec_recordings_path.exists():
    orbbec_recordings_path.mkdir(parents=True)
    #print(f"Folder '{orbbec_recordings_path}' created.")
# else:
#     print(f"Folder '{orbbec_recordings_path}' already exists.")

# Create the audio folder if it doesn't exist
if not audio_path.exists():
    audio_path.mkdir(parents=True)
    #print(f"Folder '{audio_path}' created.")
# else:
#     print(f"Folder '{audio_path}' already exists.")

#############################

def upload_files_in_folder(url, folder_path):
    files = sorted(os.listdir(folder_path), key=lambda x: int(x.split('_')[1]))[:-1]
    for file in files:
        file_path = os.path.join(folder_path, file)
        if upload_file(url, file_path):
            delete_file(file_path)
        else:
            print(f"Failed to upload file '{file_path}'. Retrying in 10 seconds...")
            time.sleep(10)  # Wait for 10 seconds before retrying

def upload_file(url, file_path):
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files)

            if response.status_code == 200:
                print(f"File '{file_path}' uploaded successfully.")
                return True
            else:
                print(f"Failed to upload file '{file_path}'. Status code: {response.status_code}")
                return False
    except Exception as e:
        print(f"An error occurred while uploading '{file_path}': {e}")
        return False

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting '{file_path}': {e}")

if __name__ == "__main__":
    url = "https://rehabrobottesting.azurewebsites.net/Storage/ucidata/audios"
    if os.path.exists(audio_path):
        try:
            while True:
                upload_files_in_folder(url, audio_path)
                time.sleep(10)  # Wait for 10 seconds before checking again
        except KeyboardInterrupt:
            print("\nLoop terminated by user.")
    else:
        print("audio_folder folder not found.")
