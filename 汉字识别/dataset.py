import glob
from torchvision import transforms
from torch.utils.data import Dataset
from PIL import Image
import os
from utils import random_split

data_dir = './dataset/'
class_names = os.listdir(data_dir)
num_class = len(class_names)
image_files = glob.glob(data_dir + '*/*.jpg', recursive=True)
image_num = len(image_files)

idx_to_class = {i: j for i, j in enumerate(class_names)}
class_to_idx = {value: key for key, value in idx_to_class.items()}

train_data_path, test_data_path = random_split(image_files, [0.8, 0.2])


class WordImageDataset(Dataset):
    def __init__(self, image_paths, transform=None):
        self.image_paths = image_paths
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        image = Image.open(image_path)

        label = image_path.split('\\')[-2]
        label = class_to_idx[label]

        if self.transform is not None:
            image = self.transform(image)

        return image, label


def get_dataset():
    train_dataset = WordImageDataset(train_data_path, transform=transforms.ToTensor())
    test_dataset = WordImageDataset(test_data_path, transform=transforms.ToTensor())
    return train_dataset, test_dataset


if __name__ == '__main__':
    train_dataset, _ = get_dataset()
    print(train_dataset[0][0][0].numpy())
    image = Image.fromarray(train_dataset[0][0][0].numpy()*255).convert('L')
    image.show()

