import os

# 遍历更改文件名
name = 2024052200001
num = 199811
for i in range(143):
    c = num + i
    a = format(c, "d") + '\\'
    path_ = os.path.join(r"D:\cc", a)
    print(path_)
    for file in os.listdir(path_):
        os.rename(os.path.join(path_, file), os.path.join(path_, str(name)) + ".jpg")
        name = name + 1


# old = r"D:\cc"
#
# for file in os.listdir(old):
#     os.rename(os.path.join(old, file), os.path.join(old, str(num)))
#     num = num + 1