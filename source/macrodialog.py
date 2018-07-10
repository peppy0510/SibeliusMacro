# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import copy
import macro
import os
import queue
import sys
import win32api
import win32con
import win32gui
import wx

# sys.path.insert(0, os.path.join(os.path.basename(__name__), 'macro'))


class MacroDialogStatus():

    def __init__(self, parent):
        self.parent = parent
        self.total = len(self.parent.macros)
        self.target_total = sum([len(v.targets) for v in self.parent.macros])
        self.label = ''
        self.done = 0
        self.target_done = 0
        self.target_left = 0
        self.left = self.total

    def count(self, label):
        if self.label != label:
            self.done += 1
            self.left -= 1
        self.label = label
        self.target_done += 1
        self.target_left -= 1
        self.parent.DynamicMessage.SetLabel('%s (%d/%d)' % (self.label, self.done, self.total))
        width, height = self.parent.ProgressBar.GetSize()
        width = width * (self.target_done / self.target_total)
        self.parent.ProgressBar.Indicator.SetSize((width, height))


class MouseCursorPosition():

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Macro():

    def __init__(self, name, label, targets):
        self.name = copy.deepcopy(name)
        self.label = copy.deepcopy(label)
        self.targets = copy.deepcopy(targets)


class MacroDialogTimer(wx.Timer):

    def __init__(self, parent):
        wx.Timer.__init__(self)
        self.parent = parent
        self.interval = 0.1
        self.started = False
        self.thread = None
        self.thread_stop_queue = queue.Queue()
        self.status = MacroDialogStatus(self.parent)
        self.Start(self.interval)
        self.targets = []
        self.macro_name = ''
        self.macro_label = ''
        # win32api.SetCursorPos((int(x), int(y)))
        # self.total_count = len(self.parent.macros)
        # self.params = self.parent.parent.GetSibeliusParams()

    def Notify(self):

        if self.thread and not self.thread.isAlive():
            self.thread = None

        if len(self.parent.macros) > 0 and len(self.targets) == 0:
            v = self.parent.macros.pop(0)
            self.targets = v.targets
            self.macro_label = v.label

        if len(self.targets) > 0 and self.thread is None:
            target = self.targets.pop(0)
            self.status.count(self.macro_label)
            self.thread = macro.Sibelius(self.parent.params, targets=[target]).thread

        if len(self.parent.macros) == 0 and len(self.targets) == 0 and self.thread is None:
            self.parent.OnCancelButton()


class ProgressBar(wx.Panel):

    def __init__(self, parent, pos, width, height=3):
        wx.Panel.__init__(self, parent=parent, pos=pos)
        self.parent = parent
        self.SetSize((width, height))
        self.SetBackgroundColour((255, 255, 255))
        self.Indicator = wx.Panel(self)
        self.Indicator.SetBackgroundColour((80, 80, 80))
        self.Indicator.SetRect((0, 0, 0, self.GetSize().height))


class MacroDialog(wx.Dialog):

    def __init__(self, parent, macros, macro_values, *args, **kwargs):
        wx.Dialog.__init__(self, parent, *args, **kwargs, style=wx.CLOSE_BOX | wx.STAY_ON_TOP)
        self.parent = parent
        self.macros = [Macro(v.name, v.label, v.targets) for v in macros]
        self.macro_values = macro_values
        self.params = self.GetSibeliusParams()
        self.SetBackgroundColour((255, 100, 100))
        self.stop_key_pressed = False
        width, height = (230, 135)
        x, y, w, h = self.parent.GetScreenRect()
        x, y = (x + (w - width) / 2, y + (h - height) / 2)
        self.SetRect((x, y, width, height))

        page_margin = 12
        line_margin = 2
        width, height = self.GetClientSize()
        message = 'Processing macro, please wait ...'
        StaticMessage = wx.StaticText(self, label=message, pos=(page_margin, page_margin))

        x, y, width, height = StaticMessage.GetRect()
        message = 'You can cancel with [BREAK] key.'
        StaticMessage = wx.StaticText(self, label=message, pos=(page_margin, y + height + line_margin))

        x, y, width, height = StaticMessage.GetRect()
        self.DynamicMessage = wx.StaticText(self, label='', pos=(page_margin, y + height + line_margin))
        x, y, width, height = self.DynamicMessage.GetRect()

        self.ProgressBar = ProgressBar(self,
                                       pos=(page_margin, y + height + line_margin + 4),
                                       width=self.GetClientSize().width - page_margin * 2)
        x, y, width, height = self.ProgressBar.GetRect()

        self.SetClientSize((self.GetClientSize().x, y + height + line_margin + page_margin))

        self.timer = MacroDialogTimer(self)
        self.Bind(wx.EVT_CLOSE, self.OnCancelButton)

        newId = wx.NewId()
        self.RegisterHotKey(newId, win32con.VK_F1, win32con.VK_PAUSE)
        # self.RegisterHotKey(newId, win32con.VK_F1, win32con.VK_F5)
        self.Bind(wx.EVT_HOTKEY, self.OnHotKeyPressed, id=newId)
        self.SetFocus()

        # _, _, (x, y) = win32gui.GetCursorInfo()
        # self.cursor_position = MouseCursorPosition(x, y)
        # self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseCursorMove)
        # self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseCursorMove)

        # cursor = wx.Cursor(wx.CURSOR_NO_ENTRY)  # wx.CURSOR_ARROW
        # self.SetCursor(cursor)
        self.ShowModal()

    # def OnMouseCursorMove(self, event=None):
    #     print('xxxxxxxxx')
    #     win32api.SetCursorPos((int(self.cursor_position.x), int(self.cursor_position.y)))

    def GetSibeliusParams(self):
        macro.SibeliusParams()
        params = {}
        for v in self.macro_values:
            params.update({v.param: v.value.GetValue()})
        return macro.SibeliusParams(**params)

    def OnHotKeyPressed(self, event):
        if not self.stop_key_pressed:
            self.stop_key_pressed = True
            self.macros = []
            self.timer.targets = []
            # message = self.DynamicMessage.GetLabel()
            # self.DynamicMessage.SetLabel('Cancel ' + message)
            # self.DynamicMessage.SetLabel('Cancel')

    def OnCancelButton(self, event=None):
        self.timer.macros = []
        if self.timer is not None and self.timer.thread is not None:
            self.timer.thread_stop_queue.put(True)
            self.timer.thread.join()

        if self.timer is not None and self.timer.IsRunning():
            self.timer.Stop()

        self.timer.Destroy()
        self.Destroy()
        self.parent.SetFocus()
        self.parent.Raise()

    # def OnPaint(self, event):
    #     width, height = self.ProgressBar.GetClientSize()
    #     width = width * (self.timer.status.target_done / self.timer.status.target_total)
    #     # print(width)
    #     dc = wx.PaintDC(self.ProgressBar)
    #     color = '#D0D0D0'
    #     dc.SetPen(wx.Pen(color))
    #     dc.SetBrush(wx.Brush(color))
    #     dc.DrawRectangle(0, 0, width, height)
