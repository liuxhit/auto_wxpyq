# coding:utf-8
from weixin_tool.auto_gui_driver.drivers.android.pages.u2_base_page import BasePage


class ChatPage(BasePage):
    """
    聊天页面
    """

    def __init__(self, device):
        super().__init__(device)
        self.msg_edit_id = 'com.tencent.mm:id/kii'
        self.send_button_id = 'com.tencent.mm:id/b8k'
        self.more_button_id = 'com.tencent.mm:id/b3q'
        self.more_button_child_text_id = 'com.tencent.mm:id/vg'
        self.more_button_child_pic_id = 'com.tencent.mm:id/ve'
        self.album_button_text = '相册'

    def paste_msg_text_content(self, text):
        """输入消息文字内容"""
        self.by_id(id_name=self.msg_edit_id).click()
        self.d.set_fastinput_ime(True)
        self.d.clear_text()
        self.d.send_keys(text)
        self.d.set_fastinput_ime(False)
        self.d.send_action("search")

    def click_send_button(self):
        """点击发送按钮"""
        send_button = self.by_id(id_name=self.send_button_id)
        found_send_button = len(send_button)
        if found_send_button != 1:
            raise RuntimeError(f'没找到发送按钮, len={found_send_button} send_button={send_button}')
        return send_button.click()

    def click_more_button(self):
        """点击更多功能按钮"""
        return self.by_id(id_name=self.more_button_id).click()

    def click_album_button(self):
        """点击更多功能中的相册图标，进入图片选择页面"""
        album_text = self.by_id_text(id_name=self.more_button_child_text_id, text_name=self.album_button_text)
        album_pic = album_text.up(resourceId=self.more_button_child_pic_id)  # 图标在对应文字上方，ua2实现为遍历up(条件)的结果判断控件的边界值，查找满足要求的最接近的控件
        assert album_pic, f'功能按钮图标查找失败'
        return album_pic.click()

