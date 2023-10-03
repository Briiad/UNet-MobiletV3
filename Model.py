
import torch
import torch.nn as nn
import torchvision.models as models

class MobileNetV3Encoder(nn.Module):
    def __init__(self, pretrained=True):
        super(MobileNetV3Encoder, self).__init__()
        mobilenet = models.mobilenet_v3_small(pretrained=pretrained)
        self.features = mobilenet.features

    def forward(self, x):
        # Extract features from different layers of MobileNetV3
        features = []
        for i, layer in enumerate(self.features):
            x = layer(x)
            if i in [1, 3, 6, 11, 13]:
                features.append(x)
        return features

class UNetDecoder(nn.Module):
    def __init__(self):
        super(UNetDecoder, self).__init__()

        # Define the upsampling layers
        self.up1 = self._upsample_block(64, 128)
        self.up2 = self._upsample_block(64, 64)
        self.up3 = self._upsample_block(32, 64)
        self.up4 = self._upsample_block(16, 32)
        self.final_conv = nn.Conv2d(16, 1, kernel_size=1)

    def _upsample_block(self, in_channels, out_channels):
        block = nn.Sequential(
            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.ReLU(inplace=True)
        )
        return block

    def forward(self, features):
        x1, x2, x3, x4, x5 = features
        d1 = self.up1(x5)
        d2 = self.up2(d1 + x4)
        d3 = self.up3(d2 + x3)
        d4 = self.up4(d3 + x2)
        out = self.final_conv(d4 + x1)
        return out

class UNet(nn.Module):
    def __init__(self, pretrained=True):
        super(UNet, self).__init__()
        self.encoder = MobileNetV3Encoder(pretrained)
        self.decoder = UNetDecoder()

    def forward(self, x):
        features = self.encoder(x)
        out = self.decoder(features)
        return out

model = UNet()
