# coding:utf-8
from uiautomator2 import Device

DEFAULT_SECONDS = 10


class BasePage(object):
    """
    第一层：对uiAutomator2进行二次封装，定义一个所有页面都继承的BasePage
    封装uiAutomator2基本方法，如：元素定位，元素等待，导航页面等
    不需要全部封装，用到多少就封装多少
    """

    def __init__(self, device: Device):
        self.d = device

    def by_id(self, id_name):
        """通过id定位单个元素"""
        try:
            self.d.implicitly_wait(DEFAULT_SECONDS)
            return self.d(resourceId=id_name)
        except Exception as e:
            print("页面中没有找到id为%s的元素" % id_name)
            raise e

    def by_id_matches(self, id_name):
        """通过id关键字匹配定位单个元素"""
        try:
            self.d.implicitly_wait(DEFAULT_SECONDS)
            return self.d(resourceIdMatches=id_name)
        except Exception as e:
            print("页面中没有找到id为%s的元素" % id_name)
            raise e

    def by_class(self, class_name):
        """通过class定位单个元素"""
        try:
            self.d.implicitly_wait(DEFAULT_SECONDS)
            return self.d(className=class_name)
        except Exception as e:
            print("页面中没有找到class为%s的元素" % class_name)
            raise e

    def by_text(self, text_name):
        """通过text定位单个元素"""
        try:
            self.d.implicitly_wait(DEFAULT_SECONDS)
            return self.d(text=text_name)
        except Exception as e:
            print("页面中没有找到text为%s的元素" % text_name)
            raise e

    def by_class_text(self, class_name, text_name):
        """通过text和class多重定位某个元素"""
        try:
            self.d.implicitly_wait(DEFAULT_SECONDS)
            return self.d(className=class_name, text=text_name)
        except Exception as e:
            print("页面中没有找到class为%s、text为%s的元素" % (class_name, text_name))
            raise e

    def by_text_match(self, text_match):
        """通过textMatches关键字匹配定位单个元素"""
        try:
            self.d.implicitly_wait(DEFAULT_SECONDS)
            return self.d(textMatches=text_match)
        except Exception as e:
            print("页面中没有找到text为%s的元素" % text_match)
            raise e

    def by_desc(self, desc_name):
        """通过description定位单个元素"""
        try:
            self.d.implicitly_wait(DEFAULT_SECONDS)
            return self.d(description=desc_name)
        except Exception as e:
            print("页面中没有找到desc为%s的元素" % desc_name)
            raise e

    def by_xpath(self, xpath):
        """通过xpath定位单个元素【特别注意：只能用d.xpath，千万不能用d(xpath)】"""
        try:
            self.d.implicitly_wait(DEFAULT_SECONDS)
            return self.d.xpath(xpath)
        except Exception as e:
            print("页面中没有找到xpath为%s的元素" % xpath)
            raise e

    def by_id_text(self, id_name, text_name):
        """通过id和text多重定位"""
        try:
            self.d.implicitly_wait(DEFAULT_SECONDS)
            return self.d(resourceId=id_name, text=text_name)
        except Exception as e:
            print("页面中没有找到resourceId、text为%s、%s的元素" % (id_name, text_name))
            raise e

    def find_child_by_id_class(self, id_name, class_name):
        """通过id和class定位一组元素，并查找子元素"""
        try:
            self.d.implicitly_wait(DEFAULT_SECONDS)
            return self.d(resourceId=id_name).child(className=class_name)
        except Exception as e:
            print("页面中没有找到resourceId为%s、className为%s的元素" % (id_name, class_name))
            raise e

    def is_text_loc(self, text):
        """定位某个文本对象（多用于判断某个文本是否存在）"""
        return self.by_text(text_name=text)

    def is_id_loc(self, id):
        """定位某个id对象（多用于判断某个id是否存在）"""
        return self.by_id(id_name=id)

    def fling_forward(self):
        """当前页面向上滑动"""
        return self.d(scrollable=True).fling.vert.forward()

    def swipe_up(self):
        """当前页面向上滑动，步长为10"""
        return self.d(scrollable=True).swipe("up", steps=10)

    def swipe_down(self):
        """当前页面向下滑动，步长为10"""
        return self.d(scrollable=True).swipe("down", steps=10)

    def swipe_left(self):
        """当前页面向左滑动，步长为10"""
        return self.d(scrollable=True).swipe("left", steps=10)

    def swipe_right(self):
        """当前页面向右滑动，步长为10"""
        return self.d(scrollable=True).swipe("right", steps=10)