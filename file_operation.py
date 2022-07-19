#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''
Time    : 2022/06/10 14:03
Author  : zhuchunjin
Email   : chunjin.zhu@taurentech.net
File    : file_operation.py
Software: PyCharm
'''
from PyQt5.QtWidgets import QWidget,QHBoxLayout, QDesktopWidget, QFileDialog, QMessageBox,QInputDialog
from PyQt5.QtCore import QDir
from export import Ui_Form
import xlrd
from pyftdi.ftdi import Ftdi
from pyftdi.gpio import (GpioAsyncController,
                         GpioSyncController,
                         GpioMpsseController)
from pyftdi.spi import SpiController, SpiIOError

from binascii import hexlify

class spi_attribute:
    freq = 30000000
    cs = 0
    mode = 0
    cpol = 0
    cpha = 0
    tranbits = 8
    chn = 0

class LoadingPanel(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.url_port = []
        self.port = []
        self.spi_a = None
        try:
            self.init_spi_config()
        except Exception as e:
            QMessageBox.information(self, 'warning',
                                    '%s'%e)
        self.all_write.pressed.connect(self.all_write_btn)
        self.read_one_data.pressed.connect(self.read_one_data_tn)
        self.write_one_data.pressed.connect(self.write_one_data_tn)

    def init_spi_config(self):
        Ftdi.show_devices()
        dev_urls = Ftdi.list_devices()
        for i in range(dev_urls[0][1]):
            self.url_port.append(
                r'ftdi://ftdi:4232:' + str(dev_urls[0][0].bus) + ':' + str(hex(dev_urls[0][0].address)) + r'/' + str(i + 1))
        self.port.append(SpiController())
        self.port[0].configure(self.url_port[0], cs_count=1)
        self.port.append(SpiController())
        self.port[1].configure(self.url_port[1], cs_count=1)
        self.port.append(GpioAsyncController())
        self.port[2].configure(self.url_port[2], direction=0xff, initial=0x83)
        self.port.append(GpioAsyncController())
        self.port[3].configure(self.url_port[3], direction=0x00, initial=0x0)
        # Set channelA
        dq = spi_attribute
        self.spi_a = self.port[dq.chn].get_port(dq.cs)
        self.spi_a.set_frequency(dq.freq)
        self.spi_a.set_mode(dq.mode)

    def all_write_btn(self):
        curPath = QDir.currentPath()
        filt = "All Files (*)"
        fname, filetype = QFileDialog.getOpenFileName(self, 'open file', curPath, filt)
        if fname == "":
            return
        else:
            self.w_excel(fname)


    def w_excel(self,f_path):
        try:
            workBook =xlrd.open_workbook(f_path)
            sheet_names=workBook.sheet_names()
            items= set(sheet_names)
            item, ok=QInputDialog.getItem(self, "select input dialog", 'sheet列表', items, 0, False)
            if ok:
                # 选择一个文件的sheet表
                worksheet=workBook.sheet_by_name(item)
                rows=worksheet.nrows
                # cols=worksheet.ncols
                for i in range(rows):
                    addrr = worksheet.cell_value(i,0)
                    value = worksheet.cell_value(i,1)
                    write_bufer = self.write_switch_addr(addrr)
                    print('write addr = ' + addrr + ' data = ' + value)
                    write_bufer.append(int(value.split('x')[1],16))
                    self.spi_a.write(write_bufer,1)
        except Exception as e:
            print(e)

    def switch_addr(self,addr):
        # 读
        try:
            write_buffer = []
            addr_str = addr.split('x')[1]
            if len(addr_str)!=4:
                new_addr = '0'*(4-len(addr_str))+addr_str
                print(new_addr)
            else:
                new_addr = addr_str
            write_buffer.append(int(new_addr[0:2], 16) + 128)
            write_buffer.append(int(new_addr[2:], 16))
            return write_buffer
        except Exception as e:
            print(e)

    def write_switch_addr(self,addr):
        try:
            write_buffer = []
            addr_str = addr.split('x')[1]
            if len(addr_str)!=4:
                new_addr = '0'*(4-len(addr_str))+addr_str
            else:
                new_addr = addr_str
            write_buffer.append(int(new_addr[0:2], 16))
            write_buffer.append(int(new_addr[2:], 16))
            return write_buffer
        except Exception as e:
            print(e)


    def read_one_data_tn(self):
        try:
            addr=self.read_addr.text().strip(" ")
            if len(addr)!=0:
                read_data = self.spi_a.exchange(self.switch_addr(addr),1)
                print('read addr = ' + addr + ' data = ' + hex(int(hexlify(read_data).decode(),16)))
                self.read_line.setText(hex(int(hexlify(read_data).decode(),16)))
            else:
                return
        except Exception as e:
            print(e)

    def write_one_data_tn(self):
        try:
            addr = self.write_addr.text().strip(" ")
            value = self.write_line.text().strip(" ")
            if len(addr)!=0 and len(value)!=0:
                print ('write addr = '+addr+' data = '+value)
                write_bufer = self.write_switch_addr(addr)
                write_bufer.append(int(value.split('x')[1], 16))
                self.spi_a.write(write_bufer, 1)
            else:
                return
        except Exception as e:
            print(e)
