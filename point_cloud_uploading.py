import os
import requests
from pathlib import Path

# #############################
# # Get the username of the original user who invoked sudo
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

# Define the path for point_cloud folder inside orbbec_recordings
point_cloud_path = orbbec_recordings_path / "point_cloud"

# Create the orbbec_recordings folder if it doesn't exist
if not orbbec_recordings_path.exists():
    orbbec_recordings_path.mkdir(parents=True)
    #print(f"Folder '{orbbec_recordings_path}' created.")
# else:
#     print(f"Folder '{orbbec_recordings_path}' already exists.")

# Create the point_cloud folder if it doesn't exist
if not point_cloud_path.exists():
    point_cloud_path.mkdir(parents=True)
    #print(f"Folder '{point_cloud_path}' created.")
# else:
#     print(f"Folder '{point_cloud_path}' already exists.")

#############################

def upload_files_in_folder(url, folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if upload_file(url, file_path)==True:
                delete_file(file_path)

def upload_file(url, file_path):
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post(url, files=files)

            if response.status_code == 200:
                #print(f"File '{file_path}' uploaded successfully.")
                return True
            else:
                print(f"Failed to upload file '{file_path}'. Status code: {response.status_code}")
                return False
    except Exception as e:
        print(f"An error occurred while uploading '{file_path}': {e}")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting '{file_path}': {e}")

if __name__ == "__main__":
    url = "https://rehabrobottesting.azurewebsites.net/Storage/ucidata/point_clouds"

    if os.path.exists(point_cloud_path):
        try:
            while True:
                upload_files_in_folder(url, point_cloud_path)
        except KeyboardInterrupt:
            print("\nLoop terminated by user.")
    else:
        print("point_cloud_folder folder not found.")
