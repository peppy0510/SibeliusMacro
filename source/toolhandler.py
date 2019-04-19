# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import wx

from macrodialog import MacroDialog
from preset import Presets


class AlwaysOnTopToggleHandler():

    def OnAlwaysOnTopToggle(self, event=None):
        self.SetAlwaysOnTopValue(event.IsChecked())

    def SetAlwaysOnTopValue(self, value):
        if value:
            self.SetAlwaysOnTopEnabled()
        else:
            self.SetAlwaysOnTopDisabled()

    def SetAlwaysOnTopEnabled(self):
        self.parent.AlwaysOnTopMenuItem.Check(True)
        self.AlwaysOnTopToggle.SetValue(True)
        # style = self.parent.GetWindowStyle()
        # self.parent.SetWindowStyle(style | wx.STAY_ON_TOP)
        self.parent.SetWindowStyle(self.parent.defaultStyle | wx.STAY_ON_TOP)
        self.parent.Update()

    def SetAlwaysOnTopDisabled(self):
        self.parent.AlwaysOnTopMenuItem.Check(False)
        self.AlwaysOnTopToggle.SetValue(False)
        # style = self.parent.GetWindowStyle()
        # self.parent.SetWindowStyle(style ^ wx.STAY_ON_TOP)
        self.parent.SetWindowStyle(self.parent.defaultStyle)
        self.parent.Update()


class SelectAllButtonHandler():

    _select_all_label_ = 'Select All'
    _unselect_all_label_ = 'Unselect All'
    _select_all_exceptions_ = ('ExportSVG', 'SaveProject')

    def OnSelectAllButton(self, event=None):
        if self.SelectAllButton.GetLabel() == self._select_all_label_:
            self.SelectAllToggle()
        else:
            self.UnselectAllToggle()

    def SelectAllToggle(self):
        for v in self.MacroFunctions:
            if v.name not in self._select_all_exceptions_:
                v.toggle.SetValue(True)
        self.SelectAllButton.SetLabel(self._unselect_all_label_)

    def UnselectAllToggle(self):
        for v in self.MacroFunctions:
            if v.name not in self._select_all_exceptions_:
                v.toggle.SetValue(False)
        self.SelectAllButton.SetLabel(self._select_all_label_)

    def HandleToggleEventSelectAllButton(self, event):
        if False in [v.toggle.GetValue() for v in self.MacroFunctions
                     if v.name not in self._select_all_exceptions_]:
            self.SelectAllButton.SetLabel(self._select_all_label_)
        else:
            self.SelectAllButton.SetLabel(self._unselect_all_label_)


class PresetComboBoxHandler():

    def OnPresetValueChanged(self):
        self.PresetComboBox.SetValue('')

    def OnPresetComboBox(self, event=None):
        for key, value in Presets[event.GetInt()].preset.items():
            attr = getattr(self, key)
            attr.SetValue(value)
        self.SelectAllToggle()


class RunSelectedButtonHandler():

    def OnRunSelectedButton(self, event=None):
        # for v in self.parent.ListPanel.OLV.GetObjects():
        #     print(v.path)
        # return
        self.ShowMacroDialog([v for v in self.MacroFunctions if v.toggle.GetValue()])


class ButtonHandler():

    def OnMacroButton(self, name):
        # if len(self.parent.ListPanel.OLV.GetObjects()) > 0:
        #     return
        self.ShowMacroDialog([v for v in self.MacroFunctions if v.name == name])

    def OnHidePanelsButton(self, event=None):
        self.OnMacroButton('HidePanels')

    def OnSinglePagesVerticallyButton(self, event=None):
        self.OnMacroButton('SinglePagesVertically')

    def OnInvisiblesButton(self, event=None):
        self.OnMacroButton('Invisibles')

    def OnUnlockFormatButton(self, event=None):
        self.OnMacroButton('UnlockFormat')

    def OnHidePageNumbersButton(self, event=None):
        self.OnMacroButton('HidePageNumbers')

    def OnMeasureNumbersButton(self, event=None):
        self.OnMacroButton('MeasureNumbers')

    def OnLayoutButton(self, event=None):
        self.OnMacroButton('Layout')

    def OnAutoBreaksButton(self, event=None):
        self.OnMacroButton('AutoBreaks')

    def OnNoteSpaceButton(self, event=None):
        self.OnMacroButton('NoteSpace')

    def OnRemoveTitleButton(self, event=None):
        self.OnMacroButton('RemoveTitle')

    def OnExportSVGButton(self, event=None):
        self.OnMacroButton('ExportSVG')

    def OnSaveProjectButton(self, event=None):
        self.OnMacroButton('SaveProject')


class ToggleHandler():

    def OnHidePanelsToggle(self, event=None):
        self.OnPresetValueChanged()
        self.HandleToggleEventSelectAllButton(event)

    def OnSinglePagesVerticallyToggle(self, event=None):
        self.OnPresetValueChanged()
        self.HandleToggleEventSelectAllButton(event)

    def OnInvisiblesToggle(self, event=None):
        self.OnPresetValueChanged()
        self.HandleToggleEventSelectAllButton(event)

    def OnUnlockFormatToggle(self, event=None):
        self.OnPresetValueChanged()
        self.HandleToggleEventSelectAllButton(event)

    def OnHidePageNumbersToggle(self, event=None):
        self.OnPresetValueChanged()
        self.HandleToggleEventSelectAllButton(event)

    def OnMeasureNumbersToggle(self, event=None):
        self.OnPresetValueChanged()
        self.HandleToggleEventSelectAllButton(event)

    def OnLayoutToggle(self, event=None):
        self.OnPresetValueChanged()
        self.HandleToggleEventSelectAllButton(event)

    def OnAutoBreaksToggle(self, event=None):
        self.OnPresetValueChanged()
        self.HandleToggleEventSelectAllButton(event)

    def OnNoteSpaceToggle(self, event=None):
        self.OnPresetValueChanged()
        self.HandleToggleEventSelectAllButton(event)

    def OnRemoveTitleToggle(self, event=None):
        self.OnPresetValueChanged()
        self.HandleToggleEventSelectAllButton(event)

    def OnExportSVGToggle(self, event=None):
        self.HandleToggleEventSelectAllButton(event)

    def OnSaveProjectToggle(self, event=None):
        self.HandleToggleEventSelectAllButton(event)


class ValueHandler():

    def OnBreakEveryBarsValue(self, event=None):
        self.OnPresetValueChanged()

    def OnStaffSizeValue(self, event=None):
        self.OnPresetValueChanged()

    def OnStavesMarginValue(self, event=None):
        self.OnPresetValueChanged()

    def OnSystemsMarginValue(self, event=None):
        self.OnPresetValueChanged()

    def OnInstrumentMarginValue(self, event=None):
        self.OnPresetValueChanged()

    def OnInstrumentStaffGapValue(self, event=None):
        self.OnPresetValueChanged()

    def OnShowInstrumentNames(self, event=None):
        self.OnPresetValueChanged()

    def OnHideInstrumentNames(self, event=None):
        self.OnPresetValueChanged()


class MacroDialogHandler():

    def ShowMacroDialog(self, macros):
        self.parent.Dialog = MacroDialog(self.parent, macros, self.MacroValues)

    def HideMacroDialog(self, event=None):
        self.parent.Dialog.OnCancelButton()


class ToolHandler(AlwaysOnTopToggleHandler,
                  SelectAllButtonHandler,
                  PresetComboBoxHandler,
                  RunSelectedButtonHandler,
                  ButtonHandler,
                  ToggleHandler,
                  ValueHandler,
                  MacroDialogHandler):
    pass
