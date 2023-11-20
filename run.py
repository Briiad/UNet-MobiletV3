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
state = 0 # 0: Stop, 1: Move
scaling_factor = 0.1

# Arduino Serial Communication
arduino = serial.Serial(
    port = '/dev/ttyUSB0',
    baudrate = 9600,
    timeout = 1,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False, 
)

# Function for Arduino Movement
def movement(distance):
    if distance < 0.19:
        state = 0
    elif distance > 0.18:
        state = 1
    
    return str(state)

while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    # Depth Estimation
    depth_map = depth_estimator(frame)
    depth_map_left = depth_estimator(frame)
    depth_map_right = depth_estimator(frame)
    color_depth = depth_estimator.draw_depth()

    # Bounding Box Center
    x_min, y_min = int(WIDTH / 4), int(HEIGHT / 4)
    x_max, y_max = WIDTH - x_min, HEIGHT - y_min
    # Bounding Box Left
    x_min_left, y_min_left = 0, int(HEIGHT / 4)
    x_max_left, y_max_left = int(WIDTH / 4), HEIGHT - y_min_left
    # Bounding Box Right
    x_min_right, y_min_right = WIDTH - x_min_left, y_min_left
    x_max_right, y_max_right = WIDTH, y_max_left

    # Draw Rectangle
    rectangle = cv2.rectangle(color_depth, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2) # Center
    rectangle = cv2.rectangle(color_depth, (x_min_left, y_min_left), (x_max_left, y_max_left), (0, 255, 0), 2) # Left
    rectangle = cv2.rectangle(color_depth, (x_min_right, y_min_right), (x_max_right, y_max_right), (0, 255, 0), 2) # Right

    # Get Depth Value from Bounding Box
    depth_roi_center = depth_map[x_min:x_max, y_min:y_max]
    depth_roi_left = depth_map_left[x_min_left:x_max_left, y_min_left:y_max_left]
    depth_roi_right = depth_map_right[x_min_right:x_max_right, y_min_right:y_max_right]

    # Calculate Average Depth Value
    depth_center = np.median(depth_roi_center)
    depth_left = np.median(depth_roi_left)
    depth_right = np.median(depth_roi_right)

    # Display Depth
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(rectangle, "Center: {:.2f} m".format(depth_center), (10, 40), font, 0.5, (0, 255, 0), 2)
    cv2.putText(rectangle, "Left: {:.2f} m".format(depth_left), (10, 60), font, 0.5, (0, 255, 0), 2)
    cv2.putText(rectangle, "Right: {:.2f} m".format(depth_right), (10, 80), font, 0.5, (0, 255, 0), 2)

    cv2.imshow("Depth", rectangle)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        arduino.write('0'.encode())
        break
    
    # Send Data to Arduino
    arduino.write(movement(depth_center).encode())
    
cap.release()
cv2.destroyAllWindows()
arduino.close()