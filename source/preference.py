# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import json
import os
import sys
import wx


class AppPreferenceBase():

    def __init__(self, parent, dirname, filename):
        self.parent = parent
        self.value = {}
        self.dirname = dirname
        self.filename = filename
        self.path = self._get_preference_path_(dirname, filename)

    def get(self, key, load=False):
        '''
        로드된 사용자 설정값을 반환.
        '''
        if load:
            self.load()
        if key in self.value:
            return self.value[key]
        return None

    def set(self, key, value, save=False):
        '''
        사용자 설정값을 변경.
        '''
        self.value.update({key: value})
        if save:
            self.save()

    def load(self):
        '''
        사용자 설정파일을 읽음.
        '''
        self.value = {}
        if os.path.isfile(self.path):
            with open(self.path, 'r', encoding='utf-8') as file:
                try:
                    value = json.loads(file.read())
                    self.value = value
                except Exception:
                    self.value = {}

    def save(self):
        '''
        사용자 설정파일을 저장.
        '''
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.value, sort_keys=True, indent=4))

    def _get_preference_path_(self, dirname, filename):
        '''
        사용자 설정파일의 위치를 반환.
        '''
        abspath = os.path.join(self._get_user_document_path_(), dirname)
        if os.path.isdir(abspath) is False:
            os.mkdir(abspath)
        path = os.path.join(abspath, filename)
        return path

    def _get_user_document_path_(self):
        '''
        사용자 도큐먼트 디렉토리의 위치를 반환.
        '''
        if sys.platform.startswith('win'):
            path = os.path.abspath(os.path.join(
                os.path.expanduser(r'~'), r'Documents'))
            if os.path.isdir(path):
                return path
            path = os.path.abspath(os.path.join(
                os.path.expanduser(r'~'), r'My Documents'))
            if os.path.isdir(path):
                return path
            return None
        elif sys.platform.startswith('darwin'):
            path = os.path.abspath(os.path.join(
                os.path.expanduser(r'~'), r'Documents'))
            if os.path.isdir(path):
                return path
            return None


class AppPreference(AppPreferenceBase):

    def SavePreference(self):
        '''
        모든 설정값을 사용자 설정파일에 저장.
        '''
        self.set('Rect', tuple(self.parent.GetRect()))
        self.set('AlwaysOnTopMenuItem', self.parent.AlwaysOnTopMenuItem.IsChecked())
        # self.set('AutoClearWhenImportMenuItem', self.parent.AutoClearWhenImportMenuItem.IsChecked())
        # self.set('AutoClearWhenBatchPrecessingMenuItem', self.parent.AutoClearWhenBatchPrecessingMenuItem.IsChecked())
        self.set('PresetComboBox', self.parent.ToolPanel.PresetComboBox.GetValue())

        for macro in self.parent.ToolPanel.MacroFunctions:
            self.set(macro.name, macro.toggle.GetValue())

        for macro in self.parent.ToolPanel.MacroValues:
            self.set(macro.name, macro.value.GetValue())

        self.save()

    def LoadPreference(self):
        '''
        모든 설정값을 사용자 설정파일에서 읽음.
        '''
        self.load()

        displays = [wx.Display(i) for i in range(wx.Display.GetCount())][:1]
        sizes = [display.GetGeometry().GetSize() for display in displays]
        screen_width = sum([v.x for v in sizes]) - 50
        screen_height = min([v.y for v in sizes]) - 50

        rect = self.get('Rect')
        if rect is not None and len(rect) == 4:
            x, y, width, height = rect
            if x > 0 and x < screen_width and y > 0 and y < screen_height:
                self.parent.SetRect(rect)

        value = self.get('AlwaysOnTopMenuItem')
        if value is not None:
            self.parent.ToolPanel.SetAlwaysOnTopValue(value)

        # value = self.get('AutoClearWhenImportMenuItem')
        # if value is not None:
        #     self.parent.AutoClearWhenImportMenuItem.Check(value)

        # value = self.get('AutoClearWhenBatchPrecessingMenuItem')
        # if value is not None:
        #     self.parent.AutoClearWhenBatchPrecessingMenuItem.Check(value)

        value = self.get('PresetComboBox')
        if value is not None:
            self.parent.ToolPanel.PresetComboBox.SetValue(value)

        for macro in self.parent.ToolPanel.MacroFunctions:
            macro.toggle.SetValue(False)
            if self.get(macro.name):
                macro.toggle.SetValue(True)

        for macro in self.parent.ToolPanel.MacroValues:
            value = self.get(macro.name)
            if value is not None:
                macro.value.SetValue(float(value))

        self.parent.ToolPanel.SelectAllButton.SetLabel('Unselect All')
        for macro in self.parent.ToolPanel.MacroFunctions:
            if macro.name not in ('ExportSVG', 'SaveProject'):
                if macro.toggle.GetValue() is False:
                    self.parent.ToolPanel.SelectAllButton.SetLabel('Select All')
