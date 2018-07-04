# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import os
import wx
from mpath import mpath


class StatusWatcher(wx.Timer):

    def __init__(self, parent):
        wx.Timer.__init__(self)
        self.parent = parent
        self.interval = 100
        self.script_md5 = ''
        self.Start(self.interval)

    def Notify(self):
        return
        # if hasattr(self.parent, 'parent') is False:
        #     return
        # if hasattr(self.parent.parent, 'ListPanel') is False:
        #     return
        # if hasattr(self.parent.parent.ListPanel, 'OLV') is False:
        #     return
        items = len(self.parent.parent.ListPanel.OLV.GetObjects())
        selected = len(self.parent.parent.ListPanel.OLV.GetSelectedObjects())
        message = u'Selected %d / %d items' % (selected, items)

        self.parent.Freeze()
        self.parent.LeftText.SetLabel(message)
        margin = 4
        w, h = self.parent.GetClientSize()
        self.parent.LeftText.SetRect(
            (margin, margin, w - margin * 2, h - margin * 2))
        self.parent.Thaw()

        # path = self.parent.parent.FuncPanel.Tool.get_selected_script_path()
        # if os.path.isfile(path):
        #     md5 = mpath(path).get_md5()
        #     if md5 != self.script_md5:
        #         self.script_md5 = md5
        #         self.parent.parent.AutoPreview()


class StatusPanel(wx.StatusBar):

    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)
        self.parent = parent
        self.StatusWatcher = StatusWatcher(self)
        self.LeftText = wx.StaticText(self, -1, '')
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        margin = 4
        w, h = self.GetClientSize()
        self.LeftText.SetRect((margin, margin, w / 2 - margin * 2, h - margin * 2))


class StatusBar():

    def InitializeStatusBar(self):
        self.StatusBar = StatusPanel(self)
        self.SetStatusBar(self.StatusBar)
