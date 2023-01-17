# coding:utf-8
import time

from weixin_tool.auto_gui_driver.drivers.android.pages.u2_base_page import BasePage


class AlbumSelectPage(BasePage):
    """
    相册选择页面
    """

    def __init__(self, device):
        super().__init__(device)
        self.select_album_id = 'com.tencent.mm:id/gqb'
        self.album_pic_class = 'android.widget.RelativeLayout'
        self.done_xpath = r'//*[@resource-id="com.tencent.mm:id/en"]'

    def select_picture_by_int(self, range_int):
        """选择第几张图片"""
        can_select_pic_list = self.find_child_by_id_class(id_name=self.select_album_id, class_name=self.album_pic_class)
        time.sleep(1)  # 等待一秒加载图片
        len_pic = len(can_select_pic_list)
        if len_pic <= range_int:
            raise RuntimeError(f'待选择图片数组越界: len={len_pic}, input_index={range_int}, raw_list={can_select_pic_list}')
        return can_select_pic_list[range_int].click()

    def click_done_button(self):
        return self.by_xpath(self.done_xpath).click()









