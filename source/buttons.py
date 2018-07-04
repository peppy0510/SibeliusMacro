# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import multiprocessing
import queue
import threading
import wx

from automation import SibeliusUIAutomation
from preset import PRESETS


class Position():

    def __init__(self, x, y):
        self.x = x
        self.y = y


class PanelLines():

    def InsertVLines(self, parent, pos, num=1, height=23):
        lines = [wx.StaticLine(parent=parent, size=(1, height),
                               pos=wx.Point(pos.x + i * 2, pos.y + 2), style=wx.LI_VERTICAL) for i in range(num)]
        return wx.Point(lines[-1].GetPosition().x + 6, pos.y)

    def InsertHLines(self, parent, pos):
        wx.StaticLine(parent=parent, size=(2560 * 4, 1),
                      pos=wx.Point(-2, pos.y + 28), style=wx.LI_HORIZONTAL)
        return wx.Point(5, pos.y + 31)


class AlwaysOnTop():

    def OnAlwaysOnTopToggle(self, event=None):
        if event.IsChecked():
            self.SetAlwaysOnTopEnabled()
        else:
            self.SetAlwaysOnTopDisabled()

    def SetAlwaysOnTopEnabled(self):
        self.AlwaysOnTopMenuItem.Check(True)
        self.AlwaysOnTopToggle.SetValue(True)
        style = self.GetWindowStyle()
        self.SetWindowStyle(style | wx.STAY_ON_TOP)

    def SetAlwaysOnTopDisabled(self):
        self.AlwaysOnTopMenuItem.Check(False)
        self.AlwaysOnTopToggle.SetValue(False)
        #  버그 패치.두 번 이상 실행 되어야 함.
        for i in range(2):
            style = self.GetWindowStyle()
            self.SetWindowStyle(style ^ wx.STAY_ON_TOP)


class MacroButtonHandlers():

    def OnRunSelectedMacroButton(self, event=None):
        precesses = []
        for macro in self.MacroFunctions:
            if macro.toggle.GetValue():
                if macro.name == 'Invisibles':
                    precesses += ['setViewInvisibles']
                if macro.name == 'UnlockFormat':
                    precesses += ['setLayoutFormatUnlock']
                if macro.name == 'HidePageNumbers':
                    precesses += ['setTextNumberingPageNumberChange']
                if macro.name == 'MeasureNumbers':
                    precesses += ['setTextNumberingEverySystem']
                if macro.name == 'Layout':
                    precesses += ['setAppearanceInstrumentNames',
                                  'setLayoutDocumentSetup',
                                  'setLayoutStaffSpacing',
                                  'setLayoutStaffSpacingOptimize']
                if macro.name == 'AutoBreaks':
                    precesses += ['setLayoutAutoBreak']
                if macro.name == 'NoteSpace':
                    precesses += ['setAppearanceResetNotesResetNoteSpacing']
                if macro.name == 'RemoveTitle':
                    precesses += ['removeTitle']
                if macro.name == 'ExportSVG':
                    precesses += ['exportGraphicAsSVG']
                if macro.name == 'SaveProject':
                    precesses += ['saveProjectFile']

        if len(precesses) > 0:
            self.ShowProcessingDialog(precesses)

    def OnSelectAllMacroButton(self, event=None):
        if self.SelectAllButton.GetLabel() == 'Select All':
            for macro in self.MacroFunctions:
                if macro.name not in ('ExportSVG', 'SaveProject'):
                    macro.toggle.SetValue(True)
            self.SelectAllButton.SetLabel('Unselect All')
        else:
            for macro in self.MacroFunctions:
                if macro.name not in ('ExportSVG', 'SaveProject'):
                    macro.toggle.SetValue(False)
            self.SelectAllButton.SetLabel('Select All')

    def GetUIAutomation(self):
        uiautomation = SibeliusUIAutomation()
        for macro in self.MacroValues:
            if macro.name == 'AutoBreaksValue':
                uiautomation.auto_break_bars = macro.value.GetValue()
            if macro.name == 'StaffSizeValue':
                uiautomation.staff_size = macro.value.GetValue()
            if macro.name == 'StavesMarginValue':
                uiautomation.staves = macro.value.GetValue()
            if macro.name == 'SystemsMarginValue':
                uiautomation.staff_margin = macro.value.GetValue()
            if macro.name == 'InstrumentMarginValue':
                uiautomation.show_instrument_margin = macro.value.GetValue()
            if macro.name == 'InstrumentNamesShowValue':
                uiautomation.show_instrument = bool(macro.value.GetValue())
        return uiautomation

    def OnInvisiblesButton(self, event=None):
        self.ShowProcessingDialog(['setViewInvisibles'])

    def OnUnlockFormatButton(self, event=None):
        self.ShowProcessingDialog(['setLayoutFormatUnlock'])

    def OnHidePageNumbersButton(self, event=None):
        self.ShowProcessingDialog(['setTextNumberingPageNumberChange'])

    def OnMeasureNumbersButton(self, event=None):
        self.ShowProcessingDialog(['setTextNumberingEverySystem'])

    def OnLayoutButton(self, event=None):
        # self.ShowProcessingDialog(['setLayout'])
        self.ShowProcessingDialog(['setAppearanceInstrumentNames',
                                   'setLayoutDocumentSetup',
                                   'setLayoutStaffSpacing',
                                   'setLayoutStaffSpacingOptimize'])

    def OnAutoBreaksButton(self, event=None):
        self.ShowProcessingDialog(['setLayoutAutoBreak'])

    def OnNoteSpaceButton(self, event=None):
        self.ShowProcessingDialog(['setAppearanceResetNotesResetNoteSpacing'])

    def OnRemoveTitleButton(self, event=None):
        self.ShowProcessingDialog(['removeTitle'])

    def OnExportSVGButton(self, event=None):
        self.ShowProcessingDialog(['exportGraphicAsSVG'])

    def OnSaveProjectButton(self, event=None):
        self.ShowProcessingDialog(['saveProjectFile'])


