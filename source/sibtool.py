# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import copy
import os
import sys
import time
import uiautomation
import win32api
import win32clipboard
import win32con
import win32gui


'''
{Ctrl}{Alt}{Shift}A
{Ctrl}{Alt}{Shift}C
{Ctrl}{Alt}{Shift}E
{Ctrl}{Alt}{Shift}G
{Ctrl}{Alt}{Shift}J
{Ctrl}{Alt}{Shift}N
{Ctrl}{Alt}{Shift}O
{Ctrl}{Alt}{Shift}Q
{Ctrl}{Alt}{Shift}W
{Ctrl}{Alt}{Shift}X
{Ctrl}{Alt}{Shift}Y
{Ctrl}{Alt}{Shift}Z
{Ctrl}{Alt}{Shift};
{Ctrl}{Alt}{Shift}'
{Ctrl}{Alt}{Shift}*
{Ctrl}{Alt}{Shift}-
{Ctrl}{Alt}{Shift}+
{Ctrl}{Alt}{Shift}`
{Ctrl}{Alt}{Shift}{F1}
{Ctrl}{Alt}{Shift}{F3}
{Ctrl}{Alt}{Shift}{F4}
{Ctrl}{Alt}{Shift}{F5}
{Ctrl}{Alt}{Shift}{F7}
{Ctrl}{Alt}{Shift}{F8}
{Ctrl}{Alt}{Shift}{F9}
{Ctrl}{Alt}{Shift}{F10}
{Ctrl}{Alt}{Shift}{F11}
{Ctrl}{Alt}{Shift}{F12}
{Ctrl}{Alt}{Shift}{Ins}
{Ctrl}{Alt}{Shift}{Del}
{Ctrl}{Alt}{Shift}{Home}
{Ctrl}{Alt}{Shift}{End}
{Ctrl}{Alt}{Shift}{PgUp}
{Ctrl}{Alt}{Shift}{PgDown}
'''


class keyboard():

    def __init__(self, parent):
        self.parent = parent

    def key2code(self, key):
        key.strip('{}')
        if key.startswith('{') and key.endswith('}'):
            code = uiautomation.Win32API.SpecialKeyDict[key.strip('{}').upper()]
        else:
            code = uiautomation.Win32API.CharacterDict[key]
        return code

    def down(self, keyslist):
        if isinstance(keyslist, (set, list, tuple)) is False:
            keyslist = [keyslist]
        for keys in keyslist:
            for key in keys.split('|'):
                uiautomation.Win32API.KeyDown(self.key2code(key), 0)

    def up(self, keyslist):
        if isinstance(keyslist, (set, list, tuple)) is False:
            keyslist = [keyslist]
        for keys in keyslist:
            for key in keys.split('|'):
                uiautomation.Win32API.KeyUp(self.key2code(key), 0)

    def esc(self):
        self.send('{ESC}' * 3, wait=10)

    def menu(self, keyslist):
        self.send(keyslist, wait=100)

    def bulk(self, keyslist):
        self.send(keyslist, wait=10)

    def send(self, keyslist, wait=50):
        if isinstance(keyslist, (set, list, tuple)) is False:
            keyslist = [keyslist]

        for ctrl in self.parent.controls:
            for keys in keyslist:
                for key in keys.split('|'):
                    ctrl.SendKeys(key, interval=wait * 0.001, waitTime=wait * 0.001)

    def get_text(self):
        self.bulk(['{CTRL}C'])
        return self.get_clipboard()

    def get_clipboard(self):
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data


class mouse():

    def move(self, x, y):
        win32api.SetCursorPos((int(x), int(y)))
        # for ctrl in self.controls:
        #     # ctrl.Click(x, y)

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


class control():

    def __init__(self, controls):

        if isinstance(controls, control):
            controls = copy.copy(controls.controls)
        if isinstance(controls, list) is False:
            self.controls = [controls]
        else:
            self.controls = controls

        self.key = keyboard(self)

    def get(self, typename=None, name=None, includes=[]):
        response = self._filter_(self.controls, typename, name, includes, 1)
        response = response if len(response) < 1 else [response[0]]
        self.controls = [ctrl for ctrl, inspect in response]
        return copy.copy(self)

    def filter(self, typename=None, name=None, includes=[], limit=None):
        response = self._filter_(self.controls, typename, name, includes, limit)
        self.controls = [ctrl for ctrl, inspect in response]
        return copy.copy(self)

    def _filter_(self, controls, typename=None, name=None,
                 includes=[], limit=None, depth=0, path=[0]):

        response = []
        includes = list(includes)

        if isinstance(controls, list) is False:
            controls = controls.GetChildren()
        else:
            for i in range(len(controls) - 1, -1, -1):
                ctrl = controls.pop(i)
                if hasattr(ctrl, 'GetRootControl'):
                    controls.insert(i, ctrl.GetRootControl())
                elif hasattr(ctrl, 'GetChildren'):
                    for children in ctrl.GetChildren():
                        controls.insert(i, children)

        class Inspect():

            def __init__(self, depth, path):
                self.depth = depth
                self.path = path

        for i, ctrl in enumerate(controls):
            include = True
            limited = limit is not None and len(response) >= limit

            if typename is not None and typename != ctrl.ControlTypeName:
                include = False
            if name is not None and name != ctrl.Name:
                include = False
            if False in [name in ctrl.Name for name in includes]:
                include = False

            if include and limited is False:
                response += [(ctrl, Inspect(depth, path + [i]))]

            limited = limit is not None and len(response) >= limit

            if limited is False:
                response += self._filter_(ctrl, typename, name,
                                          includes, limit, depth=depth + 1, path=path + [i])
        return response

    def sendkeys(self, keyslist, wait=50):
        if isinstance(keyslist, (set, list, tuple)) is False:
            keyslist = [keyslist]

        for ctrl in self.controls:
            for keys in keyslist:
                for key in keys.split('|'):
                    ctrl.SendKeys(key, interval=wait * 0.001, waitTime=wait * 0.001)

    def set_focus(self):
        for ctrl in self.controls:
            ctrl.SetFocus()

    def set_topmost(self, value):
        for ctrl in self.controls:
            if ctrl.CurrentIsTopmost() != value:
                ctrl.SetTopmost(value)

    def set_checkbox(self, value):
        for ctrl in self.controls:
            if ctrl.CurrentToggleState() != value:
                ctrl.Toggle()

    def sleep(self, sleep):
        time.sleep(sleep * 0.001)

    # def move(self, x, y):
    #     for ctrl in self.controls:
    #         ctrl.MoveCursor(x, y)
    def get_rect(self):

        class Rect():

            def __init__(self, left, top, right, bottom):
                self.x = left
                self.y = top
                self.width = right - left
                self.height = bottom - top

        rect = Rect(0, 0, 0, 0)
        for ctrl in self.controls:
            rect = Rect(*win32gui.GetWindowRect(ctrl.Handle))
            break

        return rect
