#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import subprocess
import os
import signal
import time
import threading
from subprocess import Popen

# Get the current username
import getpass
username = getpass.getuser()
print("USERNAME:", username)

class RecordingController:
    def __init__(self):
        rospy.init_node('recording_controller', anonymous=True)
        self.subscriber = rospy.Subscriber('/module_status', String, self.callback)
        
        # Initialize process variables
        self.processes = {
            "record_azure": None,
            "record_audio": None
            # "rgb_uploading": None,
            # "point_cloud_uploading": None,
            # "audio_uploading": None
        }
        # self.camera_process = None ####
        
        self.running = False
        self.monitor_thread = threading.Thread(target=self.monitor_processes)
        self.monitor_thread.start()
        rospy.loginfo("Recording Controller Node has started.")
        rospy.spin()

    def callback(self, msg):
        rospy.loginfo(f"Received message: {msg.data}")
        if msg.data == "RecMode,1":
            # self.start_camera()
            # time.sleep(3)
            self.start_recording()
        elif msg.data == "RecMode,0":
            self.stop_recording()
            # self.stop_camera()
            
            
    #@################
    # def start_camera(self):
    #     if self.camera_process is None:
    #         rospy.loginfo("\nStarting Navigation...")
    #         self.camera_process = Popen(["/home/orin2/uci_data_recording/record_azure"])

    # def stop_camera(self):
    #     if self.camera_process is not None:
    #         rospy.loginfo("\nStopping Navigation...")
    #         self.camera_process.terminate()
    #         self.camera_process.wait()
    #         self.camera_process = None
    #         print("\nListening to the rostopic '/module_status' .... \n")
    #################

    def start_recording(self):
        if not self.running:
            rospy.loginfo("Starting recording processes...")
            os.environ['DISPLAY'] = ':0'
            try:
                
                self.processes["record_azure"] = subprocess.Popen([f'/home/{username}/uci_data_recording/record_azure'])
                self.processes["record_audio"] = subprocess.Popen(['python3', f'/home/{username}/uci_data_recording/record_audio.py'])
                
                # self.processes["record_azure"] = subprocess.Popen(['/home/orin2/uci_data_recording/record_azure'])
                # self.processes["record_audio"] = subprocess.Popen(['python3', '/home/orin2/uci_data_recording/record_audio.py'])
                
                # self.processes["rgb_uploading"] = subprocess.Popen(['python3', '/home/orin2/uci_data_recording/rgb_uploading.py'])
                # self.processes["point_cloud_uploading"] = subprocess.Popen(['python3', '/home/orin2/uci_data_recording/point_cloud_uploading.py'])
                # self.processes["audio_uploading"] = subprocess.Popen(['python3', '/home/orin2/uci_data_recording/audio_uploading.py'])
                
                self.running = True
            except Exception as e:
                rospy.logerr(f"Failed to start recording processes: {e}")
                self.stop_all_processes()
                self.stop_camera()
                self.running = False
        else:
            rospy.logwarn("Recording processes are already running.")

    def stop_recording(self):
        if self.running:
            rospy.loginfo("Stopping recording processes...")
            self.stop_all_processes()
            self.write_check_file(False)
            self.running = False
        else:
            rospy.logwarn("No recording processes are running.")

    def stop_all_processes(self):
        for process_name, process in self.processes.items():
            if process is not None:
                process.send_signal(signal.SIGINT)
                process.wait()
                self.processes[process_name] = None

    def write_check_file(self, status):
        with open(f'/home/{username}/uci_data_recording/check.txt', 'w') as f:
        # with open('/home/orin2/uci_data_recording/check.txt', 'w') as f:
            f.write(str(status).lower())

    def monitor_processes(self):
        while not rospy.is_shutdown():
            if self.running:
                for process_name, process in self.processes.items():
                    if process is not None:
                        retcode = process.poll()
                        if retcode is not None:
                            rospy.logerr(f"{process_name} process terminated unexpectedly with return code {retcode}. Restarting...")
                            self.processes[process_name] = None
                            self.start_recording()
            time.sleep(1)

if __name__ == '__main__':
    try:
        RecordingController()
    except rospy.ROSInterruptException:
        pass
