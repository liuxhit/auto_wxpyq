# coding:utf-8
import typing

from weixin_tool.abc_wx_controller import ABCWeiXinController


class MockWeiXinController(ABCWeiXinController):
    """测试使用的mock类"""

    def _tool_init(self, conf, *args, **kwargs):
        self.log.info(f'初始化WeiXinController成功: {self}, conf={conf}')

    def _send_new_pyq(self, pyq_text_content, pyq_pic_path_list, *args, **kwargs) -> typing.Tuple[bool, typing.Any]:
        self.log.info(f'假装发送了一条朋友圈: {pyq_text_content}, pyq_pic_path_list={pyq_pic_path_list}')
        return True, {'sent_content': pyq_text_content, 'pyq_pic_path_list': pyq_pic_path_list}

