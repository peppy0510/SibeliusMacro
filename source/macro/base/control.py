# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import copy
import time
import win32gui

from .keyboard import Keyboard


class Control():

    def __init__(self, controls):

        if isinstance(controls, Control):
            controls = copy.copy(controls.controls)
        if isinstance(controls, list) is False:
            self.controls = [controls]
        else:
            self.controls = controls

        self.key = Keyboard(self)

    def get(self, typename=None, name=None, includes=[], excludes=[]):
        response = self._filter_(self.controls, typename, name, includes, excludes, 1)
        response = response if len(response) < 1 else [response[0]]
        self.controls = [ctrl for ctrl, inspect in response]
        return copy.copy(self)

    def filter(self, typename=None, name=None, includes=[], excludes=[], limit=None):
        response = self._filter_(self.controls, typename, name, includes, excludes, limit)
        self.controls = [ctrl for ctrl, inspect in response]
        return copy.copy(self)

    def _filter_(self, controls, typename=None, name=None,
                 includes=[], excludes=[], limit=None, depth=0, path=[0]):

        response = []
        includes = list(includes)
        excludes = list(excludes)

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
            # print(ctrl.Name)
            include = True
            limited = limit is not None and len(response) >= limit

            if typename is not None and typename != ctrl.ControlTypeName:
                include = False
            if name is not None and name != ctrl.Name:
                include = False
            if False in [v in ctrl.Name for v in includes]:
                include = False
            if True in [v in ctrl.Name for v in excludes]:
                include = False

            if include and limited is False:
                response += [(ctrl, Inspect(depth, path + [i]))]

            limited = limit is not None and len(response) >= limit

            if limited is False:
                response += self._filter_(ctrl, typename, name, includes, excludes,
                                          limit, depth=depth + 1, path=path + [i])
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

    def selectall(self):
        self.key.send(['{CTRL}A'])
        modal = Control(copy.copy(self.controls)).get(
            'WindowControl', name='there is nothing to select')
        modal.key.bulk(['{Enter}'])
