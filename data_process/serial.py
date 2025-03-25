import h5py
import numpy as np
import time
from netCDF4 import Dataset as DS
import os

def writetofile(src, dest, channel_idx, varslist, src_idx=0, frmt='nc'):
    if os.path.isfile(src):
        batch = 2**4
        Nimgtot = 52  # 总图像数量（假设固定为 52）

        # 初始化索引
        idx = 0
        end = Nimgtot

        for variable_name in varslist:
            # 打开源文件
            if frmt == 'nc':
                fsrc = DS(src, 'r', format="NETCDF4").variables[variable_name]
            elif frmt == 'h5':
                fsrc = h5py.File(src, 'r')[varslist[0]]

            print("fsrc shape", fsrc.shape)

            # 打开目标文件
            fdest = h5py.File(dest, 'a')

            start = time.time()
            while idx < end:
                # 如果剩余数据不足一个批次
                if end - idx < batch:
                    if len(fsrc.shape) == 4:
                        ims = fsrc[idx:end, src_idx]
                    else:
                        ims = fsrc[idx:end]

                    print(ims.shape)
                    fdest['fields'][idx:end, channel_idx, :, :] = ims
                    break
                else:
                    # 按批次读取数据
                    if len(fsrc.shape) == 4:
                        ims = fsrc[idx:idx + batch, src_idx]
                    else:
                        ims = fsrc[idx:idx + batch]

                    print("ims shape", ims.shape)
                    fdest['fields'][idx:idx + batch, channel_idx, :, :] = ims
                    idx += batch

                    # 计算并打印 ETA
                    ttot = time.time() - start
                    eta = (end - idx) / ((idx - 0) / ttot)
                    hrs = eta // 3600
                    mins = (eta - 3600 * hrs) // 60
                    secs = (eta - 3600 * hrs - 60 * mins)
                    print(f"ETA: {hrs} hours, {mins} minutes, {secs} seconds")

            # 记录总耗时
            ttot = time.time() - start
            hrs = ttot // 3600
            mins = (ttot - 3600 * hrs) // 60
            secs = (ttot - 3600 * hrs - 60 * mins)
            print(f"Total time: {hrs} hours, {mins} minutes, {secs} seconds")

            channel_idx += 1

# 文件路径
dest = 'oct_2021_19_21.h5'
src = 'data_stream-oper_stepType-instant.nc'

def initialize_hdf5(dest, shape, dtype='float32'):
    """
    初始化目标 HDF5 文件，创建 'fields' 数据集。
    :param dest: 目标文件路径
    :param shape: 数据集的形状 (Nimgtot, num_channels, height, width)
    :param dtype: 数据类型，默认为 float32
    """
    with h5py.File(dest, 'a') as f:
        if 'fields' not in f:
            print("Creating dataset 'fields' with shape:", shape)
            f.create_dataset('fields', shape=shape, dtype=dtype)

# 在调用 writetofile 之前初始化目标文件
Nimgtot = 52  # 总图像数量
num_channels = 17  # 假设有 17 个通道
height, width = 721, 1440  # 假设每个图像的高度和宽度
# initialize_hdf5(dest, shape=(Nimgtot, num_channels, height, width))

# 调用函数
# writetofile(src, dest, 0, ['t'], 2)

# 可以根据需要调用其他变量
# writetofile(src, dest, 6, ['u'], 3)
# writetofile(src, dest, 7, ['v'], 3)
# writetofile(src, dest, 8, ['z'], 3)
# import h5py

def inspect_hdf5(file_path):
    """
    打印 HDF5 文件中的所有对象（数据集和组）。
    :param file_path: HDF5 文件路径
    """
    with h5py.File(file_path, 'r') as f:
        print("Contents of HDF5 file:")
        f.visititems(lambda name, obj: print(name, obj))

# 检查目标文件的内容
inspect_hdf5(dest)