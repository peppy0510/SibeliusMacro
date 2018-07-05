# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import sys
import wx

from buttons import Buttons
from io import TextIOWrapper
from menubar import MenuBar
from objectlist import ListPanel
from preference import AppPreference
from statusbar import StatusBar

sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

LOGGING = False
VERSION = '0.1.1'
AUTHOR_NAME = 'Taehong Kim'
AUTHOR_EMAIL = 'peppy0510@hotmail.com'


class ToolPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, style=wx.LC_REPORT | wx.BORDER_DEFAULT)
        self.parent = parent
        self.SetBackgroundColour((180, 180, 180))
        self.BottomLine = wx.StaticLine(parent=self, size=(172, 1), style=wx.LI_HORIZONTAL)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        width, height = self.GetClientSize()
        self.BottomLine.SetRect((-2, height - 1, width + 4, 1))


class MainFrame(wx.Frame, Buttons, MenuBar, StatusBar):

    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          pos=wx.DefaultPosition, size=wx.Size(350, 733),
                          style=wx.CLIP_CHILDREN | wx.FRAME_SHAPED | wx.MINIMIZE_BOX |
                          wx.MAXIMIZE_BOX | wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION |
                          wx.RESIZE_BORDER | wx.TAB_TRAVERSAL | wx.BORDER_DEFAULT)

        self.version = VERSION
        self.author_name = AUTHOR_NAME
        self.author_email = AUTHOR_EMAIL
        self.SetTitle('SibeliusMacro')
        self.SetMinSize((350, 733))
        self.SetMaxSize((-1, -1))
        w, h = self.GetSize()
        width, height = wx.GetDisplaySize()
        self.ToolPanel = ToolPanel(self)
        self.ListPanel = ListPanel(self)
        self.InitializeMenuBar()
        self.InitializeButtons()
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
