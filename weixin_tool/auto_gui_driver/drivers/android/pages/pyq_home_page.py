# coding:utf-8
from weixin_tool.auto_gui_driver.drivers.android.pages.u2_base_page import BasePage


class PyqHomePage(BasePage):
    """
    朋友圈入口页面，以下两种情况进入朋友圈列表的xpath都是//*[@resource-id="com.tencent.mm:id/nk"]
      - 如果有历史照片，从右上角"我的朋友圈>"进入朋友圈列表
      - 如果没有历史照片，从中间"前往朋友圈>"进入朋友圈列表

    """

    def __init__(self, device):
        super().__init__(device)
        self.pyq_list_xpath = r'//*[@resource-id="com.tencent.mm:id/nk"]'

    def goto_pyq_list(self):
        """点击朋友圈入口"""
        return self.by_xpath(self.pyq_list_xpath).click()


