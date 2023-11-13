import cv2
import numpy as np

from mobileUnet_SC import MobileUnet_SC

cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! appsink")

cv2.namedWindow("Depth", cv2.WINDOW_NORMAL)

model_path = './model.onnx'
depth_estimator = MobileUnet_SC(model_path)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break
    
    # Depth Estimation
    depth_map = depth_estimator(frame)
    color_depth = depth_estimator.draw_depth()

    # Square Bounding Box To measure distance, located at the center of the image
    cv2.rectangle(color_depth, (int(frame.shape[1]/2-50), int(frame.shape[0]/2-50)), (int(frame.shape[1]/2+50), int(frame.shape[0]/2+50)), (0, 255, 0), 2)

    # Estimate distance
    distance = depth_map[int(frame.shape[0]/2), int(frame.shape[1]/2)]

    # Display Distance
    cv2.putText(color_depth, "Distance: {:.2f} cm".format(distance), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display Depth
    cv2.imshow("Depth", color_depth)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()