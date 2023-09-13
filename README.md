# This is a Monocular Depth Estimation Model on Jetson TX2 NX using TensorRT.

## Introduction
This is a Monocular Depth Estimation Model on Jetson TX2 NX using TensorRT. The model is based on U-Net and MobileNetV3 architecture and trained on DIODE Indoor Dataset. The model is converted from tensorflow to onnx and then to TensorRT engine. The model is tested on Jetson TX2 NX and the inference time is currently TBD.

## Jetson TX2 NX Setup
1. Install Jetpack 4.6.* on Jetson TX2 NX via custom install method. Please refer to [this](https://docs.nvidia.com/sdk-manager/install-with-sdkm-jetson/index.html) for more details.
2. Download and install the components needed using the following commands:
```
sudo apt-get install nvidia-jetpack
```
3. Build OpenCV with CUDA support. Please refer to [this](https://github.com/JetsonHacksNano/buildOpenCV).

## This Repository is Under Construction and Will be Updated Soon