import cv2
import numpy as np
import time
import serial 

from mobileUnet_SC import MobileUnet_SC

cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! appsink")

cv2.namedWindow("Depth", cv2.WINDOW_NORMAL)

# Global Variables
model_path = './model.onnx'
depth_estimator = MobileUnet_SC(model_path)
WIDTH = 256
HEIGHT = 192
frame_time = 0
prev_frame_time = 0
state = 0 # 0: Stop, 1: Move, 2: Turn Left, 3: Turn Right, 4: Backward

# Arduino Serial Communication
arduino = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 9600,
    timeout = 1
)

# Function for Arduino Movement
def movement(dist_center, dist_left, dist_right):
    if dist_center < 0.2:
        state = 0
        if dist_left > 0.2 and dist_right < 0.2:
            state = 2
        elif dist_right > 0.2 and dist_left < 0.2:
            state = 3
        elif dist_left < 0.2 and dist_right < 0.2:
            state = 4
    elif dist_center > 0.2:
        state = 1
    
    print(str(state))
    return str(state)

while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    # Depth Estimation
    depth_map = depth_estimator(frame)
    color_depth = depth_estimator.draw_depth()

    # Center Crop Rectangle
    center = color_depth.copy()
    center = center[:192, 85:170]
    depth_roi_center = depth_map[:192, 85:170]

    # Left Crop Rectangle
    left = color_depth.copy()
    left = left[:192, :85]
    depth_roi_left = depth_map[:192, :85]

    # Right Crop Rectangle
    right = color_depth.copy()
    right = right[:192, 170:]
    depth_roi_right = depth_map[:192, 170:]

    # Calculate Average Depth Value
    depth_center = np.median(depth_roi_center)
    depth_left = np.median(depth_roi_left)
    depth_right = np.median(depth_roi_right)

    # Display Depth
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(center, "Center: {:.2f} m".format(depth_center), (10, 10), font, 0.35, (0, 255, 0), 2)
    cv2.putText(left, "Left: {:.2f} m".format(depth_left), (10, 10), font, 0.35, (0, 255, 0), 2)
    cv2.putText(right, "Right: {:.2f} m".format(depth_right), (10, 10), font, 0.35, (0, 255, 0), 2)

    # Concatenate
    depth = np.concatenate((left, center, right), axis=1)
    cv2.imshow("Depth", depth)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        arduino.write('0'.encode())
        break
    
    # Send Data to Arduino
    arduino.write(movement(depth_center, depth_left, depth_right).encode())
    
cap.release()
cv2.destroyAllWindows()
arduino.close()