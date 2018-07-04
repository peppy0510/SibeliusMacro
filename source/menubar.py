# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import os
import subprocess
import wx


class MenuBar():

    def InitializeMenuBar(self):

        def make_menuitem(label, menu, bind=None):
            item = wx.MenuItem(menu, wx.ID_ANY, label, wx.EmptyString, wx.ITEM_CHECK)
            menu.Append(item)
            if bind is not None:
                self.Bind(wx.EVT_MENU, bind, item)
            return item

        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()
        make_menuitem('Exit', FileMenu, self.OnClose)

        MenuBar.Append(FileMenu, '&File')
        SettingsMenu = wx.Menu()
        self.AlwaysOnTopMenuItem = make_menuitem('Always on top', SettingsMenu, self.OnAlwaysOnTopToggle)
        SettingsMenu.AppendSeparator()
        self.AutoClearWhenImportMenuItem = make_menuitem('Auto clear when import', SettingsMenu, None)
        self.AutoClearWhenImportMenuItem.Check(True)
        self.AutoClearWhenBatchPrecessingMenuItem = make_menuitem('Auto clear after batch processing', SettingsMenu, None)
        self.AutoClearWhenBatchPrecessingMenuItem.Check(True)
        MenuBar.Append(SettingsMenu, '&Settings')

        HelpMenu = wx.Menu()
        self.HelpMenuAbout = make_menuitem('About', HelpMenu, self.OnHelpMenuAbout)
        MenuBar.Append(HelpMenu, '&Help')
        self.SetMenuBar(MenuBar)

    def OnHelpMenuAbout(self, event):

        width, height = (250, 135)
        x, y, w, h = self.GetScreenRect()
        x, y = (x + (w - width) / 2, y + (h - height) / 2)
        self.Dialog = wx.Dialog(self)
        self.Dialog.SetRect((x, y, width, height))
        self.Dialog.SetTitle('About')

        margin = 12
        width, height = self.Dialog.GetClientSize()
        message = 'SibeliusMacro %s' % (self.version)
        wx.StaticText(self.Dialog, label=message, pos=(margin, margin))
        message = 'Author: %s' % (self.author_name)
        wx.StaticText(self.Dialog, label=message, pos=(margin, margin + 18))
        message = 'Email: %s' % (self.author_email)
        wx.StaticText(self.Dialog, label=message, pos=(margin, margin + 18 * 2))

        self.Dialog.CloseButton = wx.Button(self.Dialog, label=u'Close')
        self.Dialog.CloseButton.SetRect((width - (78 + margin) * 1, margin + 60, 78, 24))
        self.Dialog.CloseButton.Bind(wx.EVT_BUTTON, lambda event: self.Dialog.Destroy())

        x, y = self.Dialog.CloseButton.GetPosition()
        self.Dialog.SetClientSize((self.Dialog.GetClientSize().x, y + 35))
        self.Dialog.ShowModal()

    def OnEditScript(self, event):
        script_path = self.FuncPanel.Tool.get_selected_script_path()
        subprocess.call([self.ScriptEditorPath, script_path])

    def OnOpenScript(self, event):
        script_path = self.FuncPanel.Tool.get_selected_script_path()
        path = os.path.dirname(script_path)
        subprocess.call(['explorer', path])
