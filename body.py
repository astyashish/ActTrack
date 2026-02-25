# MediaPipe Body
import mediapipe as mp # type: ignore
#from mediapipe.tasks import python # type: ignore
#from mediapipe.tasks.python import vision # type: ignore
from clientUDP import ClientUDP
import numpy as np # type: ignore
import json
import os

import cv2 # type: ignore
import threading
import time
import global_vars 
import struct
import math
# State to track the current action



# the capture thread captures images from the WebCam on a separate thread (for performance)

class CaptureThread(threading.Thread):


    cap = None
    ret = None
    frame = None
    isRunning = False
    counter = 0
    timer = 0.0
    def run(self):
        self.cap = cv2.VideoCapture(global_vars.CAM_INDEX)
        # Lower resolution for better FPS (can adjust based on requirements)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)  # Limit FPS for smoother capture
        
        #print("Opened Capture @ %s fps"%str(self.cap.get(cv2.CAP_PROP_FPS)))
        while not global_vars.KILL_THREADS:
            self.ret, self.frame = self.cap.read()
            self.isRunning = True
            if global_vars.DEBUG:
                self.counter = self.counter+1
                if time.time()-self.timer>=3:
                    #print("Capture FPS: ",self.counter/(time.time()-self.timer))
                    self.counter = 0
                    self.timer = time.time()
#--button--------------------------------------------

#--calculating angle -- ---- --------- - - - - - - - -

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 



