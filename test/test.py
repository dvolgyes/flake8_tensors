#!/usr/bin/env python3
import torch
import torch.nn
import torch.nn.functional



class Layer(torch.nn.Module):

    def __init__(self):
        super().__init__()

        self.shuffle = nn.PixelShuffle()
        self.concat = Concatenate()
        self.instancenorm = torch.nn.InstanceNorm2d()
        self.instancenorm = torch.nn.InstanceNorm2d(affine=True)
        self.maxpool = MaxPool3d()
        self.dropout = DropOut3d()
        x = torch.nn.functional.maxpool1d(...)

    def nested(self):

        class Nested():
            pass

        def nested_function():
            pass

import numpy as np

x=np.arange(100)
y=np.arange(100)
q=x.clone()

np.nansum(x)
z = x @ y

x=torch.arange(50)
x=x.reshape(5,-1)
x=x.view(5,-1)
x=x.permute(1,0)
np.tile(...)
np.repeat(...)
torch.repeat(...)
x.einsum(...)
x.matmul(...)

# losses
categorical_crossentropy(x)
F.categorical_crossentropy(x)
nn.Linear()
Dense()
Adam(...)
SGD(...)
torch.nn.CrossEntropyLoss(...)
numpy.nansum(...)
np.any(np.isnan(x))
np.any(np.any(x))
np.isnan(np.any(x))
np.all(numpy.isnan(x))
np.sum(x[np.isnan(x)])
mask=np.isnan(x)
x.detach()
x.cpu()
nonbase.x.cpu()
