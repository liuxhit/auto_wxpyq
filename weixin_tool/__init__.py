# coding:utf-8
from common_util.import_tool import import_by_name

from weixin_tool.abc_wx_controller import ABCWeiXinController
from weixin_tool.test_fake_weixin_controller import MockWeiXinController


def import_wx_ctl_cls_by_name(name_str):
    comp = name_str.split('.')[-1]
    if '.' in name_str:  # 入参是对象地址，直接import
        ret_cls = import_by_name(name_str=name_str)
    else:  # 入参是类名，尝试查找已经import的类
        ret_cls = globals()[comp]
    assert ret_cls, f'找不到类: {name_str}'
    return ret_cls

