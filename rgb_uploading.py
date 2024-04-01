import os
import requests

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
        #print(f"File '{file_path}' deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting '{file_path}': {e}")

if __name__ == "__main__":
    url = "https://rehabrobottesting.azurewebsites.net/Storage/ucidata/images"
    main_folder = os.path.expanduser("~/orbbec_recordings")
    rgb_images_folder = os.path.join(main_folder, "rgb_images")

    if os.path.exists(rgb_images_folder):
        try:
            while True:
                upload_files_in_folder(url, rgb_images_folder)
        except KeyboardInterrupt:
            print("\nLoop terminated by user.")
    else:
        print("rgb_images folder not found.")
