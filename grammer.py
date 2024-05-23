import torch
from torch.utils.data import DataLoader


torch.log(1,2)

class MyDataLoader(torch.utils.data.Dataset):
    def __init__(self, data, label):
        self.data = data
        self.label = label

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item) :
        return self.data[item], self.label[item]
