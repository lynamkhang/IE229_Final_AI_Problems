# -*- coding: utf-8 -*-
"""Final AI - Excercise 1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_nB6X9WsGXaVkf6TiKRae8ZqE0E9I6b3

# Problem 1: Write a program (PyTorch) that achieves higher accuracy on the CIFAR-10 data set. The program should be an improved version of the program in the 10th lecture (or the program you wrote in Lab Work (4)). Submit the “Program”, its “Execution Results”, and an “Explanation” of them in a word file.  Also submit the source code (.py) of the program.
"""

import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
import torchvision as tv

train_dataset = tv.datasets.CIFAR10(root="./", train=True,
transform=tv.transforms.ToTensor(), download=True)

test_dataset = tv.datasets.CIFAR10(root="./", train=False,
transform=tv.transforms.ToTensor(), download=True)

train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
batch_size=100, shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
batch_size=100, shuffle=False)

MODELNAME = "cifar10.model"
EPOCH = 20
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class VGG16(torch.nn.Module):
    def __init__(self):
        super(VGG16, self).__init__()
        self.layer1 = torch.nn.Sequential(
            torch.nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(64),
            torch.nn.ReLU())
        self.layer2 = torch.nn.Sequential(
            torch.nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(64),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size = 2, stride = 2))
        self.layer3 = torch.nn.Sequential(
            torch.nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(128),
            torch.nn.ReLU())
        self.layer4 = torch.nn.Sequential(
            torch.nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(128),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size = 2, stride = 2))
        self.layer5 = torch.nn.Sequential(
            torch.nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(256),
            torch.nn.ReLU())
        self.layer6 = torch.nn.Sequential(
            torch.nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(256),
            torch.nn.ReLU())
        self.layer7 = torch.nn.Sequential(
            torch.nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(256),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size = 2, stride = 2))
        self.layer8 = torch.nn.Sequential(
            torch.nn.Conv2d(256, 512, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(512),
            torch.nn.ReLU())
        self.layer9 = torch.nn.Sequential(
            torch.nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(512),
            torch.nn.ReLU())
        self.layer10 = torch.nn.Sequential(
            torch.nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(512),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size = 2, stride = 2))
        self.layer11 = torch.nn.Sequential(
            torch.nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(512),
            torch.nn.ReLU())
        self.layer12 = torch.nn.Sequential(
            torch.nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(512),
            torch.nn.ReLU())
        self.layer13 = torch.nn.Sequential(
            torch.nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            torch.nn.BatchNorm2d(512),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size = 2, stride = 2))
        self.fc = torch.nn.Sequential(
            torch.nn.Dropout(0.5),
            torch.nn.Linear(512 * 7 * 7, 512),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.5),
            torch.nn.Linear(512, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, 10))

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)
        out = self.layer6(out)
        out = self.layer7(out)
        out = self.layer8(out)
        out = self.layer9(out)
        out = self.layer10(out)
        out = self.layer11(out)
        out = self.layer12(out)
        out = self.layer13(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        return out

def train():
  model = VGG16().to(DEVICE)
  optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
  for epoch in range(EPOCH):
   loss = 0
   for images, labels in train_loader:
    images = images.view(-1,3,32,32).to(DEVICE)
    labels = labels.to(DEVICE)
    optimizer.zero_grad()
    y = model(images)
    batchloss = F.cross_entropy(y,labels)
    batchloss.backward()
    optimizer.step()
    loss = loss + batchloss.item()
   print("epoch", epoch, ": loss", loss)
  torch.save(model.state_dict(),MODELNAME)

def test():
    total = len(test_loader.dataset)
    correct = 0
    model = VGG16().to(DEVICE)
    model.load_state_dict(torch.load(MODELNAME))
    model.eval()
    for images, labels in test_loader:
        images = images.view(-1,3,32,32).to(DEVICE)
        labels = labels.to(DEVICE)
        y = model(images)
        pred_labels = y.argmax(dim=1)
        correct += (pred_labels == labels).sum().item()

    print("correct: ", correct)
    print("total: ", total)
    print("accuracy: ", correct / float(total))

train()

test()