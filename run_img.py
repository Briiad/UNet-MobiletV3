import numpy as np
import onnxruntime as rt
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse
from PIL import Image

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

def visualize(depth, img_path):
    depth = np.squeeze(depth)
    depth_normalized = (depth - np.min(depth)) / (np.max(depth) - np.min(depth))
    depth_color = cm.plasma(depth_normalized)
    
    img = Image.open(img_path)
    img = img.resize((256, 192))

    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title('Image')

    plt.subplot(1, 2, 2)
    plt.imshow(depth_color)
    plt.title('Depth')

    # Save the figure
    plt.savefig('result.png')

def main():
    model_path = './model.onnx'

    # Args parse for image path
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True)
    args = parser.parse_args()

    input_tensor = preprocess(args.input_path)
    depth = infer_depth(model_path, input_tensor)

    visualize(depth, args.input_path)

if __name__ == '__main__':
    main()