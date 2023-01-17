#!/usr/bin/env python3
# coding: utf-8
import logging
import argparse
import sys


class OptionParser:
    logger = logging.getLogger('main.OptionParser')

    def __init__(self):
        ap = argparse.ArgumentParser()
        ap.add_argument('-f', '--excel_file', metavar='PATH_TO_EXCEL_FILE', help='输入excel文件路径', required=True)
        # TODO: change default file format
        ap.add_argument('--file_format', metavar='CONTENT_FORMAT', default='test_text', help='输入文件的格式')
        # TODO: impl default weixin controller
        ap.add_argument('--wx_ctl_cls', metavar='PYTHON_CLASS_PATH', default='MockWeiXinController', help='微信控制类')
        ap.add_argument('--wx_ctl_ws', metavar='PATH_TO_DIR', default='./testdata', help='临时工作目录')
        ap.add_argument('--wx_ctl_gui_driver_cls', metavar='PYTHON_CLASS_PATH',
                        default='weixin_tool.auto_gui_driver.drivers.android.AndroidWeiXinGUIDriver',
                        help='微信控制类'
                        )
        ap.add_argument('--wx_gui_driver_android_device_location', metavar='SERIAL|IP|IP:PORT',
                        default='',
                        help='安卓adb设备地址（序列号/ip/ip端口），overrides $ANDROID_DEVICE_IP or $ANDROID_SERIAL'
                        )
        ap.add_argument('--wx_ctl_gui_driver_android_ws', metavar='TMP_PATH_ON_PHONE',
                        default='/data/local/tmp/weixin_auto_gui_ws')
        ap.add_argument('-d', '--dry', help='测试', action='store_true')

        self.ap = ap

    def parse_args(self, test_args=None):
        self.logger.debug(f'sys argv: {sys.argv[1:]}')
        self.logger.debug(f'test_args: {test_args}')
        if test_args is None:
            res = self.ap.parse_args()
        else:
            res = self.ap.parse_args(args=test_args)
        self.logger.debug(f'parsed args: {res}')
        return res