class MacroProcessor(wx.Timer):

    def __init__(self, parent):
        wx.Timer.__init__(self)
        self.parent = parent
        self.interval = 100
        self.started = False
        self.thread = None
        self.thread_stop_queue = queue.Queue()
        self.Start(self.interval)
        self.total_count = len(self.parent.macros)
        self.uiautomation = self.parent.parent.GetUIAutomation()

    def Notify(self):

        if self.thread and not self.thread.isAlive():
            self.thread = None

        if len(self.parent.macros) == 0 and self.thread is None:
            self.Destroy()
            self.parent.Destroy()

        if len(self.parent.macros) > 0 and self.thread is None:
            name = self.parent.macros.pop(0)
            attr = getattr(self.uiautomation, name)
            self.thread = threading.Thread(target=attr, args=(self.thread_stop_queue,))
            # self.thread.daemon = True
            self.thread.start()
            label = ''
            if name == 'setViewInvisibles':
                label = 'Invisibles'
            if name == 'setLayoutFormatUnlock':
                label = 'Format Unlock'
            if name == 'setTextNumberingPageNumberChange':
                label = 'Hide Page Numbers'
            if name == 'setTextNumberingEverySystem':
                label = 'Measure Numbers'
            # if name in ['setAppearanceInstrumentNames',
            #             'setLayoutDocumentSetup',
            #             'setLayoutStaffSpacing',
            #             'setLayoutStaffSpacingOptimize']:
            #     name = 'Layout'
            if name == 'setAppearanceInstrumentNames':
                label = 'Layout Instrument Names'
            if name == 'setLayoutDocumentSetup':
                label = 'Layout Document Setup'
            if name == 'setLayoutStaffSpacing':
                label = 'Layout Staff Spacing'
            if name == 'setLayoutStaffSpacingOptimize':
                label = 'Layout Staff Spacing Optimize'
            if name == 'setLayoutAutoBreak':
                label = 'Auto Breaks'
            if name == 'setAppearanceResetNotesResetNoteSpacing':
                label = 'Note Space'
            if name == 'removeTitle':
                label = 'Remove Title'
            if name == 'exportGraphicAsSVG':
                label = 'Export SVG'
            if name == 'saveProjectFile':
                label = 'Save Project'

            self.parent.Message.SetLabel('%s (%d/%d)' % (
                label, self.total_count - len(self.parent.macros), self.total_count))


