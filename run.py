import numpy as np
import onnxruntime as rt
import cv2
from PIL import Image

import torch

# GPU
print("CUDA is available: ", torch.cuda.is_available())

def preprocess(path, input_size=(256, 192), mean=[0.485, 0.485, 0.485], std=[0.229, 0.229, 0.229]):
    img = Image.open(path)
    img = img.resize(input_size)

    img_np = np.array(img) / 255.0
    img_np = (img_np - mean) / std

    tensor = np.transpose(img_np, (2, 0, 1))
    tensor = np.expand_dims(tensor, axis=0).astype(np.float32)

    return tensor

def infer_depth(model_path, input_tensor):
    sess = rt.InferenceSession(model_path)

    input_name = sess.get_inputs()[0].name

    outputs = sess.run(None, {input_name: input_tensor})

    return outputs[0]

def main():
    model = './model.onnx'

    # Gstreamer Pipeline on Webcam
    cap = cv2.VideoCapture("v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! appsink")

    while cap.isOpened():
        ret, frame = cap.read()

        input_tensor = preprocess(frame)

        depth = infer_depth(model, input_tensor)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()