# coding: utf-8
import typing

from common_util.logger_config import cached_log_property_on_class, get_logger_by_class_name


class ABCGUIDriver:
    """
    基于gui模拟点击的driver接口
    """

    @cached_log_property_on_class
    def log(cls):
        return get_logger_by_class_name(cls=cls)

    def __init__(self, conf, *args, **kwargs):
        self.log.debug(f'init gui driver: {self}')

    def go_home(self):
        """回到起始页面"""
        raise NotImplementedError

    def send_pyq(self, pyq_text_content, pyq_pic_path_list, *args, **kwargs) -> typing.Tuple[bool, typing.Any]:
        """发送朋友圈"""
        raise NotImplementedError

    def send_text_msg(self, chat_name, text_msg_content, *args, **kwargs) -> typing.Tuple[bool, typing.Any]:
        """发送文字消息到好友/群聊"""
        raise NotImplementedError

    def send_pic_msg(self, chat_name, chat_pic_path_list, *args, **kwargs) -> typing.Tuple[bool, typing.Any]:
        """发送图片到好友/群聊"""
        raise NotImplementedError
