import time
import cv2
import numpy as np
import onnxruntime as rt

class MobileUnet():
  def __init__(self, model_path):
    self.model = self.initialize_model(model_path)
    self.min_depth = np.inf
    self.max_depth = -np.inf

  def __call__(self, img):
    return self.estimate_depth(img)
  
  def initialize_model(self, model_path):
    self.sess = rt.InferenceSession(model_path, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    self.get_input_details()
    self.get_output_details()

  def estimate_depth(self, img):
    input_tensor = self.prepare_input(img)
    outputs = self.inference(input_tensor)
    self.depth_map = self.process_output(outputs)

    return self.depth_map
  
  def prepare_input(self, img):
    self.img_height, self.img_width = img.shape[:2]

    img_input = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_input = cv2.resize(img_input, (self.input_width, self.input_height), interpolation=cv2.INTER_AREA) /255.0
    img_input = img_input.transpose(2, 0, 1)

    return img_input[np.newaxis, :, :, :].astype(np.float32)
  
  def inference(self, input_tensor):
    start = time.time()
    outputs = self.sess.run(self.output_names, {self.input_names[0]: input_tensor})[0]
    print(time.time(), start)
    return outputs
  
  def process_output(self, outputs):
    return np.squeeze(outputs)
  
  def draw_depth(self):
    min_depth = self.depth_map.min()
    max_depth = self.depth_map.max()
    self.min_depth = min_depth if min_depth < self.min_depth else self.min_depth
    self.max_depth = max_depth if max_depth > self.max_depth else self.max_depth

    # print(self.min_depth, self.max_depth)
    norm_depth = 255 * (self.depth_map - self.min_depth) / (self.max_depth - self.min_depth)
    norm_depth = 255 - norm_depth

    color_depth = cv2.applyColorMap(norm_depth.astype(np.uint8), cv2.COLORMAP_PLASMA)

    return cv2.resize(color_depth, (self.input_width, self.input_height))
  
  def get_input_details(self):
    model_inputs = self.sess.get_inputs()
    self.input_names = [model_inputs[i].name for i in range(len(model_inputs))]

    self.input_shape = model_inputs[0].shape
    self.input_height = self.input_shape[2]
    self.input_width = self.input_shape[3]

  def get_output_details(self):
    model_outputs = self.sess.get_outputs()
    self.output_names = [model_outputs[i].name for i in range(len(model_outputs))]

    self.output_shape = model_outputs[0].shape
    self.output_height = self.output_shape[2]
    self.output_width = self.output_shape[3]