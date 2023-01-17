# coding:utf-8
from weixin_tool.auto_gui_driver.drivers.android.pages.u2_base_page import BasePage


class PyqUploadPage(BasePage):
    """
    编辑朋友圈准备发布页面
    """

    def __init__(self, device):
        super().__init__(device)
        self.pyq_text_edit_id = 'com.tencent.mm:id/jsw'
        self.add_pic_button_xpath = r'//*[@content-desc="添加照片按钮"]'
        self.select_from_album_xpath = r'//*[@text="从相册选择"]'
        self.send_button_id = 'com.tencent.mm:id/en'

    def paste_pyq_text_content(self, text):
        """输入朋友圈文字内容"""
        self.by_id(id_name=self.pyq_text_edit_id).click()
        self.d.set_fastinput_ime(True)
        self.d.clear_text()
        self.d.send_keys(text)
        self.d.set_fastinput_ime(False)
        self.d.send_action("search")

    def click_add_pic_button(self):
        return self.by_xpath(xpath=self.add_pic_button_xpath).click()

    def click_select_from_album(self):
        return self.by_xpath(xpath=self.select_from_album_xpath).click()

    def click_send_button(self):
        """点击发送按钮，回到朋友圈列表页面"""
        return self.by_id(id_name=self.send_button_id).click()










