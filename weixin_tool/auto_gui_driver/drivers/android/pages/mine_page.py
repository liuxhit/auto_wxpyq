# coding:utf-8
from weixin_tool.auto_gui_driver.drivers.android.pages.u2_base_page import BasePage


class MinePage(BasePage):
    """
    "我"页面
    有朋友圈入口
    """

    def __init__(self, device):
        super().__init__(device)
        self.pyq_xpath = r'//*[@text="朋友圈"]'

    def click_pyq(self):
        """点击朋友圈入口"""
        return self.by_xpath(self.pyq_xpath).click()
