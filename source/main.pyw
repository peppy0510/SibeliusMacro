# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import os
import win32con
import wx
# import glob
# from mpath import mpath
import wx.grid as gridlib


from buttons import Buttons
from menubar import MenuBar
from objectlist import ListPanel
from preference import AppPreference
from statusbar import StatusBar


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


# class FuncPanelTool(wx.Panel, Buttons):

#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent=parent)
#         self.parent = parent
#         self.SetBackgroundColour((180, 180, 180))
        # self.InitializeToolButtons()
        # self.LoadScriptDirectory()
        # self.LoadScriptFile()

    # def LoadScriptDirectory(self, event=None):

    #     if not event:
    #         root = os.path.sep.join([os.getcwd(), 'scripts'])
    #         paths = glob.glob(os.path.join(root, '*'))
    #         self.ScriptDirectory.Clear()
    #         names = [os.path.splitext(os.path.basename(path))[0]
    #                  for path in paths if os.path.isdir(path)]
    #         if len(names) != 0:
    #             self.ScriptDirectory.SetItems(names)
    #             self.ScriptDirectory.SetValue(names[0])
    #     else:
    #         self.LoadScriptFile()

    # def LoadScriptFile(self, event=None):

    #     # self.parent.parent.StatusBar.StatusWatcher.script_md5 =

    #     if not event:
    #         root = os.path.sep.join(
    #             [os.getcwd(), 'scripts', self.ScriptDirectory.GetValue()])
    #         paths = glob.glob(os.path.join(root, '*.py'))
    #         self.ScriptFile.Clear()
    #         names = [os.path.splitext(os.path.basename(path))[0]
    #                  for path in paths if os.path.isfile(path)]
    #         if len(names) != 0:
    #             self.ScriptFile.SetItems(names)
    #             self.ScriptFile.SetValue(names[0])

    #     self.parent.parent.AutoPreview()

    # def get_selected_script_path(self):
    #     directory = self.ScriptDirectory.GetValue()
    #     script_name = self.ScriptFile.GetValue()
    #     name = os.path.sep.join([os.getcwd(), 'scripts', directory, script_name])
    #     return os.path.join('%s.py' % (name))


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

        # pasteID = wx.NewId()
        # aTable = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('V'), pasteID), ])
        # self.SetAcceleratorTable(aTable)
        # self.Bind(wx.EVT_MENU, OnPaste, pasteID)

        # self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPress)
        # self.Bind(wx.EVT_KEY_UP, self.OnKeyPress)
        # self.Bind(wx.EVT_CHAR, self.OnKeyPress)
        # import threading
        # threading.Thread()
        self.SetFocus()
        # self.regHotKey()
        hot_key_id = wx.NewId()
        self.RegisterHotKey(hot_key_id, win32con.VK_F1, win32con.VK_F1)
        self.Bind(wx.EVT_HOTKEY, self.handleHotKey, id=hot_key_id)

    def __waitThenClose(self):

        for x in range(0, 10):
            pass
            # print "Sleeping..."
            # sleep(1)

        wx.CallAfter(self.closeOpenDialogs)
        wx.CallAfter(self.Close, True)

    def regHotKey(self):
        pass
        """
        This function registers the hotkey Alt+F1 with id=100
        """
        self.hotKeyId = wx.NewId()
        self.RegisterHotKey(
            self.hotKeyId,  # a unique ID for this hotkey
            win32con.VK_F1,  # the modifier key
            win32con.VK_F1)  # the key to watch for
        # self.RegisterHotKey(
        #     self.hotKeyId,  # a unique ID for this hotkey
        #     win32con.MOD_ALT,  # the modifier key
        #     win32con.VK_F1)  # the key to watch for
        # self.RegisterHotKey(self.hotKeyId,
        #                     wx.MOD_CONTROL | wx.MOD_SHIFT,
        #                     ord('x'))
        # self.RegisterHotKey(
        #     self.hotKeyId,  # a unique ID for this hotkey
        #     win32con.MOD_ALT,  # the modifier key
        #     win32con.VK_F1)  # the key to watch for
        self.Dialog = None

    def handleHotKey(self, event):
        print('ALT F1')
        # if hasattr(self.ToolPanel, 'Dialog') and self.ToolPanel.Dialog:
        # if hasattr(self, 'Dialog') and self.Dialog:
        # print(hasattr(self, 'Dialog'))

        # if hasattr(self.Dialog:
        if hasattr(self, 'Dialog') and self.Dialog:
            self.Dialog.OnCancelButton()
            print('do hot key actions')

        """
        Prints a simple message when a hotkey event is received.
        """

    def OnKeyPress(self, event):
        keycode = event.GetKeyCode()
        print('OnKeyPress', keycode)
        event.Skip()

    def OnSize(self, event):
        center = 170
        width, height = self.GetClientSize()
        self.ToolPanel.SetRect(wx.Rect(0, 0, center, height))
        self.ListPanel.SetRect(wx.Rect(center, 0, width - center, height))

    def OnClose(self, event):
        self.StatusBar.StatusWatcher.Stop()
        self.Preference.SavePreference()
        self.Destroy()

    #     self.ListPanel.Freeze()
    #     self.ListPanel.OLV.SetObjects(ITEMS)
    #     self.ListPanel.SortList()
    #     self.ListPanel.Thaw()

    #     script_path = tool.get_selected_script_path()
    #     with open(script_path, 'rb') as file:
    #         script = file.read()

    #     items = self.ListPanel.OLV.GetObjects()

    #     for i, item in enumerate(items):
    #         item.revert()
    #         item.set_serialize_index(i)
    #         if tool.EnableScript.GetValue():
    #             item = run_rename_script(item, items, script)

    #         if tool.EnableSerilize.GetValue():
    #             name = item.get_basename()
    #             zeros = tool.SerilizeZeros.GetValue()
    #             offset = tool.SerilizeStart.GetValue()
    #             position = tool.SerilizePosition.GetValue()
    #             reverse = tool.SerilizeTail.GetValue()
    #             value = str(i + offset)
    #             value = value.zfill(zeros)
    #             item.insert_string(value, position, reverse=reverse)

    #         if tool.EnableInsertString.GetValue():
    #             value = tool.InsertStringText.GetValue()
    #             position = tool.InsertStringPosition.GetValue()
    #             reverse = tool.InsertStringTail.GetValue()
    #             item.insert_string(value, position, reverse=reverse)

    #         if tool.EnableFindReplace.GetValue() and len(tool.FindStringText.GetValue()) > 0:
    #             find = tool.FindStringText.GetValue()
    #             replace = tool.ReplaceStringText.GetValue()
    #             if tool.EnableSkipExtension.GetValue():
    #                 name = item.get_basename()
    #                 item.set_basename(name.replace(find, replace))
    #             else:
    #                 name = item.get_filename()
    #                 item.set_filename(name.replace(find, replace))

    #         # • · « » × § ¤ ‡ †
    #         if item.get_filename() == item.original_filename:
    #             item.status = u' '
    #         else:
    #             item.status = u'•'
    #         if item.has_to_remove:
    #             item.status = u'¤'
    #     self.ListPanel.Freeze()
    #     self.ListPanel.OLV.SetObjects(items)
    #     self.ListPanel.SortList()
    #     self.ListPanel.Thaw()

    def OnRenameButton(self, event):
        pass

    #     self.ListPanel.Freeze()
    #     self.ListPanel.OLV.SetObjects(ITEMS)
    #     self.ListPanel.SortList()
    #     self.ListPanel.Thaw()
    #     self.AutoPreview()

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
    # import sys
    # from io import TextIOWrapper
    # sys.stdout = TextIOWrapper(sys.stdout.buffer,
    #                            encoding='utf-8', errors='replace')
    main()
