#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''
Time    : 2022/06/10 18:20
Author  : zhuchunjin
Email   : chunjin.zhu@taurentech.net
File    : write_otem.py
Software: PyCharm
'''

'''
    写入：例子  
            rest = read_and_write_iterable(0,0x1023,0x34)
            # :return  [16,35,52]
            spi.write(rest,1))
    读取：例子
            rest = read_and_write_iterable(1,0x1023) 
            # :return  [144,35] 
            spi.exchange(rest,1)    
'''


def read_and_write_iterable(flag, address, data=None):
    """
    :param address: 地址
    :param flag: 0:表示写入 1:表示读取
    :param data: 写入时用
    :return:
    """
    try:
        write_buffer = []
        adder_str = address.split('x')[1]
        if len(adder_str) != 4:
            new_adder = '0' * (4 - len(adder_str)) + adder_str
        else:
            new_adder = adder_str
        if flag == 0:
            # 写入数据
            write_buffer.append(int(new_adder[0:2], 16))
            write_buffer.append(int(new_adder[2:], 16))
            write_buffer.append(int(data.split('x')[1], 16))
        else:
            # 读出数据
            write_buffer.append(int(new_adder[0:2], 16) + 128)
            write_buffer.append(int(new_adder[2:], 16))
        return write_buffer
    except Exception as e:
        print(e)
