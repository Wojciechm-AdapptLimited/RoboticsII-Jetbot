import sys

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchsummary import summary

import tqdm

# class ConvolutionalModel(nn.Module):
#     def __init__(self,input_size=224):
#         super(ConvolutionalModel, self).__init__()

#         conv_params = [3,8,16,32,64]

#         self.convs = []
#         for a,b in zip(conv_params[:-1],conv_params[1:]):
#             self.convs.append(nn.Conv2d(a,b,kernel_size=5))
        
#         linear_params = [10*10*64,64,2]
#         self.linears = []
#         for a,b in zip(linear_params[:-1],linear_params[1:]):
#             self.linears.append(nn.Linear(a,b))
#         self.output = self.linears.pop(-1)

#     def forward(self,x):

#         for conv in self.convs:
#             x = F.relu(F.max_pool2d(conv(x),2))
#         x = x.view(-1,10*10*64)
#         for lin in self.linears:
#             x = F.relu(lin(x))
#         return F.tanh(x)

def create_model():
    layers = []
    conv_params = [3,8,16,32,64]
    for a,b in zip(conv_params[:-1],conv_params[1:]):
        layers.append(nn.Conv2d(a,b,kernel_size=5))
        layers.append(nn.ReLU())
        layers.append(nn.MaxPool2d(2))
    layers.append(nn.Flatten())
    linear_params = [10*10*64,64,2]
    out = linear_params.pop(-1)
    for a,b in zip(linear_params[:-1],linear_params[1:]):
        layers.append(nn.Linear(a,b))
        layers.append(nn.ReLU())

    layers.append(nn.Linear(linear_params[-1],out))
    layers.append(nn.Tanh())

    return nn.Sequential(*layers)

def training_loop(model,train_dataloader,epochs=10,loss=nn.L1Loss,optimizer=optim.SGD,optimizer_params=[]):
    criterion = loss()
    optimizer = optimizer(*optimizer_params)
    for epoch in tqdm(range(epochs)):
        model.train()
        for i, (X,y) in enumerate(train_dataloader):
            optimizer.zero_grad()
            outputs = model(X)
            loss = criterion(outputs,y)
            loss.backward()
            optimizer.step()
            loss += loss.item()

def main(*argv):
    train_transform = transforms.Compose([
        transforms.RandomRotation(10),
        transforms.ToTensor(),        
        transforms.GaussianBlur(5, sigma=(0.1, 2.0)),        
        transforms.Normalize((0.1307,), (0.3081,)) 
    ])
    model = create_model()
    summary(model,(3,224,224))

    return 0

if __name__ == "__main__":
    main(*sys.argv)