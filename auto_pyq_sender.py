#!/usr/bin/env python3
# coding: utf-8
import logging
import os
import time
import typing

import common_util.logger_config
from common_util.option_parser import OptionParser
from file_reader import FileReaderFactory
from weixin_tool import ABCWeiXinController, import_wx_ctl_cls_by_name


class AutoPYQSender:
    args = None
    logger = logging.getLogger('main.AutoPYQSender')

    def __init__(self, args=None):
        self.init_args(args)

    def init_args(self, args=None):
        if args is None:
            args = OptionParser().parse_args()
        self.args = args

    def run(self):
        self.logger.info('主流程开始执行')
        # 读取excel
        excel_file_path = os.path.abspath(self.args.excel_file)
        file_reader_cls = FileReaderFactory.get_reader_cls(content_format=self.args.file_format)
        freader = file_reader_cls(fpath=excel_file_path)
        fdata_list = freader.read_file()
        self.logger.info(f'文件内数据条数: {len(fdata_list)}')
        # 记录发送状态？
        pass  # TODO: determine data schema(record status for avoid duplicate sending)
        # 发送朋友圈
        wx_ctr_cls: typing.Type[ABCWeiXinController] = import_wx_ctl_cls_by_name(self.args.wx_ctl_cls)
        self.logger.debug(f'got wx_ctl_cls: {wx_ctr_cls} by input conf: {self.args.wx_ctl_cls}')
        wx_cls = wx_ctr_cls(conf=self.args)
        for r in fdata_list:
            pyq_text_content = r.get_pyq_text_content()
            pyq_pic_path_list = r.get_pic_path_list()
            self.logger.info(f'请求发送朋友圈: {pyq_text_content}, pyq_pic_path_list={pyq_pic_path_list}')
            resp = wx_cls.send_new_pyq(pyq_text_content=pyq_text_content, pyq_pic_path_list=pyq_pic_path_list)
            self.logger.info(f'请求发送朋友圈结果: {resp}')
            time.sleep(0.5)
        self.logger.info('主流程执行完毕')


if __name__ == '__main__':
    test_args = OptionParser().parse_args([
        '-f', './testdata/test_excel_file.txt',
        '--file_format', 'test_text',
        # '--wx_ctl_cls', 'weixin_tool.test_fake_weixin_controller.MockWeiXinController',
        # '--wx_ctl_cls', 'MockWeiXinController',
        '--wx_ctl_cls', 'weixin_tool.gui_weixin_controller.GUIWeiXinController',
        '--wx_ctl_gui_driver_cls', 'weixin_tool.auto_gui_driver.drivers.android.AndroidWeiXinGUIDriver',
        # '--wx_gui_driver_android_device_location', '192.168.1.21',
        # '-d',
    ])
    AutoPYQSender(args=test_args).run()
