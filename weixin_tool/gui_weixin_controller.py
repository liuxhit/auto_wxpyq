# coding:utf-8
import typing
import os

from common_util.import_tool import import_by_name
from weixin_tool.abc_wx_controller import ABCWeiXinController
from weixin_tool.auto_gui_driver import ABCGUIDriver


class GUIWeiXinController(ABCWeiXinController):
    """
    基于gui模拟点击的微信控制器，接口为通用逻辑供各平台driver实现，init环节选择加载不同平台的driver
    """
    gui_driver = None

    def __str__(self):
        return repr(self) + f'[driver={self.gui_driver} workspace={self.workspace}]'

    def _tool_init(self, conf, *args, **kwargs):
        # 初始化工作目录
        self.workspace = os.path.abspath(conf.wx_ctl_ws)
        if not os.path.exists(self.workspace):
            os.mkdir(self.workspace)
        self.log.debug(f'初始化wx_ctl工作目录: {self.workspace}')

        driver_cls: typing.Type[ABCGUIDriver] = import_by_name(conf.wx_ctl_gui_driver_cls)
        if not driver_cls:
            errmsg = f'找不到gui_driver类: {conf.wx_ctl_gui_driver_cls}'
            self.log.fatal(errmsg)
            raise RuntimeError(errmsg)
        self.gui_driver = driver_cls(conf, *args, **kwargs)
        self.log.info(f'初始化WeiXinController成功: {self}, conf={conf}')

    def _send_new_pyq(self, pyq_text_content, pyq_pic_path_list, *args, **kwargs) -> typing.Tuple[bool, typing.Any]:
        ret, driver_ret_data = self.gui_driver.send_pyq(pyq_text_content, pyq_pic_path_list)
        return ret, {'driver_ret_data': driver_ret_data, 'sent_content': pyq_text_content, 'pyq_pic_path_list': pyq_pic_path_list}

    def _dry_send_new_pyq(self, pyq_text_content, pyq_pic_path_list, *args, **kwargs):
        self.log.info(f'【GUI_WXC_DRY_RUN】假装通过GUI模拟点击发送了一条朋友圈: {pyq_text_content}')
        return True, {'dry_run': True, 'sent_content': pyq_text_content, 'pyq_pic_path_list': pyq_pic_path_list}

    def _dry_send_text_msg(self, chat_name, text_msg_content, *args, **kwargs):
        self.log.info(f'【GUI_WXC_DRY_RUN】假装通过GUI模拟点击发送了一条消息给【{chat_name}】: {text_msg_content}')
        return super()._dry_send_text_msg(chat_name, text_msg_content, *args, **kwargs)

    def _send_text_msg(self, chat_name, text_msg_content, *args, **kwargs):
        ret, driver_ret_data = self.gui_driver.send_text_msg(chat_name, text_msg_content)
        return ret, {'driver_ret_data': driver_ret_data, 'chat_name': chat_name, 'sent_content': text_msg_content}

    def _dry_send_pic_msg(self, chat_name, chat_pic_path_list, *args, **kwargs):
        self.log.info(f'【GUI_WXC_DRY_RUN】假装通过GUI模拟点击发送了一个图片给【{chat_name}】: {chat_pic_path_list}')
        return super()._dry_send_pic_msg(chat_name, chat_pic_path_list, *args, **kwargs)

    def _send_pic_msg(self, chat_name, chat_pic_path_list, *args, **kwargs):
        ret, driver_ret_data = self.gui_driver.send_pic_msg(chat_name, chat_pic_path_list)
        return ret, {'driver_ret_data': driver_ret_data, 'chat_name': chat_name, 'chat_pic_path_list': chat_pic_path_list}




