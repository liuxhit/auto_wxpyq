# coding: utf-8
import logging
import typing

from file_reader.abc_file_reader import ABCFileReader


class FileReaderFactory:
    logger = logging.getLogger('main.FileReaderFactory')
    reader_dict = {}

    @classmethod
    def get_reader_cls(cls, content_format) -> typing.Type[ABCFileReader]:
        reader_cls = cls.reader_dict.get(content_format, None)
        if reader_cls is not None:
            return reader_cls
        errmsg = f'未知文件格式: {content_format}, 已知格式列表: {cls.reader_dict}'
        cls.logger.warning(errmsg)
        raise ValueError(errmsg)

    @classmethod
    def add_file_reader(cls, reader_cls: ABCFileReader):
        reader_format = reader_cls.content_format
        if not reader_format:
            cls.logger.warning(f'skip invalid file reader: {reader_cls}(format: {reader_format})')
            return
        if reader_format in cls.reader_dict:
            cls.logger.warning(f'skip repeated file reader: {reader_cls}(format: {reader_format})')
            return
        cls.reader_dict[reader_format] = reader_cls
        cls.logger.debug(f'add one file reader[{reader_cls}] for format[{reader_format}]')

    @classmethod
    def register(cls):
        def wrapper(reader_cls):
            cls.add_file_reader(reader_cls=reader_cls)
            return reader_cls
        return wrapper
