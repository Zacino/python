# encoding:utf-8
import time
import os
from PIL import Image
import cv2
import numpy as np

'''人为构造xml文件的格式'''
out0 = '''<annotation>
    <folder>%(folder)s</folder>
    <filename>%(name)s</filename>
    <path>%(path)s</path>
    <source>
        <database>None</database>
    </source>
    <size>
        <width>%(width)d</width>
        <height>%(height)d</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>
'''
out1 = '''    <object>
        <name>%(class)s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%(xmin)d</xmin>
            <ymin>%(ymin)d</ymin>
            <xmax>%(xmax)d</xmax>
            <ymax>%(ymax)d</ymax>
        </bndbox>
    </object>
'''

out2 = '''</annotation>
'''
'''txt转xml函数'''

def translate(fdir, lists,classes):
    print("---this is txt2xml---")
    source = {}
    label = {}
    if not os.path.exists(fdir+"/Annotations"):
        os.mkdir(fdir+"/Annotations")
    # os.system("cd "+fdir+"/Annotations;" + "sudo chown a:a *")
    for jpg in lists:
        # print("jpg:",jpg)
        zhui = jpg.split("/")[-1].split(".")[1]
        if os.path.exists(fdir + "/Txt/"+jpg.split("/")[-1].split(".")[0]+".txt"):
            if zhui == 'jpg' or zhui == 'png' or zhui == 'bmp' or zhui == 'jpeg':
                image = cv2.imread(jpg)  # 路径不能有中文
                h, w, _ = image.shape  # 图片大小
                fxml = jpg.replace('.'+zhui, '.xml').replace('JPEGImages', 'Annotations')
                print("fxml:", fxml)

                # os.system("sudo chmod 777 " + fdir + '/Annotations')
                fxml = open(fxml, 'w', encoding='utf-8')

                imgfile = jpg.split('/')[-1]
                source['name'] = imgfile
                source['path'] = jpg
                source['folder'] = os.path.basename(fdir)
                source['width'] = w
                source['height'] = h

                fxml.write(out0 % source)

                txt = fdir+"/Txt/"+jpg.split("/")[-1].replace('.'+zhui, '.txt')

                if os.path.exists(txt):
                    lines = np.loadtxt(txt)  # 读入txt存为数组
                    print("lines:",lines)
                    if len(np.array(lines).shape) == 1:
                        lines = [lines]
                    for box in lines:
                        # print(box.shape)
                        if box.shape != (5,):
                            box = lines

                        '''把txt上的第一列（类别）转成xml上的类别
                           我这里是labelimg标1、2、3，对应txt上面的0、1、2'''
                        for i in range(len(classes)):
                            if str(int(box[0])) == str(i):
                                label['class'] = classes[i]

                        '''把txt上的数字（归一化）转成xml上框的坐标'''
                        xmin = float(box[1] - 0.5 * box[3]) * w
                        ymin = float(box[2] - 0.5 * box[4]) * h
                        xmax = float(xmin + box[3] * w)
                        ymax = float(ymin + box[4] * h)

                        label['xmin'] = xmin
                        label['ymin'] = ymin
                        label['xmax'] = xmax
                        label['ymax'] = ymax
                        if os.path.exists(txt):
                            fxml.write(out1 % label)
                fxml.write(out2)

        else:
            pass
def to_xml(file_dir,classes):
    # os.system("sudo chmod 777 "+file_dir)
    lists = []
    classes = list(classes.split(","))
    file_dir0 = file_dir+"/JPEGImages/"
    for i in os.listdir(file_dir0):
        if i.split(".")[1] == 'jpg' or i.split(".")[1] == 'png' or i.split(".")[1] == 'bmp' or i.split(".")[1] == 'jpeg':
            lists.append(file_dir0 + '/' + i)
    translate(file_dir,lists,classes)

if __name__ == '__main__':
    """
    将图片和txt放在file_dir下的JPEGImages文件夹和Txt文件夹中，
    """
    file_dir = r'D:\wsj_3'
    classes = "_background_,people"
    # classes = "_background_,people,pa,zuo,cheng,tang,rsvd1,rsvd2"

    # classes = "people,headsh,helmet,nohelmet,mask,nomask,vest,novest"
    to_xml(file_dir,classes)
