# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


__PRESETS__ = [
    {
        'name': '1단(작은크기)',
        'preset': {
            'AutoBreaksValue': 4.0,
            'StaffSizeValue': 5.5,
            'StavesMarginValue': 10.0,
            'SystemsMarginValue': 25.0,
            'InstrumentMarginValue': 2.0,
            'InstrumentNamesShowValue': False,
        }
    },
    {
        'name': '1단(보통크기)',
        'preset': {
            'AutoBreaksValue': 4.0,
            'StaffSizeValue': 7.2,
            'StavesMarginValue': 10.0,
            'SystemsMarginValue': 25.0,
            'InstrumentMarginValue': 2.0,
            'InstrumentNamesShowValue': False,
        }
    },
    {
        'name': '2단(작은크기)',
        'preset': {
            'AutoBreaksValue': 4.0,
            'StaffSizeValue': 5.5,
            'StavesMarginValue': 10.0,
            'SystemsMarginValue': 25.0,
            'InstrumentMarginValue': 3.0,
            'InstrumentNamesShowValue': True,
        }
    },
    {
        'name': '2단(보통크기)',
        'preset': {
            'AutoBreaksValue': 4.0,
            'StaffSizeValue': 7.2,
            'StavesMarginValue': 10.0,
            'SystemsMarginValue': 25.0,
            'InstrumentMarginValue': 3.0,
            'InstrumentNamesShowValue': True,
        }
    }
]


class MacroPreset():

    def __init__(self, preset):
        for key in preset.keys():
            setattr(self, key, preset[key])


PRESETS = [MacroPreset(preset) for preset in __PRESETS__]
