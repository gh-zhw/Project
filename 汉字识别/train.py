import torch
from torch import nn
from torch.utils.data import DataLoader
from model import CNN
from dataset import get_dataset


input_shape = 28
input_channel = 1
num_classes = 8

batch_size = 4
num_epoch = 5
learning_rate = 1e-3

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


train_dataset, test_dataset = get_dataset()

train_dataloader = DataLoader(
    dataset=train_dataset,
    shuffle=True,
    batch_size=batch_size
)
test_dataloader = DataLoader(
    dataset=test_dataset,
    shuffle=False,
    batch_size=batch_size
)


model = CNN(input_shape, input_channel, num_classes).to(device)

loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)


total_batch = len(train_dataloader)

# train
model.train()
for epoch in range(num_epoch):
    for batch_idx, (images, labels) in enumerate(train_dataloader):
        images = images.to(device)
        labels = labels.to(device)

        out = model(images)
        loss = loss_fn(out, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (batch_idx+1) % 5 == 0:
            print(f'epoch {epoch+1}/{num_epoch}, {batch_idx+1}/{total_batch}, loss: {loss.item():.4f}')

# test
model.eval()
total = 0
correct = 0
with torch.no_grad():
    for images, labels in test_dataloader:
        images = images.to(device)
        labels = labels.to(device)

        out = model(images)
        preds = torch.argmax(out, dim=1)

        total += images.size(0)
        correct += (preds == labels).sum().item()
test_acc = correct/total
print(f'test_acc: {correct}/{total}={test_acc}')


torch.save(model.state_dict(), f'./model/model_acc_{test_acc}.pth')
