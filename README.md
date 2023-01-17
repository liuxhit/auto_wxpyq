# python环境
```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements
```

# 电脑安装adb
...

# 手机(安卓)打开usb调试

# 连接手机
```shell
# windows安装手机驱动
# macos如果找不到设备：https://blog.csdn.net/adyw2565876/article/details/50286003
adb devices  # 获取手机序列号
python -m uiautomator2 init --serial 2d479368  # 2d479368是上一步获取的序列号
adb tcpip 5555  # 允许从wifi连接手机
```

# 测试数据
```shell
# 在 ./testdata 目录下， test_excel_file.txt 文件
# 运行(最后加上-d参数不会真实发朋友圈)：
python main.py -f ./testdata/test_excel_file.txt --file_format test_text --wx_ctl_cls weixin_tool.gui_weixin_controller.GUIWeiXinController --wx_ctl_gui_driver_cls weixin_tool.auto_gui_driver.drivers.android.AndroidWeiXinGUIDriver -d
```
