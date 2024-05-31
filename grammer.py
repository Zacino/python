import torch
from torch.utils.data import DataLoader
import pandas as pd


# python 列表[]  元组()  字典{} k-v
# 元组的元素不能修改，但可以对元组连接组合；元组的元素值也不能删除，只能删除整个元组

a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# python 索引   a[index]
# index    0 1 2 ... 9      -10 -9 -8 ... -1
# 在基本索引中，超出有效范围会抛出IndexError


# python 切片   a[start:stop]   左闭右开
# print(a[2:5])   [2, 3, 4]
# print(a[5:-1])   [5, 6, 7, 8]
# 超出有效范围 和 缺省
# 超出有效范围进行截断  a[-100:3] = a[-10:3]     a[0:100] = a[0:10]  如果start>stop 空
# 缺省的一项默认取最大区间 a[1:] = a[1:10]  a[10:] = 空


# python 扩展切片   a[start:stop:step] step非零整数，含义为步长 普通切片step=1
# step为正数 同上   a[:-2:2]  [0, 2, 4, 6] step为负数 从start出发以步长|step|逆序索引序列
# 截断依就，但缺省发生一点变化 start缺省为无穷大，stop为无穷小 a[5::-1] [5, 4, 3, 2, 1, 0]


# python 多层列表切片
# print(a[2:5][1:3][-1:])  [2:5] = [2, 3, 4]  然后[1:3]是在上一步结果中运行 [2:5][1:3] = [3, 4]


# 语法 lambda arguments: expression
# arguments 是参数列表，可以包含零个或多个参数，但必须在冒号(:)前指定。
# expression 是一个表达式，用于计算并_返回_函数的结果。
add = lambda x, y: x+y  # add(2,3)

# 高阶函数用法
# map(function, iterable, ...) function->函数   iterable->一个或多个序列
# 返回值：
# Python 2.x 版本返回的是列表
# Python 3.x 版本返回的是迭代器
c_lambda_map = map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10])  # list(c) 结果：[3, 7, 11, 15, 19]


# ！！python3 不支持
# apply(func,*args,**kwargs)             function(a,b)
# args是一个包含按照函数所需参数传递的位置参数的一个元组 apply(function, ('good','better'))
# kwargs是一个包含关键字参数的字典，而其中args如果不传递，kwargs需要传递，则必须在args的位置留空。
# apply(function,('cai'), {'b':'caiquan'})   ('cai', 'caiquan')
# apply(function, (), {'a':'caiquan', 'b':'Tom'})  ('caiquan', 'Tom')
# **kwargs 也可用a=1， b=2   apply(function, (), a=1, b=2)
