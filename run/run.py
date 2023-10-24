import cv2
import torch
import torchvision.transforms as transforms
import numpy as np

# Load the PyTorch model
model = torch.load("path_to_your_model.pth")
model.eval()

# If you have CUDA support, use the GPU for inference
if torch.cuda.is_available():
    model = model.cuda()

# Define the preprocessing steps
preprocess = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((192, 256)),  # Define the desired input size
    transforms.ToTensorV2(),
    # Add any other preprocessing steps your model requires
])

# Define the postprocessing steps
postprocess = transforms.Compose([
    # Add any preprocessing steps your model requires
    transforms.ToPILImage(),
    transforms.Resize((192, 256)),  # Define the desired output size
    transforms.ToTensorV2()  # Converts PIL Image to numpy array
])

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Preprocess the frame
    input_tensor = preprocess(frame).unsqueeze(0)
    if torch.cuda.is_available():
        input_tensor = input_tensor.cuda()

    # Predict depth
    with torch.no_grad():
        depth_map = model(input_tensor)

    # Convert depth map tensor to numpy for visualization
    depth_map_np = depth_map.squeeze().cpu().numpy()

    # Post-process the depth map if necessary (color mapping, resizing back, etc.)
    visualized_depth = postprocess(depth_map_np)  # Define this function based on your visualization needs

    # Display the results
    cv2.imshow('Depth Map', visualized_depth)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()