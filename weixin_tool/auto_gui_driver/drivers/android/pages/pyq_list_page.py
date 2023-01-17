# coding:utf-8
from weixin_tool.auto_gui_driver.drivers.android.pages.u2_base_page import BasePage


class PyqListPage(BasePage):
    """
    朋友圈列表页面，有一个照相机图标可以发新朋友圈

    """

    def __init__(self, device):
        super().__init__(device)
        self.send_new_pyq_id = 'com.tencent.mm:id/ju8'
        self.select_from_album_xpath = r'//*[@text="从相册选择"]'
        self.select_album_id = 'com.tencent.mm:id/gqb'
        self.album_pic_class = 'android.widget.RelativeLayout'

    def click_send_new_pyq(self):
        """点击发送朋友圈"""
        return self.by_id(self.send_new_pyq_id).click()

    def click_select_from_album(self):
        """（发送新朋友圈）点击从相册选择"""
        return self.by_xpath(self.select_from_album_xpath).click()

