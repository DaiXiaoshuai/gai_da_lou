import json
import os
from time import sleep
import cv2

from tecent_ocr import TecentOcr


def start_tao_bao():
    """
    打开手机淘宝
    :return:
    """
    os.system("adb shell am force-stop com.taobao.taobao")  # 强制关闭淘宝
    os.system("adb shell am start -n com.taobao.taobao/com.taobao.tao.TBMainActivity")  # 启动淘宝


def tap(x, y):
    """手机模拟点击，需要在开发者模式下开启相应权限"""
    os.system('adb shell input tap %d %d' % (x, y))


def swipe(x1, y1, x2, y2):
    """手机模拟滑动"""
    os.system('adb shell input swipe %d %d %d %d' % (x1, y1, x2, y2))


def tap_back():
    """模拟点击返回键"""
    os.system('adb shell input keyevent 4')  # 返回


def init_to_task_window():
    """启动淘宝，并进入盖大楼的任务界面"""
    start_tao_bao()
    sleep(5)
    os.system('adb shell input tap %d %d' % (params['ModuleX'], params['ModuleY']))  # 盖大楼板块
    sleep(5)
    os.system('adb shell input tap %d %d' % (params['TaskIconX'], params['TaskIconY']))  # 任务图标
    sleep(2)


def click(event, x, y, flags, param):
    """手机界面投影到电脑上时，屏幕点击的回调"""
    if event == cv2.EVENT_LBUTTONDOWN:
        cmd = str('adb shell input tap %d %d' % (x, y))
        os.system(cmd)
        print(x, y)


# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
# cv2.resizeWindow("image", 432, 864)
# cv2.setMouseCallback('image', click)


def get_screen_shot():
    """获取当前手机界面截图"""
    os.system('adb shell screencap -p /sdcard/01.png')
    os.system('adb pull /sdcard/01.png')
    image = cv2.imread("01.png")
    return image


def refresh():
    cv2.imshow('image', get_screen_shot())
    cv2.waitKey(10)


def hasTask(resp):
    """
    ocr识别的返回结果中，是否包含"去浏览"任务
    :return:
    """
    for item in resp.TextDetections:
        if item.DetectedText == "去浏览":
            return True
    return False


f = open('config.json', 'r', encoding='utf-8')
text = f.read()
f.close()
params = json.loads(text)
cut_position_x = params['OcrCutStartX']  # 屏幕截图中用于ocr识别部分的起始x像素坐标，此值需要根据手机屏幕大小进行适配
cut_position_y = params['OcrCutStartY']  # y像素坐标
init_to_task_window()
button_area = get_screen_shot()[cut_position_y:params['OcrCutEndY'], cut_position_x:params['OcrCutEndX']]
ocr = TecentOcr()
result = ocr.identify(button_area)
while hasTask(result):
    for item in result.TextDetections:
        if item.DetectedText == "去浏览":
            tap(cut_position_x + (item.Polygon[0].X + item.Polygon[1].X)/2,
                cut_position_y + (item.Polygon[0].Y + item.Polygon[2].Y)/2)
            sleep(2)
            swipe(500, 1200, 500, 500)
            swipe(500, 1200, 500, 500)
            sleep(20)
            tap_back()
            sleep(1)
    button_area = get_screen_shot()[cut_position_y:params['OcrCutEndY'], cut_position_x:params['OcrCutEndX']]
    result = ocr.identify(button_area)
    if result.TextDetections[0].DetectedText != "去分享":
        init_to_task_window()
        button_area = get_screen_shot()[cut_position_y:params['OcrCutEndY'], cut_position_x:params['OcrCutEndX']]
        result = ocr.identify(button_area)
