# encoding:utf-8
# 用于视频截图用

import glob
import os
import random
import math
import shutil
import cv2
import datetime
import re
from pathlib import Path
from PIL import Image

# 视频路径
# VIDEO_DIR = r"D:\Project\01_to_be_done\手机\video"
VIDEO_DIR = r"D:\ccgf"
# 每隔多少帧截一次
SNAP_INT = 10
# 截图存储路径, 不能有中文
SNAP_PATH = r"D:\c"

def remove_chinese_characters(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]+')  # 匹配中文字符的正则表达式
    new_text = re.sub(pattern, '', text)  # 替换中文字符为空字符串
    return new_text

def cal_frame(video_path):
    print(video_path)
    video = cv2.VideoCapture(video_path)
    # 获取视频帧数
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    # 打印帧数
    print("视频切出:", frame_count/SNAP_INT)
    # 释放视频资源
    video.release()



def snap_video(video_path, snap_path):
    fpath, fname = os.path.split(video_path)  # 分离文件名和路径ate_train_test_txt.py
    if not os.path.exists(fpath):
        os.makedirs(fpath)  # 创建路径
    # 获取前缀（文件名称）
    FILE_PREFIX = os.path.splitext(fname)[0]
    FILE_PREFIX = remove_chinese_characters(FILE_PREFIX)

    curr_time = datetime.datetime.now()
    time_str = curr_time.strftime("%Y%m%d")
    # 截图存储路径
    snap_path = snap_path + '/' + time_str + '/' + 'snap_' + FILE_PREFIX
    if not os.path.exists(snap_path):
        os.makedirs(snap_path)

    cap = cv2.VideoCapture(video_path)  #打开视频
    frame_cnt = 0
    jpg_cnt = 0
    while True:
        ret, frame = cap.read()  # 读取一帧视频
        # ret 读取了数据就返回True,没有读取数据(已到尾部)就返回False
        # frame 返回读取的视频数据--一帧数据
        if not ret:
            break
        if (frame_cnt % SNAP_INT) == 0:
            jpg_cnt += 1
            jpg_end = "%(datastr)s_%(fileprefix)s_%(num)05d.jpg"%{'datastr':time_str,'fileprefix':FILE_PREFIX,'num':jpg_cnt}
            print("jpg_end:",jpg_end)
            dst_jpg_file = snap_path + '//' + jpg_end

            # 重新保存大小
            pic = cv2.resize(frame, (1920, 1088), interpolation=cv2.INTER_CUBIC)

            # cv2.imwrite(dst_jpg_file, pic)
            cv2.imencode('.jpg', pic)[1].tofile(dst_jpg_file)

        frame_cnt += 1

    cap.release()  # 释放视频流
    return frame_cnt

if __name__ == '__main__':
    video_name = VIDEO_DIR + '/*.mp4'
    video_list_path = glob.glob(video_name)
    for videoitem in video_list_path:
        cal_frame(videoitem)
        snap_video(videoitem, SNAP_PATH)