class MacroProcessingDialog(wx.Dialog):

    def __init__(self, parent, macros, *args, **kwargs):
        # wx.Dialog.__init__(self, parent, *args, **kwargs, style=wx.CLOSE_BOX | wx.STAY_ON_TOP | wx.DIALOG_NO_PARENT)
        wx.Dialog.__init__(self, parent, *args, **kwargs, style=wx.CLOSE_BOX | wx.STAY_ON_TOP)
        self.parent = parent
        self.macros = macros
        self.stop = False
        width, height = (205, 135)
        x, y, w, h = self.parent.GetScreenRect()
        x, y = (x + (w - width) / 2, y + (h - height) / 2)
        self.SetRect((x, y, width, height))
        self.SetTitle('Processing Macro')

        margin = 12
        width, height = self.GetClientSize()
        message = 'Processing macro, please wait ...'
        wx.StaticText(self, label=message, pos=(margin, margin))

        self.Message = wx.StaticText(self, label='', pos=(margin, margin + 20))

        # wx.StaticText(self, label=message, pos=(margin, margin + 18 * 2))

        # self.CancelButton = wx.Button(self, label=u'Cancel')
        # self.CancelButton.SetRect((width - (78 + margin) * 1, margin + 60, 78, 24))
        # self.CancelButton.Bind(wx.EVT_BUTTON, self.OnCancelButton)
        # x, y = self.CancelButton.GetPosition()

        x, y = self.Message.GetPosition()

        self.SetClientSize((self.GetClientSize().x, y + 30))
        self.processor = MacroProcessor(self)
        self.Bind(wx.EVT_CLOSE, self.OnCancelButton)
        self.ShowModal()

    def OnCancelButton(self, event=None):
        print('OnCancelButton')
        self.processor.macros = []
        if self.processor is not None and self.processor.thread is not None:
            self.processor.thread_stop_queue.put(True)
            self.processor.thread.join()
        self.processor.Destroy()
        self.Destroy()


class MacroProcessing():

    def ShowProcessingDialog(self, processors):

        # width, height = (250, 135)
        # x, y, w, h = self.GetScreenRect()
        # x, y = (x + (w - width) / 2, y + (h - height) / 2)
        self.Dialog = MacroProcessingDialog(self, processors)
        # self.Dialog.SetRect((x, y, width, height))
        # self.Dialog.SetTitle('About')

        # margin = 12
        # width, height = self.Dialog.GetClientSize()
        # message = 'SibeliusMacro %s' % (self.version)
        # wx.StaticText(self.Dialog, label=message, pos=(margin, margin))
        # message = 'Author: %s' % (self.author_name)
        # wx.StaticText(self.Dialog, label=message, pos=(margin, margin + 18))
        # message = 'Email: %s' % (self.author_email)
        # wx.StaticText(self.Dialog, label=message, pos=(margin, margin + 18 * 2))

        # self.Dialog.CancelButton = wx.Button(self.Dialog, label=u'Cancel')
        # self.Dialog.CancelButton.SetRect((width - (78 + margin) * 1, margin + 60, 78, 24))
        # self.Dialog.CancelButton.Bind(wx.EVT_BUTTON, self.HideProcessingDialog)

        # x, y = self.Dialog.CancelButton.GetPosition()
        # self.Dialog.SetClientSize((self.Dialog.GetClientSize().x, y + 35))
        # self.Dialog.ShowModal()

    def HideProcessingDialog(self, event=None):
        self.Dialog.OnCancelButton()


