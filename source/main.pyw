# encoding: utf-8


__appname__ = 'SibeliusMacro'
__version__ = '0.2.1'
__author__ = 'Taehong Kim'
__email__ = 'peppy0510@hotmail.com'
__license__ = ''
__doc__ = '''
'''


import os
import sys
import wx

from listpanel import ListPanel
from menubar import MenuBar
from preference import AppPreference
from statusbar import StatusBar
from toolpanel import ToolPanel
from wininstance import get_current_real_cwq
from wininstance import kill_existing_instances

LOGGING = False
FRAME_MIN_SIZE = wx.Size(350, 795)
FRAME_MIN_SIZE = wx.Size(186, 795)
FRAME_MAX_SIZE = (-1, -1)
FRAME_MAX_SIZE = FRAME_MIN_SIZE
# wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.SYSTEM_MENU


class MainFrame(wx.Frame, MenuBar, StatusBar):

    icon_path = os.path.join('assets', 'icon', 'icon.ico')

    def __init__(self, parent=None):
        self.defaultStyle = wx.CLIP_CHILDREN | wx.FRAME_SHAPED | wx.CLOSE_BOX | \
            wx.CAPTION | wx.RESIZE_BORDER | wx.TAB_TRAVERSAL | wx.BORDER_DEFAULT | wx.STAY_ON_TOP
        wx.Frame.__init__(self, parent, id=wx.ID_ANY,
                          pos=wx.DefaultPosition, size=FRAME_MIN_SIZE,
                          style=self.defaultStyle)

        self.version = __version__
        self.author_name = __author__
        self.author_email = __email__
        self.SetTitle(__appname__)
        self.SetMinSize(FRAME_MIN_SIZE)
        self.SetMaxSize(FRAME_MAX_SIZE)

        icon = wx.Icon()

        if hasattr(sys, '_MEIPASS'):
            self.icon_path = os.path.join(sys._MEIPASS, self.icon_path)
        else:
            cwd = os.path.dirname(get_current_real_cwq())
            self.icon_path = os.path.join(cwd, self.icon_path)

        # print(self.icon_path)
        icon.CopyFromBitmap(wx.Bitmap(self.icon_path, wx.BITMAP_TYPE_ANY))
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
    kill_existing_instances()
    main()
