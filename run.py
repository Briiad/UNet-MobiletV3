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
    x_max, y_max = WIDTH - x_min, HEIGHT - y_min

    rectangle = cv2.rectangle(color_depth, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    # Get Depth Value from Bounding Box
    depth_roi = depth_map[y_min:y_max, x_min:x_max]
    depth = np.mean(depth_roi)

    # FPS and Depth Value as Meters
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Font size is 8
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(rectangle, "FPS: {:.2f}".format(fps), (10, 20), font, 0.5, (0, 255, 0), 2)
    cv2.putText(rectangle, "Depth: {:.2f} m".format(depth), (10, 40), font, 0.5, (0, 255, 0), 2)

    cv2.imshow("Depth", rectangle)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()