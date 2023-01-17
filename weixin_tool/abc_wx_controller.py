# coding:utf-8
import logging
import inspect

from common_util.logger_config import cached_log_property_on_class, get_logger_by_class_name


def log_action_for_class_method(fun):
    def fun_wrapper(self, *args, **kwargs):
        action_name = fun.__name__
        action_kwargs = (args, kwargs)

        self.log.info(f'{self} calling action[{action_name}] with arguments: {action_kwargs}')
        ret = fun(self, *args, **kwargs)
        self.log.info(f'{self} action[{action_name}] done, ret: {ret}, original arguments: {action_kwargs}')

        return ret
    return fun_wrapper


class WeiXinControllerResult:
    action_name = ''
    success_flag = False
    context = None

    def __init__(self, action_name, is_success: bool, context=None):
        self.action_name = action_name
        self.success_flag = is_success
        self.context = context

    def is_success(self):
        return self.success_flag

    def get_context(self):
        return self.context

    def __str__(self):
        return f'WeiXinControllerResult[{self.action_name}]: 是否成功: {self.is_success()}, 上下文: {self.get_context()}'


class ABCWeiXinController:
    """
    微信控制器，对外暴露用户接口，具体实现交给子类
    """

    @cached_log_property_on_class
    def log(cls):
        return get_logger_by_class_name(cls=cls)

    def __init__(self, conf, *args, **kwargs):
        self.is_dry_run = conf.dry
        self.workspace = conf.wx_ctl_ws
        self._tool_init(conf, *args, **kwargs)

    @staticmethod
    def _make_resp(action_name, is_success: bool, context=None):
        return WeiXinControllerResult(action_name, is_success, context)

    @log_action_for_class_method
    def _tool_init(self, conf, *args, **kwargs):
        """
        登陆账号、连接设备等初始化操作
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    @log_action_for_class_method
    def send_new_pyq(self, pyq_text_content, pyq_pic_path_list, *args, **kwargs) -> WeiXinControllerResult:
        """
        发送新的朋友圈
        :param pyq_pic_path_list:
        :param pyq_text_content:
        :param args:
        :param kwargs:
        :return:
        """
        if self.is_dry_run:
            is_success, ctx = self._dry_send_new_pyq(pyq_text_content, pyq_pic_path_list, *args, **kwargs)
        else:
            is_success, ctx = self._send_new_pyq(pyq_text_content, pyq_pic_path_list, *args, **kwargs)
        return self._make_resp(action_name='send_pyq', is_success=is_success, context=ctx)

    def _dry_send_new_pyq(self, pyq_text_content, pyq_pic_path_list, *args, **kwargs):
        self.log.info(f'【DRY_RUN】发送了一条朋友圈: {pyq_text_content}')
        return True, {'dry_run': True, 'sent_content': pyq_text_content, 'pyq_pic_path_list': pyq_pic_path_list}

    def _send_new_pyq(self, pyq_text_content, pyq_pic_path_list, *args, **kwargs):
        raise NotImplementedError

    # @log_action_for_class_method
    # def send_msg_to_friend(self):
    #     """
    #     发送消息给好友
    #     :return:
    #     """
    #     raise NotImplementedError
    #
    # @log_action_for_class_method
    # def send_msg_to_group(self):
    #     """
    #     发送消息给群组
    #     :return:
    #     """
    #     raise NotImplementedError
    #
    # @log_action_for_class_method
    # def on_receive_msg(self):
    #     """
    #     接收到消息
    #     :return:
    #     """
    #     raise NotImplementedError
