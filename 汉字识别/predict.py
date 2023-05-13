import torch
from PIL import Image
from torchvision import transforms
from model import CNN
from dataset import idx_to_class


input_shape = 28
input_channel = 1
num_classes = 8

model = CNN(input_shape, input_channel, num_classes)
model.load_state_dict(torch.load('./model/model_acc_1.0.pth'))

image = Image.open('./dataset/周/0.jpg')
transform = transforms.ToTensor()
image = transform(image).unsqueeze(0)

output = model(image)
pred = torch.argmax(output).item()
print(idx_to_class[pred])

