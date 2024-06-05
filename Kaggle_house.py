
import numpy as np
import pandas as pd
import torch
from torch import nn
from d2l import torch as d2l
from download import download


train_data = pd.read_csv(download('kaggle_house_train'))
test_data = pd.read_csv(download('kaggle_house_test'))

# panda loc：通过行、列的名称或标签来索引 iloc：通过行、列的索引位置来寻找数据
# df.loc[row_label, col_label] 其中，row_label可以是单个标签、标签列表或切片
# df.iloc[row_index, col_index] row_index可以是单个索引、索引列表或切片，用于定位行
# print(train_data.loc[1, 'Id'])  行标签是1
print(train_data.iloc[0:4, [0, 1, 2, 3, -3, -2, -1]])

# pd.concat()函数可以沿着指定的轴将多个dataframe或者series拼接到一起。行方向axis=0
all_features = pd.concat((train_data.iloc[:, 1:-1], test_data.iloc[:, 1:]))

# 将所有缺失的值替换为相应特征的平均值。
# 然后，为了将所有特征放在一个共同的尺度上， 我们通过将特征重新缩放到零均值和单位方差来标准化数据：
# 若无法获得测试数据，则可根据训练数据计算均值和标准差
# numpy中区分string和object panda中没有这种区别
# all_features.dtypes获取每一列数据类型并返回   != 'object' 不为object对象返回true
print(all_features.dtypes[all_features.dtypes != 'object'])
numeric_features = all_features.dtypes[all_features.dtypes != 'object'].index
all_features[numeric_features] = (all_features[numeric_features].apply(
    lambda x: (x - x.mean()) / (x.std())))
# 在标准化数据之后，所有均值消失，因此我们可以将缺失值设置为0
all_features[numeric_features] = all_features[numeric_features].fillna(0)

# 处理离散值。 这包括诸如“MSZoning”之类的特征。 我们用独热编码替换它们
# “Dummy_na=True”将“na”（缺失值）视为有效的特征值，并为其创建指示符特征
all_features = pd.get_dummies(all_features, dummy_na=True)

# 通过values属性,dataframe的values，我们可以 从pandas格式中提取NumPy格式，并将其转换为张量表示用于训练。
# 每一行数据就是一个样本
n_train = train_data.shape[0]
# 为什么使用numpy  python list中保存的是对象指针，对于数值运算很低效
train_features = torch.tensor(all_features[:n_train].values, dtype=np.float32)
test_features = torch.tensor(all_features[n_train:].values, dtype=np.float32)
# reshape 为-1时是让系统主动计算
train_labels = torch.tensor(train_data.SalePrice.values.reshape(-1, 1), dtype=np.float32)


"""
    训练
"""

loss = nn.MSELoss()  # l2损失 均方误差  1/n求和（y-y'）^2
in_features = train_features.shape[1]


def get_net():
    net = nn.Sequential(nn.Linear(in_features,1))


# 均方根误差
def log_rmse(net, features, labels):
    # 为了在取对数时进一步稳定该值，将小于1的值设置为1
    #  torch.clamp(input, min, max, out=None) 输入input张量每个元素的范围限制到区间 [min,max]
    # float('inf') 正无穷
    clipped_preds = torch.clamp(net(features), 1, float('inf'))
    rmse = torch.sqrt(loss(torch.log(clipped_preds), torch.log(labels)))
    return rmse.item()  # .item()用于在只包含一个元素的tensor中提取值 否则的话使用.tolist()


def train(net, train_features, train_labels, test_features, test_labels,
          num_epochs, learning_rate, weight_decay, batch_size):
    train_ls, test_ls = [], []
    train_iter = d2l.load_array((train_features, train_labels), batch_size)
    # 这里使用的是Adam优化算法
    optimizer = torch.optim.Adam(net.parameters(),
                                 lr = learning_rate,
                                 weight_decay = weight_decay)
    for epoch in range(num_epochs):
        for X, y in train_iter:
            optimizer.zero_grad()
            l = loss(net(X), y)
            l.backward()
            optimizer.step()
        train_ls.append(log_rmse(net, train_features, train_labels))
        if test_labels is not None:
            test_ls.append(log_rmse(net, test_features, test_labels))
    return train_ls, test_ls
