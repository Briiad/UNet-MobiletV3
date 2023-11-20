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
min_depth = 0
max_depth = 255
state = 0 # 0: Stop, 1: Move

# Arduino Serial Communication
# arduino = serial.Serial(
#     port = '/dev/ttyUSB0',
#     baudrate = 9600,
#     timeout = 1,
#     bytesize=serial.EIGHTBITS,
#     parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
#     xonxoff=False,
#     rtscts=False,
#     dsrdtr=False, 
# )

# Function for Arduino Movement
def movement(distance):
    if distance < 1.2:
        state = 0
    elif distance > 1.2:
        state = 1
    
    return str(state)

while True:
    ret, frame = cap.read()

    if not ret:
        break
    
    # Depth Estimation
    depth_map = depth_estimator(frame)
    color_depth = depth_estimator.draw_depth()

    # Center Bounding Box 
    x_min, y_min = int(WIDTH/4), int(HEIGHT/4)
    x_max, y_max = WIDTH - x_min, HEIGHT - y_min
    rectangle = cv2.rectangle(color_depth, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    # Get Depth Value from Bounding Box
    depth_roi_center = depth_map[x_min:x_max, y_min:y_max]

    # Find the Lowest Depth Value
    depth_center = np.amin(depth_roi_center)

    # Display Depth
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(rectangle, "Max: {:.2f} m".format(depth_center), (10, 40), font, 0.5, (0, 255, 0), 2)

    cv2.imshow("Depth", rectangle)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        # arduino.write('0'.encode())
        break
    
    # Send Data to Arduino
    # arduino.write(movement(depth_center).encode())
    
cap.release()
cv2.destroyAllWindows()
# arduino.close()