class MacroToggleHandlers():

    def HandleToggleEventSelectAllButton(self, event):
        if event.IsChecked() is False:
            self.SelectAllButton.SetLabel('Select All')

    def OnInvisiblesToggle(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        self.HandleToggleEventSelectAllButton(event)

    def OnUnlockFormatToggle(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        self.HandleToggleEventSelectAllButton(event)

    def OnHidePageNumbersToggle(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        self.HandleToggleEventSelectAllButton(event)

    def OnMeasureNumbersToggle(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        self.HandleToggleEventSelectAllButton(event)

    # def OnInstrumentNamesToggle(self, event=None):
    #     self.MacroPresetComboBox.SetValue('')
    #     self.HandleToggleEventSelectAllButton(event)

    def OnLayoutToggle(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        self.HandleToggleEventSelectAllButton(event)

    def OnAutoBreaksToggle(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        self.HandleToggleEventSelectAllButton(event)

    def OnNoteSpaceToggle(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        self.HandleToggleEventSelectAllButton(event)

    def OnRemoveTitleToggle(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        self.HandleToggleEventSelectAllButton(event)

    def OnExportSVGToggle(self, event=None):
        # self.MacroPresetComboBox.SetValue('')
        self.HandleToggleEventSelectAllButton(event)

    def OnSaveProjectToggle(self, event=None):
        # self.MacroPresetComboBox.SetValue('')
        self.HandleToggleEventSelectAllButton(event)


class MacroValueHandlers():

    def OnAutoBreaksValue(self, event=None):
        pass

    def OnStaffSizeValue(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        pass

    def OnStavesMarginValue(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        pass

    def OnSystemsMarginValue(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        pass

    def OnInstrumentMarginValue(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        pass

    def OnInstrumentNamesShow(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        pass

    def OnInstrumentNamesHide(self, event=None):
        self.MacroPresetComboBox.SetValue('')
        pass


class Buttons(PanelLines, AlwaysOnTop, MacroButtonHandlers,
              MacroToggleHandlers, MacroValueHandlers, MacroProcessing):

    def InitializeButtons(self):
        font_family = wx.SWISS
        font_style = wx.NORMAL
        font_weight = wx.NORMAL
        font_face_name = 'Segoe UI'
        font_encoding = wx.FONTENCODING_DEFAULT
        font = wx.Font(8, font_family, font_style, font_weight,
                       faceName=font_face_name, encoding=font_encoding)
        small_font = wx.Font(7, font_family, font_style, font_weight,
                             faceName=font_face_name, encoding=font_encoding)

        def make_button(label, pos, bind,
                        style=wx.BORDER_DEFAULT,
                        foreground_color=(0, 0, 0),
                        background_color=(240, 240, 240)):
            pos = self.InsertHLines(self.ToolPanel, pos)
            pos = self.InsertVLines(self.ToolPanel, pos, num=2)
            button = wx.Button(label=label, parent=self.ToolPanel,
                               pos=wx.Point(pos.x, pos.y), size=(125, 26), style=style)
            button.SetBackgroundColour(background_color)
            button.SetForegroundColour(foreground_color)
            button.SetFont(font)
            button.Bind(wx.EVT_BUTTON, bind)
            pos.x += button.GetSize().x + 3
            pos = self.InsertVLines(self.ToolPanel, pos)
            return button, pos

        def make_button_and_toggle(label, pos, button_bind, toggle_bind,
                                   style=wx.BORDER_DEFAULT,
                                   foreground_color=(0, 0, 0),
                                   background_color=(240, 240, 240)):
            button, pos = make_button(label, pos, button_bind,
                                      style=style,
                                      foreground_color=foreground_color,
                                      background_color=background_color)
            toggle = wx.CheckBox(self.ToolPanel, pos=wx.Point(pos.x, pos.y + 6))
            pos.x += toggle.GetSize().x + 3
            pos = self.InsertVLines(self.ToolPanel, pos)
            toggle.Bind(wx.EVT_CHECKBOX, toggle_bind)
            return button, toggle, pos

        def make_spinctrl(label, pos, bind, min_value, max_value, increment, initial):
            pos = self.InsertHLines(self.ToolPanel, pos)
            offset = 97
            label = wx.StaticText(self.ToolPanel, label=label)
            label.SetFont(small_font)
            label.SetPosition(wx.Point(offset - label.GetSize().width, pos.y + 6))
            pos.x += offset
            spinctrl = wx.SpinCtrlDouble(
                self.ToolPanel, value='', pos=wx.Point(pos.x, pos.y + 2), size=(60, 22),
                style=wx.SP_ARROW_KEYS, min=min_value, max=max_value, inc=increment, initial=initial, name='wxSpinCtrl')
            spinctrl.Bind(wx.EVT_SPINCTRLDOUBLE, bind)
            return spinctrl, pos

        def make_combobox(pos, bind=None):
            pos = self.InsertHLines(self.ToolPanel, pos)
            pos = self.InsertVLines(self.ToolPanel, pos, num=2)
            combobox = wx.ComboBox(
                self.ToolPanel, size=(122, 22), pos=wx.Point(pos.x + 2, pos.y + 2), style=wx.CB_DROPDOWN)
            combobox.SetEditable(False)
            if bind:
                combobox.Bind(wx.EVT_COMBOBOX, bind)
            pos.x += combobox.GetSize().x + 6
            pos = self.InsertVLines(self.ToolPanel, pos)
            return combobox, pos

        pos = Position(5, -28)
        pos = self.InsertHLines(self.ToolPanel, pos)
        pos = Position(5, 2)

        pos = self.InsertVLines(self.ToolPanel, pos, num=2)
        self.AlwaysOnTopToggle = wx.CheckBox(
            self.ToolPanel, pos=wx.Point(pos.x + 3, pos.y + 6), label=u' Always on top ')
        self.AlwaysOnTopToggle.SetFont(font)
        self.AlwaysOnTopToggle.Bind(wx.EVT_CHECKBOX, self.OnAlwaysOnTopToggle)

        pos.x += 127

        self.SelectAllButton, pos = make_button(
            u'Run Selected', pos, self.OnRunSelectedMacroButton,
            foreground_color=(255, 255, 255), background_color=(125, 125, 125))

        self.MacroPresetComboBox, pos = make_combobox(pos, self.OnMacroPresetComboBox)
        self.MacroPresetComboBox.SetItems([v.name for v in PRESETS])
        self.MacroPresetComboBox.SetValue(PRESETS[1].name)

        self.SelectAllButton, pos = make_button(
            u'Select All', pos, self.OnSelectAllMacroButton,
            foreground_color=(255, 255, 255), background_color=(125, 125, 125))

        self.InvisiblesButton, self.InvisiblesToggle, pos = make_button_and_toggle(
            u'Invisibles', pos, self.OnInvisiblesButton, self.OnInvisiblesToggle)

        self.UnlockFormatButton, self.UnlockFormatToggle, pos = make_button_and_toggle(
            u'Unlock Format', pos, self.OnUnlockFormatButton, self.OnUnlockFormatToggle)

        self.HidePageNumbersButton, self.HidePageNumbersToggle, pos = make_button_and_toggle(
            u'Hide Page Numbers', pos, self.OnHidePageNumbersButton, self.OnHidePageNumbersToggle)

        self.MeasureNumbersButton, self.MeasureNumbersToggle, pos = make_button_and_toggle(
            u'Measure Numbers', pos, self.OnMeasureNumbersButton, self.OnMeasureNumbersToggle)

        # self.InstrumentNamesButton, self.InstrumentNamesToggle, pos = make_button_and_toggle(
        #     u'Instrument Names', pos, self.OnInstrumentNamesButton, self.OnInstrumentNamesToggle)

        self.LayoutButton, self.LayoutToggle, pos = make_button_and_toggle(
            u'Layout', pos, self.OnLayoutButton, self.OnLayoutToggle)

        self.StaffSizeValue, pos = make_spinctrl(
            u'Staff Size', pos, self.OnStaffSizeValue, min_value=1.0, max_value=15.0, increment=0.1, initial=7.2)

        self.StavesMarginValue, pos = make_spinctrl(
            u'Staves Margin', pos, self.OnStavesMarginValue, min_value=0, max_value=30, increment=1, initial=10)

        self.SystemsMarginValue, pos = make_spinctrl(
            u'Systems Margin', pos, self.OnSystemsMarginValue, min_value=0, max_value=30, increment=1, initial=25)

        self.InstrumentMarginValue, pos = make_spinctrl(
            u'Instrument Margin', pos, self.OnInstrumentMarginValue, min_value=0, max_value=20, increment=1, initial=0)

        class InstrumentNamesShowValue():

            def __init__(self, parent):
                self.parent = parent

            def SetValue(self, value):
                value = bool(value)
                self.parent.InstrumentNamesShow.SetValue(value)
                self.parent.InstrumentNamesHide.SetValue(not value)

            def GetValue(self):
                return self.parent.InstrumentNamesShow.GetValue()

        pos = self.InsertHLines(self.ToolPanel, pos)
        pos.x += 60

        label = wx.StaticText(self.ToolPanel, label='Instrument Show')
        label.SetFont(small_font)
        label.SetPosition(wx.Point(36, pos.y + 6))

        self.InstrumentNamesShow = wx.RadioButton(
            self.ToolPanel, size=wx.Size(14, 14), pos=wx.Point(107, pos.y + 6), style=wx.RB_GROUP)
        self.InstrumentNamesShow.SetFont(small_font)
        self.InstrumentNamesShow.Bind(wx.EVT_RADIOBUTTON, self.OnInstrumentNamesShow)
        self.InstrumentNamesShow.SetValue(True)

        label = wx.StaticText(self.ToolPanel, label='Hide')
        label.SetFont(small_font)
        label.SetPosition(wx.Point(125, pos.y + 6))

        self.InstrumentNamesHide = wx.RadioButton(
            self.ToolPanel, size=wx.Size(14, 14), pos=wx.Point(147, pos.y + 6))
        self.InstrumentNamesHide.SetFont(small_font)
        self.InstrumentNamesHide.Bind(wx.EVT_RADIOBUTTON, self.OnInstrumentNamesHide)
        self.InstrumentNamesShowValue = InstrumentNamesShowValue(self)

        self.AutoBreaksButton, self.AutoBreaksToggle, pos = make_button_and_toggle(
            u'Auto Breaks', pos, self.OnAutoBreaksButton, self.OnAutoBreaksToggle)

        self.AutoBreaksValue, pos = make_spinctrl(
            u'Every Bars', pos, self.OnAutoBreaksValue, min_value=1, max_value=8, increment=1, initial=4)

        self.NoteSpaceButton, self.NoteSpaceToggle, pos = make_button_and_toggle(
            u'Note Space', pos, self.OnNoteSpaceButton, self.OnNoteSpaceToggle)

        self.RemoveTitleButton, self.RemoveTitleToggle, pos = make_button_and_toggle(
            u'Remove Title', pos, self.OnRemoveTitleButton, self.OnRemoveTitleToggle)

        self.ExportSVGButton, self.ExportSVGToggle, pos = make_button_and_toggle(
            u'Export SVG', pos, self.OnExportSVGButton, self.OnExportSVGToggle,
            foreground_color=(255, 255, 255), background_color=(125, 125, 125))

        self.SaveProjectButton, self.SaveProjectToggle, pos = make_button_and_toggle(
            u'Save Project', pos, self.OnSaveProjectButton, self.OnSaveProjectToggle,
            foreground_color=(255, 255, 255), background_color=(125, 125, 125))

        pos = self.InsertHLines(self.ToolPanel, pos)

        class MacroFunction():

            def __init__(self, parent, name):
                self.name = name
                self.button = getattr(parent, name + 'Button')
                self.toggle = getattr(parent, name + 'Toggle')
                self.method = self.button.ProcessEvent

            def run(self):
                self.button.ProcessEvent

        class MacroValue():

            def __init__(self, parent, name):
                name = name + 'Value'
                self.name = name
                self.value = getattr(parent, name)

        self.MacroValues = []
        for name in ('AutoBreaks', 'StaffSize', 'StavesMargin',
                     'SystemsMargin', 'InstrumentMargin', 'InstrumentNamesShow'):
            self.MacroValues += [MacroValue(self, name)]

        self.MacroFunctions = []
        for name in ('Invisibles', 'UnlockFormat', 'HidePageNumbers', 'MeasureNumbers',
                     'Layout', 'AutoBreaks', 'NoteSpace', 'RemoveTitle', 'ExportSVG', 'SaveProject'):
            self.MacroFunctions += [MacroFunction(self, name)]

        self.ToolPanel.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnMacroPresetComboBox(self, event=None):
        for key, value in PRESETS[event.GetInt()].preset.items():
            attr = getattr(self, key)
            attr.SetValue(value)

        for macro in self.MacroFunctions:
            if macro.name not in ('ExportSVG', 'SaveProject'):
                macro.toggle.SetValue(True)

        self.SelectAllButton.SetLabel('Unselect All')

    def OnPaint(self, event):
        width, height = self.ToolPanel.GetClientSize()
        dc = wx.PaintDC(self.ToolPanel)  # <<< This was changed
        color = '#D0D0D0'
        dc.SetPen(wx.Pen(color))
        dc.SetBrush(wx.Brush(color))
        # dc.DrawRectangle(0, 30, width, 528)
        dc.DrawRectangle(0, 558, width, 62)
        dc.DrawRectangle(0, 30, width, 93)
        # print(, event.GetString())
        # print(dir(event))

        # Filter Buttons

        # label = wx.StaticText(label='Filter', parent=self.FuncPanel,
        #                       pos=wx.Point(pos.x, pos.y + 5))
        # pos.x += label.GetSize().x + 6

        # self.ImportFilterFile = wx.CheckBox(
        #     self.FuncPanel, pos=wx.Point(pos.x, pos.y + 5), label=u'File')
        # self.ImportFilterFile.Bind(wx.EVT_CHECKBOX, self.OnImportFilterFile)
        # self.ImportFilterFile.SetValue(True)
        # pos.x += self.ImportFilterFile.GetSize().x + 1

        # self.ImportFilterFolder = wx.CheckBox(label=u'Folder', parent=self.FuncPanel,
        #                                       pos=wx.Point(pos.x, pos.y + 24))
        # self.ImportFilterFolder.Bind(wx.EVT_CHECKBOX, self.OnImportFilterFoler)
        # self.ImportFilterFolder.SetValue(True)
        # pos.x += self.ImportFilterFolder.GetSize().x

        # pos = self.InsertVLines(self.FuncPanel, pos, height=41)

        # Tools Buttons

        # self.ToolsButton = wx.Button(label=u'Tools', parent=self.FuncPanel,
        #                              pos=wx.Point(pos.x, pos.y), size=(50, 24))

        # self.ToolsButton.SetBackgroundColour((240, 240, 240))
        # self.ToolsButton.SetForegroundColour((0, 0, 0))
        # self.ToolsButton.Bind(wx.EVT_BUTTON, self.OnToolsButton)
        # pos.x += self.ToolsButton.GetSize().x + 4

        # pos = self.InsertVLines(self.FuncPanel, pos)

        # Preview Buttons

        # self.PreviewButton = wx.Button(label=u'Run Opened F5', parent=self.ToolPanel,
        #                                pos=wx.Point(pos.x, pos.y), size=(125, 43))
        # self.PreviewButton.SetBackgroundColour((240, 240, 240))
        # self.PreviewButton.SetForegroundColour((0, 0, 0))
        # self.PreviewButton.Bind(wx.EVT_BUTTON, self.RunMacroOpened)
        # pos.x += self.PreviewButton.GetSize().x + 2

        # self.RenameButton = wx.Button(label=u'Run List F6', parent=self.ToolPanel,
        #                               pos=wx.Point(pos.x, pos.y), size=(125, 43))
        # self.RenameButton.SetBackgroundColour((240, 240, 240))
        # self.RenameButton.SetForegroundColour((0, 0, 0))
        # self.RenameButton.Bind(wx.EVT_BUTTON, self.OnRenameButton)
        # pos.x += self.RenameButton.GetSize().x + 4

        # pos = self.InsertVLines(self.ToolPanel, pos, height=41)
