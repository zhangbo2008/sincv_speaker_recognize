#!/usr/bin/env python3

# TIMIT_preparation 
# Mirco Ravanelli 
# Mila - University of Montreal 

# July 2018

# Description: 
# This code prepares TIMIT for the following speaker identification experiments. 
# It removes start and end silences according to the information reported in the *.wrd files and normalizes the amplitude of each sentence.

# How to run it:
# python TIMIT_preparation.py $TIMIT_FOLDER $OUTPUT_FOLDER data_lists/TIMIT_all.scp 

# NOTE: This script expects filenames in lowercase (e.g, train/dr1/fcjf0/si1027.wav" rather than "TRAIN/DR1/FCJF0/SI1027.WAV)
# 对timit数据进行说明.读的都是英文,数据里面train 里面文件夹里面每一个文件夹代表一个方言accent,从dr1到dr8然后, 每一个文件夹里面有Fxxx代表一个女人一个Mxxx代表一个男人.文件夹里面表示这个人说的话.
# 每一个语音有4个文件组成 .wav   .phn   .txt  .wav
# wav是语音,  phn是 每一个音速的开始帧和结束帧,音速是什么         wrd是每一个单词的开始帧,结束帧,单词是什么.
# 更具体的可以查看数据集里面的README.DOC

import nbconvert.exporters.base

# ===========下面的预处理, 把文件里面的语音, 只抽取里面带语音的部分,空白部分删除.
import shutil
import os
import soundfile as sf
import numpy as np
import sys

#=============读取文件列表
def ReadList(list_file):
    f = open(list_file, "r")
    lines = f.readlines()
    list_sig = []
    for x in lines:
        list_sig.append(x.rstrip())
    f.close()
    return list_sig

# 只拷贝目录结构,不拷贝里面文件.
def copy_folder(in_folder, out_folder):
    if not (os.path.isdir(out_folder)):
        shutil.copytree(in_folder, out_folder, ignore=ig_f)

# 找到所有的文件名
def ig_f(dir, files):
    return [f for f in files if os.path.isfile(os.path.join(dir, f))]


in_folder = 'TIMIT'
out_folder = 'TIMIT_after_preparation'
list_file = 'data_lists/TIMIT_all.scp'

# Read List file
list_sig = ReadList(list_file)
list_sig = [i.upper() for i in list_sig]

# Replicate input folder structure to output folder
copy_folder(in_folder, out_folder)

# Speech Data Reverberation Loop
for i in range(len(list_sig)):
    # Open the wav file
    wav_file = in_folder + '/' + list_sig[i]
    [signal, fs] = sf.read(wav_file)
    signal = signal.astype(np.float64)

    # Signal normalization
    signal = signal / np.max(np.abs(signal))

    # Read wrd file
    wrd_file = wav_file.replace(".WAV", ".WRD")
    wrd_sig = ReadList(wrd_file)
    beg_sig = int(wrd_sig[0].split(' ')[0])
    end_sig = int(wrd_sig[-1].split(' ')[1])

    # Remove silences
    signal = signal[beg_sig:end_sig]

    # Save normalized speech
    file_out = out_folder + '/' + list_sig[i]

    sf.write(file_out, signal, fs)

    print("Done %s" % (file_out))
