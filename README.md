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

## Environment Setup
1. Install MiniForge at [here](https://github.com/conda-forge/miniforge/releases)
2. Set powershell to run as administrator and run the following commands:
```powershell
conda init powershell
Set-ExecutionPolicy unrestricted
conda config --set auto_activate_base false
```
3. Create a new conda environment
```conda
conda create -n <env_name> python=3.7
```
If you make the env inside vscode,
```conda
conda create --prefix .conda python=3.7
```
4. Activate the environment
```conda
conda activate <env_name>
```
5. Install the torch, dont forget to check the versions from [here](https://pytorch.org/get-started/previous-versions/)
```conda
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.6 -c pytorch -c nvidia
```
6. Install torchmetrics
```conda
conda install -c conda-forge torchmetrics
```
7. Install other dependencies
```pip
pip install -r requirements.txt
```