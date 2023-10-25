
import numpy as np
import onnxruntime as rt
import cv2

import torch

# GPU
print("CUDA is available: ", torch.cuda.is_available())

class DepthEstimation:
    def __init__(self, model_path):
        self.sess = rt.InferenceSession(model_path)

    def predict(self, img):
        input_img = cv2.resize(img, (256, 192))
        input_img = np.transpose(input_img, (2, 0, 1))
        input_img = input_img.astype(np.float32) / 255.0
        input_img = np.expand_dims(input_img, axis=0)

        input_name = self.sess.get_inputs()[0].name
        outputs = self.sess.run(None, {input_name: input_img})

        depth = outputs[0].squeeze(0)
        if depth.shape[0] > 1:  # Multi-channel output
            depth = np.argmax(depth, axis=0)
        
        # Improved normalization
        depth = (depth - np.min(depth)) / (np.max(depth) - np.min(depth))
        depth = (depth * 255).astype(np.uint8)

        return depth

def main():
    model = './model.onnx'
    estimator = DepthEstimation(model)

    # Gstreamer Pipeline on Webcam
    cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! appsink")

    while cap.isOpened():
        ret, frame = cap.read()

        depth_map = estimator.predict(frame)

        print(np.min(depth_map), np.max(depth_map), np.mean(depth_map))

        depth_color = cv2.applyColorMap(depth_map, cv2.COLORMAP_PLASMA)

        cv2.imshow('Depth Map', depth_color)
        cv2.imshow('Original Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
