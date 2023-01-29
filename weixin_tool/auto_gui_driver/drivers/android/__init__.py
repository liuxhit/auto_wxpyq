# coding: utf-8
import time
import datetime
import typing
import os
from contextlib import contextmanager

from weixin_tool.auto_gui_driver import ABCGUIDriver

import uiautomator2 as u2
from weixin_tool.auto_gui_driver.drivers.android.pages import HomePage, MinePage, PyqHomePage, PyqListPage, AlbumSelectPage, PyqUploadPage, SearchPage, ChatPage


class AndroidWeiXinGUIDriver(ABCGUIDriver):
    """
    设备：米6
    微信版本：8.0.32
    """
    device_location = ''  # 设备地址（序列号或者ip）
    host_ws = ''  # 电脑端临时工作目录
    device_ws = ''  # 设备端临时工作目录
    apk = 'com.tencent.mm'  # 微信包名
    home_activity = 'com.tencent.mm.ui.LauncherUI'  # 起始页面
    device_album_dir = '/sdcard/DCIM/Camera/'

    d: u2.Device = None
    home: HomePage = None
    mine: MinePage = None
    pyq_home: PyqHomePage = None
    pyq_list: PyqListPage = None
    album_select: AlbumSelectPage = None
    pyq_upload: PyqUploadPage = None
    search: SearchPage = None
    chat: ChatPage = None

    to_clean_device_pic_file: typing.List[str] = None

    sleep_sec = 1

    def __init__(self, conf, *args, **kwargs):
        super().__init__(conf, *args, **kwargs)
        self.setup(conf)

    def __str__(self):
        return repr(self) + f'[device={self._device_info()}, current_app={self._current_app()}]'

    def setup(self, conf):
        # 初始化host端临时目录
        self.host_ws = os.path.abspath(os.path.join(conf.wx_ctl_ws, 'android_host_ws'))
        if not os.path.exists(self.host_ws):
            os.mkdir(self.host_ws)
        self.log.debug(f'初始化host端工作目录: {self.host_ws}')

        # 连接设备
        self.device_location = conf.wx_gui_driver_android_device_location
        self.d = u2.connect(self.device_location)
        self.log.debug(f'连接到设备: {self._device_info()}')

        # 初始化设备端临时目录
        self.device_ws = conf.wx_ctl_gui_driver_android_ws
        mkdir_cmd = f'mkdir -p {self.device_ws}'
        r1 = self.d.shell(mkdir_cmd)
        r2 = self.d.shell(f'ls -ld {self.device_ws} ; ls -lR {self.device_ws}')
        self.log.debug(f'初始化设备端工作目录: {self.device_ws}, cmd: [{mkdir_cmd}], cmd_ret_code: {r1.exit_code}, ls_res_after_init: {r2.output}')

        # 重启微信
        self.d.app_start(package_name=self.apk, activity=self.home_activity, stop=True, wait=True)

        # 初始化page
        self.home = HomePage(self.d)
        self.mine = MinePage(self.d)
        self.pyq_home = PyqHomePage(self.d)
        self.pyq_list = PyqListPage(self.d)
        self.album_select = AlbumSelectPage(self.d)
        self.pyq_upload = PyqUploadPage(self.d)
        self.search = SearchPage(self.d)
        self.chat = ChatPage(self.d)

        # 初始化资源清理列表
        self.to_clean_device_pic_file = []

        self.log.info(f'微信app初始化完成: {self}')

    def _device_info(self):
        if not self.d:
            return None
        return self.d.info

    def _current_app(self):
        if not self.d:
            return None
        return self.d.app_current()

    @staticmethod
    def _get_device_file_name_infix():
        """推送文件到远端后，为避免文件名冲突，在文件名里面加一些标识性的中缀"""
        now = datetime.datetime.now()
        time_str = now.strftime('%Y%m%d_%H%M%S_%f')
        return time_str

    def _make_device_pic_path_for_push(self, host_pic_path):
        from pathlib import Path
        original_filename = os.path.basename(host_pic_path)
        device_file_name = f'PIC_{self._get_device_file_name_infix()}_{original_filename}'
        device_file_path = Path(os.path.join(self.device_album_dir, device_file_name)).as_posix()  # in case of running at windows
        return device_file_path

    @contextmanager
    def _push_pic_and_refresh(self, host_pic_path, dst='', mode=0o755):
        """push图片并refresh数据库，dst尽量保证是目标文件名"""
        if not dst:
            dst = self._make_device_pic_path_for_push(host_pic_path=host_pic_path)
        self.d.push(src=host_pic_path, dst=dst, mode=mode)
        self.log.info(f'发送文件: {host_pic_path} -> {dst}, mode={mode}')
        time.sleep(self.sleep_sec)
        refresh_cmd = f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{dst}'
        r = self.d.shell(refresh_cmd)
        self.log.info(f'通知更新: {refresh_cmd}, ret_code={r.exit_code}, output={r.output}')
        time.sleep(self.sleep_sec)
        try:
            yield
        except Exception as e:
            self.log.exception(f'error while yield: {e}')
            raise e
        finally:
            self.to_clean_device_pic_file.append(dst)

    def _delete_pic_and_refresh(self, device_pic_path):
        """删除图片文件并刷新缓存"""
        self.d.shell(f'rm {device_pic_path}')
        time.sleep(self.sleep_sec)
        self.d.shell(f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{device_pic_path}')
        time.sleep(self.sleep_sec)
        self.log.info(f'清理设备文件: {device_pic_path}')

    def go_home(self):
        self.d.app_start(package_name=self.apk, activity=self.home_activity, stop=True, wait=True)

    def send_pyq(self, pyq_text_content, pyq_pic_path_list, *args, **kwargs) -> typing.Tuple[bool, typing.Any]:
        """
        发送一条朋友圈（照片随机选择一个相册图片）
        :param pyq_pic_path_list: host端的图片地址
        :param pyq_text_content:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            assert len(pyq_pic_path_list) >= 1, f'不能发送不带图片的朋友圈'
            self.go_home()  # 重置app，进入初始页面
            time.sleep(self.sleep_sec)
            with self._push_pic_and_refresh(host_pic_path=pyq_pic_path_list[0]):
                time.sleep(self.sleep_sec)
                self.home.click_mine_icon()  # 点击右下角"我"
                time.sleep(self.sleep_sec)
                self.mine.click_pyq()  # 点击朋友圈
                time.sleep(self.sleep_sec)
                self.pyq_home.goto_pyq_list()  # 点击进入朋友圈列表
                time.sleep(self.sleep_sec)
                time.sleep(self.sleep_sec)
                self.pyq_list.click_send_new_pyq()  # 点击开始发送新朋友圈
                time.sleep(self.sleep_sec)
                self.pyq_list.click_select_from_album()  # 点击从相册选择按钮
                time.sleep(self.sleep_sec)
                self.album_select.select_picture_by_int(0)  # 选择第一张图片
                time.sleep(self.sleep_sec)
                self.album_select.click_done_button()  # 完成照片选择，进入新朋友圈编辑页面
                time.sleep(self.sleep_sec)
            self.pyq_upload.paste_pyq_text_content(text=pyq_text_content)  # 输入朋友圈的文字内容
            time.sleep(self.sleep_sec)
            for pic_path in pyq_pic_path_list[1:]:
                with self._push_pic_and_refresh(host_pic_path=pic_path):
                    time.sleep(self.sleep_sec)
                    self.pyq_upload.click_add_pic_button()
                    time.sleep(self.sleep_sec)
                    self.pyq_upload.click_select_from_album()
                    time.sleep(self.sleep_sec)
                    self.album_select.select_picture_by_int(0)  # 选择第一张照片（新上传的）
                    time.sleep(self.sleep_sec)
                    self.album_select.click_done_button()  # 完成照片选择，进入新朋友圈编辑页面
                    time.sleep(self.sleep_sec)
            self.pyq_upload.click_send_button()
            time.sleep(self.sleep_sec)
            # todo: check send result
            return True, None
        except Exception as e:
            self.log.exception(f'driver发送朋友圈出错: {e}')
            return False, {'error': e}
        finally:
            while self.to_clean_device_pic_file:
                p = self.to_clean_device_pic_file.pop()
                self._delete_pic_and_refresh(device_pic_path=p)
                time.sleep(self.sleep_sec)

    def send_text_msg(self, chat_name, text_msg_content, *args, **kwargs) -> typing.Tuple[bool, typing.Any]:
        """发送文字消息到好友/群聊"""
        try:
            self.go_home()
            time.sleep(self.sleep_sec)
            self.home.click_search_icon()
            time.sleep(self.sleep_sec)
            self.search.paste_search_text_content(chat_name)
            time.sleep(self.sleep_sec)
            self.search.click_first_search_result()
            time.sleep(self.sleep_sec)
            self.chat.paste_msg_text_content(text_msg_content)
            time.sleep(self.sleep_sec)
            self.chat.click_send_button()
            time.sleep(self.sleep_sec)
            # TODO: check send result
            return True, None
        except Exception as e:
            self.log.exception(f'driver发送聊天消息出错: {e}')
            return False, {'error': e}

    def send_pic_msg(self, chat_name, chat_pic_path_list, *args, **kwargs) -> typing.Tuple[bool, typing.Any]:
        """发送图片到好友/群聊"""
        try:
            assert len(chat_pic_path_list) >= 1, f'待发送图片列表为空'
            self.go_home()
            time.sleep(self.sleep_sec)
            self.home.click_search_icon()
            time.sleep(self.sleep_sec)
            self.search.paste_search_text_content(chat_name)
            time.sleep(self.sleep_sec)
            self.search.click_first_search_result()
            time.sleep(self.sleep_sec)
            for pic_path in chat_pic_path_list:
                with self._push_pic_and_refresh(host_pic_path=pic_path):
                    time.sleep(self.sleep_sec)
                    self.chat.click_more_button()
                    time.sleep(self.sleep_sec)
                    self.chat.click_album_button()
                    time.sleep(self.sleep_sec)
                    self.album_select.select_picture_by_int(0)  # 选择第一张照片（新上传的）
                    time.sleep(self.sleep_sec)
                    self.album_select.click_done_button()  # 完成照片选择，进入新朋友圈编辑页面
                    time.sleep(self.sleep_sec)
            time.sleep(self.sleep_sec)
            # TODO: check send result
            return True, None
        except Exception as e:
            self.log.exception(f'driver发送聊天图片出错: {e}')
            return False, {'error': e}
        finally:
            while self.to_clean_device_pic_file:
                p = self.to_clean_device_pic_file.pop()
                self._delete_pic_and_refresh(device_pic_path=p)
                time.sleep(self.sleep_sec)


if __name__ == '__main__':
    exit()  # 仅保存代码，防止误操作运行
    import uiautomator2 as u2
    d = u2.connect()

    from weixin_tool.auto_gui_driver.drivers.android.pages import BasePage
    b = BasePage(d)

    from weixin_tool.auto_gui_driver.drivers.android.pages import HomePage, MinePage, PyqHomePage, PyqListPage, AlbumSelectPage, PyqUploadPage, SearchPage, ChatPage
    h, m, ph, pl, asp, pu, s, c = HomePage(d), MinePage(d), PyqHomePage(d), PyqListPage(d), AlbumSelectPage(d), PyqUploadPage(d), SearchPage(d), ChatPage(d)

    from weixin_tool.auto_gui_driver.drivers.android import AndroidWeiXinGUIDriver
    class MockConf:
        wx_gui_driver_android_device_location = ''
        wx_ctl_ws = './testdata'
        wx_ctl_gui_driver_android_ws = '/data/local/tmp/weixin_auto_gui_ws'
    gui_driver = AndroidWeiXinGUIDriver(conf=MockConf())

    print(2131231)
    pass
