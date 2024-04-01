import cv2
import pykinect_azure as pykinect
import numpy as np
import os
import time
from datetime import datetime, timedelta

# Function to get the folder size in bytes
def get_folder_size(folder):
    total_size = 0
    for path, dirs, files in os.walk(folder):
        for f in files:
            fp = os.path.join(path, f)
            total_size += os.path.getsize(fp)
    return total_size

if __name__ == "__main__":
    # Initialize the library, if the library is not found, add the library path as an argument
    print("Testin 1")
    pykinect.initialize_libraries()
    print("Testin 2")
    # Modify camera configuration
    device_config = pykinect.default_configuration
    device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
    device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
    print("Testin 3")
    # Try to start the device
    try:
        device = pykinect.start_device(config=device_config)
        print("Testin 4")
    except pykinect.DeviceOpenError as e:
        print("Failed to open the Azure Kinect device:", e)
        exit(1)

    # Create the main folder if it doesn't exist
    save_folder = "/home/nano1/azure_recording"
    if not os.path.exists(save_folder):
        print("Testin 5")
        os.makedirs(save_folder)

    max_total_size_bytes = 2 * 1024 * 1024 * 1024  # 2 GB
    print("Testin 6")
    recording_duration = timedelta(minutes=1)
    current_start_time = datetime.now()
    current_recording_count = 1
    print("Testin 7")
    fps = 15
    frame_interval = 1.0 / fps
    print("Testin 8")
    while True: 
        # Check total folder size before recording
        total_size = get_folder_size(save_folder)
        if total_size >= max_total_size_bytes:
            print("Total folder size limit reached. Stopping recording.")
            break

        # Get capture
        try:
            capture = device.update()
        except pykinect.DeviceOpenError as e:
            print("Failed to capture frame from Azure Kinect device:", e)
            continue

        # Get the color image from the capture
        ret, color_image = capture.get_color_image()

        # Get the color depth image from the capture
        ret_depth, depth_image = capture.get_colored_depth_image()

        # Get the 3D point cloud
        try:
            ret_points, points = capture.get_pointcloud()
        except Exception as e:
            print("Failed to retrieve point cloud from Azure Kinect device:", e)
            continue

        if not ret or not ret_depth or not ret_points:
            continue

        if points is None:
            continue

        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")[:-3]

        # Check if recording duration has exceeded 1 minute
        elapsed_time = datetime.now() - current_start_time
        if elapsed_time >= recording_duration:
            current_start_time = datetime.now()
            current_recording_count += 1

        # Create subfolders for the current recording
        subfolder_name = f"T{current_recording_count}"
        current_recording_folder = os.path.join(save_folder, "images", subfolder_name)
        if not os.path.exists(current_recording_folder):
            os.makedirs(current_recording_folder)

        pc_folder = os.path.join(save_folder, "point_cloud", subfolder_name)
        if not os.path.exists(pc_folder):
            os.makedirs(pc_folder)

        # Save the RGB image with the timestamp
        rgb_image_path = os.path.join(current_recording_folder, f"image_{timestamp}.jpg")
        if ret and color_image is not None:
            cv2.imwrite(rgb_image_path, color_image)

        # Save the point cloud data with the timestamp
        pc_path = os.path.join(pc_folder, f"pointcloud_{timestamp}.npy")

        # Check folder size before saving
        current_recording_size = get_folder_size(current_recording_folder)
        if current_recording_size < max_total_size_bytes:
            try:
                np.save(pc_path, points)
            except Exception as e:
                print("Failed to save point cloud data:", e)
        else:
            print("Recording folder size limit reached. Stopping saving.")

        # Plot the color image and depth image
        #cv2.imshow("Color Image", color_image)
        #cv2.imshow('Depth Image', depth_image)

        # Press q key to stop
        if cv2.waitKey(1) == ord('q'):
            break

        # Control frame rate
        time.sleep(frame_interval)

    # Stop and close the device
    device.stop_device()
