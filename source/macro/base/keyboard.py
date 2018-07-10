# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import uiautomation
import win32clipboard


class Keyboard():

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
