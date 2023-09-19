import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models

# The Model used for the project are MobileNetV3 as the encoder and UNet as the decoder
class UpSample(nn.Sequential):
    def __init__(self, skip_input, output_features):
        super(UpSample, self).__init__()
        self.conv1 = nn.Conv2d(skip_input, output_features, kernel_size=3, padding=1, stride=1)
        self.leaky1 = nn.LeakyReLU(0.2)
        self.conv2 = nn.Conv2d(output_features, output_features, kernel_size=3, padding=1, stride=1)
        self.leaky2 = nn.LeakyReLU(0.2)

    def forward(self, x, concat_with):
        x = F.interpolate(x, size=[concat_with.size()[2], concat_with.size()[3]], mode='bilinear', align_corners=True)
        return self.leaky2(self.conv2(self.leaky1(self.conv1(torch.cat([x, concat_with], dim=1)))))

# Encoder
class MobileNetV3(nn.Module):
    def __init__(self):
        super(MobileNetV3, self).__init__()
        self.model = models.mobilenet_v3_small(pretrained=True)

    def forward(self, x):
        features = [x]
        for k, v in self.model.features._modules.items():
            features.append(v(features[-1]))
        return features

# Decoder
class UNet(nn.Module):
    def __init__(self, num_features=1280, decoder_width=0.6):
        super(UNet, self).__init__()
        features = int(num_features * decoder_width)

        self.conv1 = nn.Conv2d(num_features, features, kernel_size=3, padding=1, stride=1)

        self.Up0 = UpSample(skip_input=features // 1 + 320, output_features=features // 2)
        self.Up1 = UpSample(skip_input=features // 2 + 160, output_features=features // 2)
        self.Up2 = UpSample(skip_input=features // 2 + 64, output_features=features // 4)
        self.Up3 = UpSample(skip_input=features // 4 + 32, output_features=features // 8)
        self.Up4 = UpSample(skip_input=features // 8 + 24, output_features=features // 8)
        self.Up5 = UpSample(skip_input=features // 8 + 16, output_features=features // 16)

        self.conv2 = nn.Conv2d(features // 16, 1, kernel_size=3, padding=1, stride=1)

    def forward(self, features):
        x_block0 = features[2]
        x_block1 = features[4]
        x_block2 = features[6]
        x_block3 = features[9]
        x_block4 = features[15]
        x_block5 = features[18]
        x_block6 = features[19]

        x_d0 = self.conv1(x_block6)
        x_d1 = self.Up0(x_d0, x_block5)
        x_d2 = self.Up1(x_d1, x_block4)
        x_d3 = self.Up2(x_d2, x_block3)
        x_d4 = self.Up3(x_d3, x_block2)
        x_d5 = self.Up4(x_d4, x_block1)
        x_d6 = self.Up5(x_d5, x_block0)

        return self.conv2(x_d6)
    
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.encoder = MobileNetV3()
        self.decoder = UNet()

    def forward(self, x):
        return self.decoder(self.encoder(x))