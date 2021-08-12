#转化原始的timit数据到可以播放的wav文件. 用法, 设置好path即可.注意转化之后的后缀变成了_wav.

import params as hp
from sphfile import SPHFile
import glob
import os

if __name__ == "__main__":
    path = 'E:/timit数据集/data/lisa/data/timit/raw/TIMIT/TRAIN/*/*/*.WAV'
    sph_files = glob.glob(path)
    print(len(sph_files), "train utterences")
    for i in sph_files:
        sph = SPHFile(i)
        sph.write_wav(filename=i.replace(".WAV", "_.wav"))
        os.remove(i)
