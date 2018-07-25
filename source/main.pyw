# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import os
import sys
import wx

from listpanel import ListPanel
from menubar import MenuBar
from preference import AppPreference
from statusbar import StatusBar
from toolpanel import ToolPanel

LOGGING = False
VERSION = '0.1.1'
AUTHOR_NAME = 'Taehong Kim'
AUTHOR_EMAIL = 'peppy0510@hotmail.com'
FRAME_MIN_SIZE = wx.Size(350, 795)
FRAME_MIN_SIZE = wx.Size(186, 795)
FRAME_MAX_SIZE = (-1, -1)
FRAME_MAX_SIZE = FRAME_MIN_SIZE
# wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU


class MainFrame(wx.Frame, MenuBar, StatusBar):

    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          pos=wx.DefaultPosition, size=FRAME_MIN_SIZE,
                          style=wx.CLIP_CHILDREN | wx.FRAME_SHAPED | wx.CLOSE_BOX | wx.CAPTION |
                          wx.RESIZE_BORDER | wx.TAB_TRAVERSAL | wx.BORDER_DEFAULT | wx.STAY_ON_TOP)

        self.version = VERSION
        self.author_name = AUTHOR_NAME
        self.author_email = AUTHOR_EMAIL
        self.SetTitle('SibeliusMacro')
        self.SetMinSize(FRAME_MIN_SIZE)
        self.SetMaxSize(FRAME_MAX_SIZE)

        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(os.path.join(os.path.dirname(
            os.path.dirname(__file__)), 'assets', 'icon.ico'), wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

        self.ToolPanel = ToolPanel(self)
        self.ListPanel = ListPanel(self)
        self.InitializeMenuBar()
        self.InitializeStatusBar()
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_SIZE, self.OnSize, self)
        self.Preference = AppPreference(self, 'SibeliusMacro', 'settings.json')
        self.Preference.LoadPreference()
        self.ListPanel.SortList()
        self.Show(True)
        self.SetFocus()

    def OnSize(self, event):
        center = 170
        width, height = self.GetClientSize()
        self.ToolPanel.SetRect(wx.Rect(0, 0, center, height))
        self.ListPanel.SetRect(wx.Rect(center, 0, width - center, height))

    def OnClose(self, event):
        self.StatusBar.StatusWatcher.Stop()
        self.Preference.SavePreference()
        self.Destroy()

    def OnClearButton(self, event):
        selected = self.ListPanel.OLV.GetObjects()
        self.ListPanel.OLV.RemoveObjects(selected)


class App(wx.App):

    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)

    def OnInit(self):
        frame = MainFrame()
        frame.Show()
        return True

    def __del__(self):
        pass


def main():
    app = App()
    app.MainLoop()


if __name__ == '__main__':
    main()
