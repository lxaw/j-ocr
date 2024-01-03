import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class OcrCNN(nn.Module):
    def __init__(self,inch,outch,k_size,stride,padding,num_classes):
        super(OcrCNN,self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(
                in_channels = inch,
                out_channels = outch,
                kernel_size = k_size,
                stride = stride,
                padding = padding,
            ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(
                in_channels =outch,
                out_channels = 32,
                kernel_size = k_size,
                stride = stride,
                padding = padding,
            ),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        # output to some class
        self.out = nn.Linear([TODO],num_classes)
    
    def forward(self,x):
        x = self.conv1(x)
        x = self.conv2(x)
        # flatten the output of conv2 to (batch_size, 32 * 7 * 7)
        x = x.view(x.size(0),-1)
        output = self.out(x)

        return output

