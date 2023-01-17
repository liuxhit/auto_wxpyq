# coding: utf-8
import os.path

from file_reader.abc_file_reader import ABCFileReader
from file_reader.file_reader_factory import FileReaderFactory
from data_store.record import DataRecord


@FileReaderFactory.register()
class TestTextFileReader(ABCFileReader):
    """
    测试，文本文件，一行一个待发送的朋友圈内容
    每行格式：文字内容|图片文件名(相对文件路径),多个就逗号分割
    """
    content_format = 'test_text'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read_file(self):
        with open(self.fpath, 'r') as f:
            content = list(filter(None, [line.strip() for line in f.readlines()]))
        res = []
        fdir = os.path.dirname(self.fpath)
        for c in content:
            text_content, pic_path_str = c.rsplit('|', 1)
            pyq_pic_path = None
            if pic_path_str.strip():
                pyq_pic_path = [os.path.abspath(os.path.join(fdir, p)) for p in pic_path_str.split(',')]
            res.append(DataRecord(pyq_text_content=text_content, pyq_pic_path=pyq_pic_path))
        return res
