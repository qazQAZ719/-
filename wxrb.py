from PIL import ImageGrab
import aircv
import cv2
import numpy
import win32api
import win32con
import sys, time



def screen():
    # 截图
    img = ImageGrab.grab((0, 0, 360, 710))
    #     img.save("1.png")
    return img


def findrb(pic):
    pic = cv2.cvtColor(numpy.asarray(pic), cv2.COLOR_RGB2BGR)
    rb = cv2.imread("./rb.png")
    pos = aircv.find_template(pic, rb, 0.99)
    if (pos == None):
        sys.exit()
    circle_center_pos = pos['result']
    target = (int(circle_center_pos[0]), int(circle_center_pos[1]))
    return target


def winop(target):
    # 打开红包
    win32api.SetCursorPos([target[0], target[1]])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.6)
    # 抢红包
    win32api.SetCursorPos([180, 410])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(1)
    # 退出
    win32api.SetCursorPos([20, 70])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    count = 1
    return count


if __name__ == "__main__":
    count = 0
    img = screen()
    target = findrb(img)
    print(target)
    if target != None:
        count += winop(target)
        print("抢到第{}个红包".format(count))