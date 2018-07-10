# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import time
import win32api
import win32con
import win32gui


class Mouse():

    def move(self, x, y):
        win32api.SetCursorPos((int(x), int(y)))

    def click(self, x, y):
        position = self.get_position()
        self.move(x, y)
        self.down(x, y)
        self.up(x, y)
        self.move(position.x, position.y)
        time.sleep(0.08)

    def down(self, x, y):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, int(x), int(x), 0, 0)

    def up(self, x, y):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, int(x), int(x), 0, 0)

    def get_position(self):
        flags, hcursor, (x, y) = win32gui.GetCursorInfo()

        class Cursor():

            def __init__(self, x, y):
                self.x = x
                self.y = y

        return Cursor(x, y)
