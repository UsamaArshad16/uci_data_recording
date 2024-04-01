import os
import requests
import time

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
    main_folder = os.path.expanduser("~/orbbec_recordings")
    audio_folder = os.path.join(main_folder, "audio")

    if os.path.exists(audio_folder):
        try:
            while True:
                upload_files_in_folder(url, audio_folder)
                time.sleep(10)  # Wait for 10 seconds before checking again
        except KeyboardInterrupt:
            print("\nLoop terminated by user.")
    else:
        print("audio_folder folder not found.")
