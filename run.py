import cv2
import numpy as np

from mobileUnet_SC import MobileUnet_SC

cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! appsink")

cv2.namedWindow("Depth", cv2.WINDOW_NORMAL)

model_path = './model.onnx'
depth_estimator = MobileUnet_SC(model_path)
WIDTH = 256
HEIGHT = 192

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break
    
    # Depth Estimation
    depth_map = depth_estimator(frame)
    color_depth = depth_estimator.draw_depth()

    # Square Bounding Box 
    x_min, y_min = int(WIDTH/4), int(HEIGHT/4)
    x_max, y_max = WIDTH - x_min, HEIGHT

    rectangle = cv2.rectangle(color_depth, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    # Get Median Depth Value from Bounding Box
    depth_roi = depth_map[y_min:y_max, x_min:x_max]
    median_depth = np.median(depth_roi)

    # FPS and Depth Value as Meters
    fps = cap.get(cv2.CAP_PROP_FPS)
    cv2.putText(rectangle, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(rectangle, f"Depth: {median_depth:.2f} m", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Depth", rectangle)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()