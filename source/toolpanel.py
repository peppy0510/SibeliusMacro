# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import wx

from preset import Presets
from toolhandler import ToolHandler


class Position():

    def __init__(self, x, y):
        self.x = x
        self.y = y


class MacroFunction():

    def __init__(self, parent, name, label, targets):
        self.name = name
        self.label = label
        self.targets = targets
        self.button = getattr(parent, self.name + 'Button')
        self.toggle = getattr(parent, self.name + 'Toggle')
        # self.method = self.button.ProcessEvent

    def run(self):
        self.button.ProcessEvent


class MacroValue():

    def __init__(self, parent, name, param):
        name = name + 'Value'
        self.name = name
        self.param = param
        self.value = getattr(parent, name)


class ToolPanelFont():

    @classmethod
    def _get_args_(self):
        return wx.SWISS, wx.NORMAL, wx.NORMAL

    @classmethod
    def _get_kwargs_(self):
        return {'faceName': 'Segoe UI', 'encoding': wx.FONTENCODING_DEFAULT}

    @classmethod
    def Get(self):
        return wx.Font(8, *self._get_args_(), **self._get_kwargs_())

    @classmethod
    def GetSmall(self):
        return wx.Font(7, *self._get_args_(), **self._get_kwargs_())


class ToolPanel(wx.Panel, ToolHandler):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, style=wx.LC_REPORT | wx.BORDER_DEFAULT)
        self.parent = parent
        self.SetBackgroundColour((180, 180, 180))
        self.BottomLine = wx.StaticLine(parent=self, size=(172, 1), style=wx.LI_HORIZONTAL)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.MacroValues = []
        self.MacroFunctions = []

        pos = Position(5, -28)
        pos = self.InsertHLines(pos)
        pos = Position(5, 2)

        pos = self.MakeAlwaysOnTopButton(pos)

        pos.x += 127

        pos = self.MakeButton(pos, 'Run Selected', dark=True)

        pos = self.MakePresetComboBox(pos)

        pos = self.MakeButton(pos, 'Select All', dark=True)
        pos = self.MakeButtonAndToggle(pos, 'HidePanels')
        pos = self.MakeButtonAndToggle(pos, 'SinglePagesVertically')
        pos = self.MakeButtonAndToggle(pos, 'Invisibles')
        pos = self.MakeButtonAndToggle(pos, 'Unlock Format')
        pos = self.MakeButtonAndToggle(pos, 'Hide Page Numbers')
        pos = self.MakeButtonAndToggle(pos, 'Measure Numbers')
        pos = self.MakeButtonAndToggle(pos, 'Layout',
                                       targets=['InstrumentNames', 'DocumentSetup',
                                                'StaffSpacing', 'StaffSpacingOptimize'])
        pos = self.MakeSpinCtrl(pos, 'Staff Size', param='staff_size',
                                initial=7.2, increment=0.1, min_value=1.0, max_value=15.0)
        pos = self.MakeSpinCtrl(pos, 'Staves Margin', param='staves_size',
                                initial=10, increment=1, min_value=0, max_value=30)
        pos = self.MakeSpinCtrl(pos, 'Systems Margin', param='systems_size',
                                initial=25, increment=1, min_value=0, max_value=30)
        pos = self.MakeInstrumentShowRadio(pos, param='show_instrument_name')
        pos = self.MakeSpinCtrl(pos, 'Instrument Margin', param='instrument_staff_margin',
                                initial=0, increment=1, min_value=0, max_value=30)
        pos = self.MakeSpinCtrl(pos, 'Instrument Staff Gap', param='instrument_name_barline_gap',
                                initial=0, increment=1, min_value=0, max_value=30)
        pos = self.MakeButtonAndToggle(pos, 'Auto Breaks')
        pos = self.MakeSpinCtrl(pos, 'Break Every Bars', param='auto_breaks_bars',
                                initial=4, increment=1, min_value=1, max_value=8)
        pos = self.MakeButtonAndToggle(pos, 'Note Space')
        pos = self.MakeButtonAndToggle(pos, 'Remove Title')
        pos = self.MakeButtonAndToggle(pos, 'Export SVG', dark=True)
        pos = self.MakeButtonAndToggle(pos, 'Save Project', dark=True)
        pos = self.InsertHLines(pos)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnSize(self, event):
        width, height = self.GetClientSize()
        self.BottomLine.SetRect((-2, height - 1, width + 4, 1))

    def InsertVLines(self, pos, num=1, height=23):
        lines = [wx.StaticLine(parent=self, size=(1, height),
                               pos=wx.Point(pos.x + i * 2, pos.y + 2), style=wx.LI_VERTICAL) for i in range(num)]
        return wx.Point(lines[-1].GetPosition().x + 6, pos.y)

    def InsertHLines(self, pos):
        wx.StaticLine(parent=self, size=(2560 * 4, 1),
                      pos=wx.Point(-2, pos.y + 28), style=wx.LI_HORIZONTAL)
        return wx.Point(5, pos.y + 31)

    def MakeButton(self, pos, label, style=wx.BORDER_DEFAULT, dark=False):
        pos = self.InsertHLines(pos)
        pos = self.InsertVLines(pos, num=2)
        button = wx.Button(label=label, parent=self,
                           pos=wx.Point(pos.x, pos.y), size=(125, 26), style=style)

        attrname = label.replace(' ', '')
        setattr(self, attrname + 'Button', button)

        attrname = 'On' + attrname + 'Button'
        if hasattr(self, attrname):
            button.Bind(wx.EVT_BUTTON, getattr(self, attrname))

        background = (125, 125, 125) if dark else (240, 240, 240)
        button.SetBackgroundColour(background)
        button.SetForegroundColour((255, 255, 255) if sum(background[:3]) / 3 < 255 / 2 else (0, 0, 0))
        button.SetFont(ToolPanelFont.Get())
        pos.x += button.GetSize().x + 3
        pos = self.InsertVLines(pos)
        return pos

    def MakeButtonAndToggle(self, pos, label, targets=[], style=wx.BORDER_DEFAULT, dark=False):
        pos = self.MakeButton(pos, label, style=style, dark=dark)

        toggle = wx.CheckBox(self, pos=wx.Point(pos.x, pos.y + 6))
        attrname = label.replace(' ', '')
        setattr(self, attrname + 'Toggle', toggle)

        targets = [attrname] if len(targets) == 0 else targets
        self.MacroFunctions += [MacroFunction(self, attrname, label, targets=targets)]

        attrname = 'On' + attrname + 'Toggle'
        if hasattr(self, attrname):
            toggle.Bind(wx.EVT_CHECKBOX, getattr(self, attrname))

        pos.x += toggle.GetSize().x + 3
        pos = self.InsertVLines(pos)
        return pos

    def MakeSpinCtrl(self, pos, label, param, initial, increment, min_value, max_value):
        pos = self.InsertHLines(pos)
        offset = 97
        text = wx.StaticText(self, label=label)
        text.SetFont(ToolPanelFont.GetSmall())
        text.SetPosition(wx.Point(offset - text.GetSize().width, pos.y + 6))
        pos.x += offset
        spinctrl = wx.SpinCtrlDouble(
            self, value='', pos=wx.Point(pos.x, pos.y + 2), size=(60, 22),
            style=wx.SP_ARROW_KEYS, min=min_value, max=max_value, inc=increment, initial=initial, name='wxSpinCtrl')

        attrname = label.replace(' ', '')
        setattr(self, attrname + 'Value', spinctrl)

        self.MacroValues += [MacroValue(self, attrname, param)]

        attrname = 'On' + attrname + 'Value'
        if hasattr(self, attrname):
            spinctrl.Bind(wx.EVT_SPINCTRLDOUBLE, getattr(self, attrname))

        return pos

    def MakeAlwaysOnTopButton(self, pos):
        pos = self.InsertVLines(pos, num=2)
        self.AlwaysOnTopToggle = wx.CheckBox(
            self, pos=wx.Point(pos.x + 3, pos.y + 6), label=' Always on top ')
        self.AlwaysOnTopToggle.SetFont(ToolPanelFont.Get())
        self.AlwaysOnTopToggle.Bind(wx.EVT_CHECKBOX, self.OnAlwaysOnTopToggle)
        return pos

    def MakePresetComboBox(self, pos):
        pos = self.InsertHLines(pos)
        pos = self.InsertVLines(pos, num=2)
        combobox = wx.ComboBox(
            self, size=(122, 22), pos=wx.Point(pos.x + 2, pos.y + 2), style=wx.CB_DROPDOWN)
        combobox.SetEditable(False)
        combobox.Bind(wx.EVT_COMBOBOX, self.OnPresetComboBox)
        pos.x += combobox.GetSize().x + 6
        pos = self.InsertVLines(pos)
        combobox.SetItems([v.name for v in Presets])
        combobox.SetValue(Presets[1].name)
        self.PresetComboBox = combobox
        return pos

    def MakeInstrumentShowRadio(self, pos, param):

        class ShowInstrumentNamesValue():

            def __init__(self, show, hide):
                self.show = show
                self.hide = hide

            def SetValue(self, value):
                value = bool(value)
                self.show.SetValue(value)
                self.hide.SetValue(not value)

            def GetValue(self):
                return self.show.GetValue()

        pos = self.InsertHLines(pos)
        pos.x += 60

        label = wx.StaticText(self, label='Instrument Show')
        label.SetFont(ToolPanelFont.GetSmall())
        label.SetPosition(wx.Point(36, pos.y + 6))

        show = wx.RadioButton(
            self, size=wx.Size(14, 14), pos=wx.Point(107, pos.y + 6), style=wx.RB_GROUP)
        show.SetFont(ToolPanelFont.GetSmall())
        show.Bind(wx.EVT_RADIOBUTTON, self.OnShowInstrumentNames)
        show.SetValue(True)

        label = wx.StaticText(self, label='Hide')
        label.SetFont(ToolPanelFont.GetSmall())
        label.SetPosition(wx.Point(125, pos.y + 6))

        hide = wx.RadioButton(
            self, size=wx.Size(14, 14), pos=wx.Point(147, pos.y + 6))
        hide.SetFont(ToolPanelFont.GetSmall())
        hide.Bind(wx.EVT_RADIOBUTTON, self.OnHideInstrumentNames)
        self.ShowInstrumentNamesValue = ShowInstrumentNamesValue(show, hide)

        self.MacroValues += [MacroValue(self, 'ShowInstrumentNames', param)]

        return pos

    def OnPaint(self, event):
        width, height = self.GetClientSize()
        dc = wx.PaintDC(self)
        color = '#D0D0D0'
        dc.SetPen(wx.Pen(color))
        dc.SetBrush(wx.Brush(color))
        dc.DrawRectangle(0, 30, width, 93)
        dc.DrawRectangle(0, 589, width, 62)
