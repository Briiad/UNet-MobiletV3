import cv2
import numpy as np
import onnxruntime as ort

# Load the ONNX model
session = ort.InferenceSession('model.onnx')

# Define the input and output names
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
  # Capture frame-by-frame
  ret, frame = cap.read()

  # Preprocess the input image
  img = cv2.resize(frame, (224, 224))
  img = img.astype(np.float32)
  img = img / 255.0
  img = np.transpose(img, (2, 0, 1))
  img = np.expand_dims(img, axis=0)

  # Run the inference
  pred = session.run([output_name], {input_name: img})[0]

  # Postprocess the output
  pred = np.squeeze(pred)
  pred = np.argmax(pred, axis=0)
  pred = pred.astype(np.uint8)

  # Display the output
  cv2.imshow('Output', pred)

  # Exit on ESC
  if cv2.waitKey(1) == 27:
    break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
