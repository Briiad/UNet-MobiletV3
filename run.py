import cv2
import numpy as np

from mobileUnet_SC import MobileUnet_SC
from mobileUnet_GLP import MobileUnet_GLP

cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! appsink")

cv2.namedWindow("Depth", cv2.WINDOW_NORMAL)

model_path = './model.onnx'
depth_estimator = MobileUnet_SC(model_path)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break
    
    depth_map = depth_estimator(frame)
    color_depth = depth_estimator.draw_depth(2.5)

    # combined_depth = np.hstack((frame, color_depth))

    cv2.imshow("Depth", color_depth)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()