# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


__PRESETS__ = [
    {
        'name': '1단(작은크기)',
        'preset': {
            'StaffSizeValue': 5.5,
            'StavesMarginValue': 10.0,
            'SystemsMarginValue': 25.0,
            'InstrumentMarginValue': 11.0,
            'InstrumentStaffGapValue': 2.0,
            'ShowInstrumentNamesValue': False,
            'BreakEveryBarsValue': 4.0,
        }
    },
    {
        'name': '1단(보통크기)',
        'preset': {
            'StaffSizeValue': 7.2,
            'StavesMarginValue': 10.0,
            'SystemsMarginValue': 25.0,
            'InstrumentMarginValue': 14.0,
            'InstrumentStaffGapValue': 2.0,
            'ShowInstrumentNamesValue': False,
            'BreakEveryBarsValue': 4.0,
        }
    },
    {
        'name': '2단(작은크기)',
        'preset': {
            'StaffSizeValue': 5.5,
            'StavesMarginValue': 10.0,
            'SystemsMarginValue': 25.0,
            'InstrumentMarginValue': 13.0,
            'InstrumentStaffGapValue': 3.0,
            'ShowInstrumentNamesValue': True,
            'BreakEveryBarsValue': 4.0
        }
    },
    {
        'name': '2단(보통크기)',
        'preset': {
            'StaffSizeValue': 7.2,
            'StavesMarginValue': 10.0,
            'SystemsMarginValue': 25.0,
            'InstrumentMarginValue': 15.0,
            'InstrumentStaffGapValue': 3.0,
            'ShowInstrumentNamesValue': True,
            'BreakEveryBarsValue': 4.0
        }
    }
]


class MacroPreset():

    def __init__(self, preset):
        for key in preset.keys():
            setattr(self, key, preset[key])


Presets = [MacroPreset(preset) for preset in __PRESETS__]
