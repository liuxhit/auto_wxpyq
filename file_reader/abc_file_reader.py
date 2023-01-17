# coding: utf-8
import logging
import typing
import os

from data_store.record import DataRecord


class ABCFileReader:
    """
    读取文件所有内容（假设文件不是很大），解析为一条一条待定格式
    """
    content_format: str = ''
    logger = logging.getLogger('main.FileReader')

    def __init__(self, fpath, *args, **kwargs):
        self.fpath = fpath

        self.logger.info(f'输入文件路径: {fpath}')
        self.logger.info(f'输入文件格式: {self.content_format}')
        if not os.access(fpath, os.R_OK):
            errmsg = f'文件不可读或不存在: {fpath}'
            self.logger.fatal(errmsg)
            raise ValueError(errmsg)

    def read_file(self) -> typing.List[DataRecord]:
        raise NotImplementedError
