import os
import xml.etree.ElementTree as ET
# 递归函数，替换元素中文本内容中的'di'为'zuo'
def replace_di_with_zuo(elem):
    print("elem.text:",elem.text)
    if elem.text and 'sleep' in elem.text:
        elem.text = elem.text.replace('sleep', 'pa')
    for child in elem:
        replace_di_with_zuo(child)

if __name__ == '__main__':
    path = r'C:\Users\14234\Desktop\通用sleep\Annotations'
    save_path = r'C:\Users\14234\Desktop\通用sleep\Annotations_new'

    for file in os.listdir(path):
        xml_path = os.path.join(path, file)
        print("xml_path:",xml_path)
        new_xml_path = os.path.join(save_path, file)
        # 读取XML文件
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 遍历XML文件中的所有<name>标签，替换其中的'di'为'zuo'
        for name in root.iter('name'):
            replace_di_with_zuo(name)

        # 将替换后的XML文件写入新文件
        tree.write(new_xml_path)