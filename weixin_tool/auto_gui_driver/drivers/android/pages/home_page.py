# coding:utf-8
from weixin_tool.auto_gui_driver.drivers.android.pages.u2_base_page import BasePage


class HomePage(BasePage):
    """
    微信启动页，下方四个tag入口：微信/通讯录/发现/我
    """

    def __init__(self, device):
        super().__init__(device)
        self.mine_xpath = r'//*[@resource-id="com.tencent.mm:id/fj3"]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[4]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]'
        self.search_icon_id = 'com.tencent.mm:id/j5t'

    def msg_icon_obj(self):
        """会话图标"""
        return self.by_id(id_name=self.msg_icon)

    def click_msg_icon(self):
        """点击底部会话图标"""
        return self.by_id(id_name=self.msg_icon).click()

    def click_friend_icon(self):
        """点击底部通讯录图标"""
        return self.by_id(id_name=self.friend_icon).click()

    def click_find_icon(self):
        """点击底部发现图标"""
        return self.by_id(id_name=self.find_icon).click()

    def click_mine_icon(self):
        """点击底部我的图标"""
        return self.by_xpath(self.mine_xpath).click()

    def click_search_icon(self):
        """点击右上角+号图标"""
        return self.by_id(id_name=self.search_icon_id).click()

    def click_create_group_btn(self):
        """点击右上角+号图标"""
        return self.by_id(id_name=self.create_group_btn).click()