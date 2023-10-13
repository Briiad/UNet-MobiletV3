import torch.nn as nn
import segmentation_models_pytorch as smp

class Model(nn.Module):
    def __init__(self,):
        super().__init__()
        self.model = smp.UnetPlusPlus(
            # MobileNetV3 Small with pretrained weights
            encoder_name="timm-mobilenetv3_large_100",
            encoder_weights="imagenet",
            in_channels=3,
            classes=1,
            # activation function for the output of the network ()
            activation="linear",
        )

    def forward(self, x):
        return self.model(x)
    
    def _num_params(self,):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)