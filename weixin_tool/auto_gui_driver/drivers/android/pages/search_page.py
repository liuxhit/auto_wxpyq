# coding:utf-8
import time

from weixin_tool.auto_gui_driver.drivers.android.pages.u2_base_page import BasePage


class SearchPage(BasePage):
    """
    微信搜索页
    """

    def __init__(self, device):
        super().__init__(device)
        self.search_text_id = 'com.tencent.mm:id/cd7'
        # self.search_result_icon_class = 'android.widget.ImageView'
        self.search_result_icon_id = 'com.tencent.mm:id/a27'  # 可能有多条，默认点第一条

    def paste_search_text_content(self, text):
        """输入朋友圈文字内容"""
        self.by_id(id_name=self.search_text_id).click()
        self.d.set_fastinput_ime(True)
        self.d.clear_text()
        self.d.send_keys(text)
        self.d.set_fastinput_ime(False)
        self.d.send_action("search")

    def click_first_search_result(self, range_int=0):
        """点击第一个搜索结果"""
        can_select_icon_list = self.by_id(id_name=self.search_result_icon_id)
        time.sleep(1)  # 等待一秒加载图片
        len_icon = len(can_select_icon_list)
        if len_icon <= range_int:
            raise RuntimeError(f'待选择搜索结果数组越界: len={len_icon}, input_index={range_int}, raw_list={can_select_icon_list}')
        return can_select_icon_list[range_int].click()
