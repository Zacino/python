
import numpy as np
import pandas as pd
import torch
from torch import nn
from d2l import torch as d2l
from download import download


train_data = pd.read_csv(download('kaggle_house_train'))
test_data = pd.read_csv(download('kaggle_house_test'))


print(train_data.iloc[0:4, [0, 1, 2, 3, -3, -2, -1]])

