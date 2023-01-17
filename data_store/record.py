# coding: utf-8
import typing
import os
import logging


class DataRecord:
    # TODO: persistence ability
    # TODO: picture manage

    id: int = -1                            # PK
    # datekey: str = ''                       # 日期？
    pyq_text_content: str = ''              # 朋友圈文字内容
    pyq_pic_path: typing.List[str] = None   # 朋友圈图片文件路径
    pyq_send_status: bool = False           # 是否已发送

    logger = logging.getLogger(__name__)

    def __init__(self, pyq_text_content, pyq_pic_path: typing.List[str] = None):
        self.pyq_text_content = pyq_text_content
        self.pyq_pic_path = []
        if pyq_pic_path:
            for pic_file in pyq_pic_path:
                self.add_pic(pic_file)

    def __str__(self):
        return repr(self) + f'[pyq_text_content={self.pyq_text_content}, pyq_pic_path={self.pyq_pic_path}, pyq_send_status={self.pyq_send_status}]'

    def get_pyq_text_content(self):
        return self.pyq_text_content

    def get_pic_path_list(self):
        return self.pyq_pic_path or []

    def add_pic(self, pic_file):
        p = os.path.abspath(pic_file)
        if not os.access(p, os.R_OK):
            self.logger.error(f'图片文件不可读或不存在: {p}')
            return
        self.pyq_pic_path.append(p)

    def mark_sent(self):
        self.pyq_send_status = True

    def is_sent(self):
        return self.pyq_send_status