# ----------------Function to draw table on the side with key body part coordinates--------------------------------------------------------
def draw_table(image, key_landmarks):
    # Create a black rectangle for the table on the right side
    table_width = 500  # Width of the table
    table_height = image.shape[0]  # Match the height of the webcam feed
    

    # Create space for the table by extending the original image width
    extended_image = cv2.copyMakeBorder(image, 0, 0, 0, table_width, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    
    # Set table headers
    header_y = 50
    cv2.putText(extended_image, "Body Part", (image.shape[1] + 10, header_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(extended_image, "X", (image.shape[1] + 150, header_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(extended_image, "Y", (image.shape[1] + 200, header_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(extended_image, "Z", (image.shape[1] + 250, header_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


    # Draw rows with body part names and coordinates
    row_height = 30  # Height of each row
    for i, (part, landmark) in enumerate(key_landmarks.items()):
        x = int(landmark.x * image.shape[1])  # Scale x relative to image width
        y = int(landmark.y * image.shape[0])  # Scale y relative to image height
        z = int(landmark.z * image.shape[-1])  # Scale z relative to image depth

        # Display body part name and coordinates in the table
        cv2.putText(extended_image, part, (image.shape[1] + 10, header_y + (i + 1) * row_height), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(extended_image, f"{x}", (image.shape[1] + 150, header_y + (i + 1) * row_height), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(extended_image, f"{y}", (image.shape[1] + 200, header_y + (i + 1) * row_height), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(extended_image, f"{z}", (image.shape[1] + 250, header_y + (i + 1) * row_height), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 305), 1)

    return extended_image


#------------------------------------------------------xxx----------------------------------------------------------------------
# the body thread actually does the 
# processing of the captured images, and communication with unity
class BodyThread(threading.Thread):
    data = ""
    dirty = True
    pipe = None
    timeSinceCheckedConnection = 0
    timeSincePostStatistics = 0
    head_landmark=None
    #------------smoother or filter ------------------------------------------------------------
    def __init__(self,callback=None):
        super().__init__()
        self.best_match=None
        self.running = True
        self.latest_results = None
        self.landmark_history = {i: [] for i in range(33)}  # History buffer for smoothing
        self.history_length = 10  # Smoothing window
        self.callback = callback  # Store the callback
        self.key_landmarks = {}
        self.resultis=False
        self.keymap=None

    def smooth_landmarks(self, landmark_index, new_value):
        """Smooth landmark values using a sliding window."""
        if len(self.landmark_history[landmark_index]) >= self.history_length:
            self.landmark_history[landmark_index].pop(0)  # Remove oldest value

        self.landmark_history[landmark_index].append(new_value)  # Add new value

        # Calculate smoothed value (average of the buffer)
        smoothed_value = np.mean(self.landmark_history[landmark_index], axis=0)
        return smoothed_value
    def process_landmarks_and_calculate_angles(self, results):
        """Extract landmarks, calculate angles, and find the best match."""
        # Extract landmarks
        if not results.pose_landmarks:
            return None, 0, None  # No landmarks detected

        landmarks = results.pose_landmarks.landmark

        # Define key landmark points
        def get_point(index):
            return [landmarks[index].x, landmarks[index].y]

        # Calculate angles
        def calculate_angle(point_a, point_b, point_c):
            # Calculate vectors
            ba = np.array(point_a) - np.array(point_b)
            bc = np.array(point_c) - np.array(point_b)
            # Calculate cosine angle
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            # Return angle in degrees
            return np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

        # Extract key body parts
        points = {
            "nose": get_point(0),
            "l_shoulder": get_point(11),
            "r_shoulder": get_point(12),
            "l_elbow": get_point(13),
            "r_elbow": get_point(14),
            "l_wrist": get_point(15),
            "r_wrist": get_point(16),
            "l_hip": get_point(23),
            "r_hip": get_point(24),
            "l_knee": get_point(25),
            "r_knee": get_point(26),
            "l_ankle": get_point(27),
            "r_ankle": get_point(28),
            "l_foot_index": get_point(31),
            "r_foot_index": get_point(32),
        }

        # Calculate angles
        real_time_angles = {
            "LeftElbow": calculate_angle(points["l_shoulder"], points["l_elbow"], points["l_wrist"]),
            "RightElbow": calculate_angle(points["r_shoulder"], points["r_elbow"], points["r_wrist"]),
            "LeftShoulder": calculate_angle(points["l_hip"], points["l_shoulder"], points["l_elbow"]),
            "RightShoulder": calculate_angle(points["r_hip"], points["r_shoulder"], points["r_elbow"]),
            "LeftHip": calculate_angle(points["l_shoulder"], points["l_hip"], points["l_knee"]),
            "RightHip": calculate_angle(points["r_shoulder"], points["r_hip"], points["r_knee"]),
            "LeftKnee": calculate_angle(points["l_hip"], points["l_knee"], points["l_ankle"]),
            "RightKnee": calculate_angle(points["r_hip"], points["r_knee"], points["r_ankle"]),
            "LeftAnkle": calculate_angle(points["l_knee"], points["l_ankle"], points["l_foot_index"]),
            "RightAnkle": calculate_angle(points["r_knee"], points["r_ankle"], points["r_foot_index"]),
        }

        # Calculate head angle
        def calculate_head_angle(v1, v2):
                            # Calculate the dot product
                            dot_product = v1[0] * v2[0] + v1[1] * v2[1]
                            # Calculate the magnitude of both vectors
                            magnitude_v1 = (v1[0]**2 + v1[1]**2)**0.5
                            magnitude_v2 = (v2[0]**2 + v2[1]**2)**0.5
                            # Calculate the angle in radians and convert it to degrees
                            angle_radians = math.acos(dot_product / (magnitude_v1 * magnitude_v2))
                            angle_degrees = math.degrees(angle_radians)
                            return angle_degrees
        # Calculate the vectors from the shoulders to the nose
        shoulder_vector = np.array(points["r_shoulder"]) - np.array(points["l_shoulder"])
        nose_vector = np.array(points["nose"]) - (np.array(points["l_shoulder"]) + np.array(points["r_shoulder"])) / 2
        real_time_angles["HeadAngle"] =  calculate_head_angle(shoulder_vector, nose_vector)
        head_angle=real_time_angles["HeadAngle"]
        # Load joint angles from JSON
        _angles_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "angles.json")
        with open(_angles_path, "r") as file:
            angle_data = json.load(file)

        joint_angles = {name: angles for data in angle_data for name, angles in data.items()}

        # Compare angles with tolerance
        tolerance = 20
        best_match = None
        max_matches = 0

        for name, angles in joint_angles.items():
            matches = sum(
                int(abs(real_time_angles[joint] - angles[joint]) <= tolerance)
                for joint in angles if joint in real_time_angles
            )
            if matches > max_matches:
                max_matches = matches
                best_match = name

        return best_match, max_matches, real_time_angles,head_angle,points["nose"]
    def run(self):

        # Create a window to display the video and add a trackbar as a DEBUG
        #cv2.namedWindow('Body Tracking with Table')

        # Initialize the "DEBUG". False represents "unchecked", True represents "checked".

        #cv2.createTrackbar('DEBUG_GUI', 'Body Tracking with Table', 0, 1,DEBUG_GUI)

        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose

        self.setup_comms()
        
        capture = CaptureThread()
        capture.start()




        with mp_pose.Pose(min_detection_confidence=0.80, min_tracking_confidence=0.5, model_complexity = global_vars.MODEL_COMPLEXITY,static_image_mode = False,enable_segmentation = False) as pose: 
            
            while not global_vars.KILL_THREADS and capture.isRunning==False:
                print("Waiting for camera and capture thread.")
                time.sleep(0.5)
            print("Beginning capture")
                
            while not global_vars.KILL_THREADS and capture.cap.isOpened():
                ti = time.time()

                # Fetch stuff from the capture thread
                ret = capture.ret
                image = capture.frame

                # Image transformations and stuff
                image = cv2.flip(image, cv2.COLOR_BGR2RGB)
                image.flags.writeable = global_vars.DEBUG
                
                # Detections
                results = pose.process(image)
                tf = time.time()
                
                key_landmarks = {}
                # Rendering results
                if global_vars.DEBUG:
                    if time.time()-self.timeSincePostStatistics>=1:
                        if global_vars.DEBUG and time.time() - self.timeSincePostStatistics >= 1:
                            print(f"Theoretical Maximum FPS: {1 / (tf - ti):.2f}")
                            self.timeSincePostStatistics = time.time()               
#-----------------when ashish is there show the values -------------------NEW-------------------------------    
                    if results.pose_landmarks:
                        key_landmarks = {}
                        for i, landmark in enumerate(results.pose_landmarks.landmark):
                            smoothed = self.smooth_landmarks(i, np.array([landmark.x, landmark.y, landmark.z]))
                            key_landmarks[f"Landmark {i}"] = smoothed
                                            
                            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, 
                                                                    mp_drawing.DrawingSpec(color=(255, 69, 0), thickness=1, circle_radius=2),
                                                                    mp_drawing.DrawingSpec(color=(127, 255, 212), thickness=1, circle_radius=1))

# Highlight key body parts and display coordinates-----------------------------------------------------------
                        
                        landmark_indices = {
                            "Head": 0, "Left Shoulder": 11, "Right Shoulder": 12, "Left Elbow": 13, 
                            "Right Elbow": 14, "Left Wrist": 15, "Right Wrist": 16, "Left Hip": 23, 
                            "Right Hip": 24, "Left Knee": 25, "Right Knee": 26, "Left Ankle": 27, "Right Ankle": 28
                        }

                        key_landmarks = {name: results.pose_landmarks.landmark[idx] for name, idx in landmark_indices.items()}

                        #----------------Angle------------------------------------
                        # Load the JSON data
                        _angles_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "angles.json")
                        with open(_angles_path2, "r") as file:
                            angle_data = json.load(file)  # Load the array of dictionaries

                        # Extract joint angles
                        joint_angles = {}
                        for data in angle_data:
                            for name, values in data.items():
                                joint_angles[name] = values

                        if not joint_angles:
                            raise ValueError("No joint angles found in the JSON file.")
 #-----------------------------------------------------real_time_angles-----------------------------------------------------------------                           
                        best_match, max_matches, real_time_angles,head_angle,nose = self.process_landmarks_and_calculate_angles(results)

                        # Display best match
                        if best_match:
                            confidence = 60 if max_matches >= 7 else 50
                            cv2.putText(image, f"Match: {best_match} ({max_matches} joints, {confidence}% chance)",
                                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                            # Trigger actions based on best match
                            if max_matches >= 7:
                                if best_match == "left":
                                    self.keymap = "A"
                                elif best_match == "right":
                                    self.keymap = "D"
                                elif best_match == "up":
                                    self.keymap = "Space"

 #-----------------------------------------------------real_time_angles-----------------------------------------------------------------                           
                                        
                        # Visualize angle--------------------
                        # Draw the coordinate on the frame---
                        # Call the callback with the latest data
                        if self.callback:
                            self.callback(key_landmarks)
                        
                        for part, landmark in key_landmarks.items():
                            x = int(landmark.x * image.shape[1])
                            y = int(landmark.y * image.shape[0])
                            z = int(landmark.z * image.shape[-1])
                            # Draw the coordinate on the frame
                            if global_vars.DEBUG_GUI == True:
                                cv2.putText(
                                    image, 
                                    f"{part}: ({x}, {y}, {z})",  # Include z in the string, not in the position
                                    (int(x), int(y)),  # Only x and y for the position; cast to int if needed
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    0.5, 
                                    (0, 255, 0), 
                                    2
                                )
                                cv2.putText(image, str(int(head_angle)), 
                                    tuple(np.multiply(nose, [640, 480]).astype(int)), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA
                                            )
                            
#--------------------------------------------------------------------------------------------------------------
# Draw table with coordinates
                        image_with_table = draw_table(image, key_landmarks)
                        if global_vars.DEBUG_GUI == True:
                            # Display the image with the table and checkbox state
                            image_with_table = draw_table(image, key_landmarks)
                            # Do something when checkbox is checked
                            cv2.putText(image_with_table, "DEBUG ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                        else:
                            # Display the image and checkbox state
                            image_with_table = image
                            # Do something when checkbox is unchecked
                            cv2.putText(image_with_table, "DEBUG OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    else:
                        image_with_table = image  # No pose detected, show raw image
                    
                    



                    

                    cv2.imshow('Body Tracking', image_with_table)
                    cv2.waitKey(3)


                # Set up data for relay
                self.data = ""
                i = 0
                if results.pose_world_landmarks:
                    hand_world_landmarks = results.pose_world_landmarks
                    for i in range(0,33):
                        self.data += "{}|{}|{}|{}\n".format(i,hand_world_landmarks.landmark[i].x,hand_world_landmarks.landmark[i].y,hand_world_landmarks.landmark[i].z,self.keymap)
                self.send_data(self.data)
                #print(self.data)
                    
        self.pipe.close()
        capture.cap.release()
        cv2.destroyAllWindows()
        pass
    def get_latest_results(self):
        """Return the most recent tracking results."""
        return self.latest_results

    def stop(self):
        """Stop the thread."""
        self.running = False            
    def setup_comms(self):
        ####
        if not hasattr(global_vars, 'USE_LEGACY_PIPES'):
            raise AttributeError("Missing attribute 'USE_LEGACY_PIPES' in global_vars module.")
        ####
        if not global_vars.USE_LEGACY_PIPES:
            self.client = ClientUDP(global_vars.HOST,global_vars.PORT)
            self.client.start()
        else:
            print("Using Pipes for interprocess communication (not supported on OSX or Linux).")
        pass      

    def send_data(self,message):
        ####
        if not hasattr(global_vars, 'USE_LEGACY_PIPES'):
            raise AttributeError("Missing attribute 'USE_LEGACY_PIPES' in global_vars module.")
        ####
        if not global_vars.USE_LEGACY_PIPES:

            self.client.sendMessage(message)
            pass
        else:
            # Maintain pipe connection.
            if self.pipe==None and time.time()-self.timeSinceCheckedConnection>=1:
                try:
                    self.pipe = open(r'\\.\pipe\UnityMediaPipeBody1', 'r+b', 0)
                except FileNotFoundError:
                    print("Waiting for Unity project to run...")
                    self.pipe = None
                self.timeSinceCheckedConnection = time.time()

            if self.pipe != None:
                try:     
                    s = self.data.encode('utf-8') 
                    self.pipe.write(struct.pack('I', len(s)) + s)   
                    self.pipe.seek(0)    
                except Exception as ex:  
                    print("Failed to write to pipe. Is the unity project open?")
                    self.pipe= None
        pass