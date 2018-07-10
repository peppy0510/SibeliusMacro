# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import base


class HidePanels(base.MacroBase):

    name = 'Hide Panels'

    def run(self):
        self.root.key.esc()
        self.root.key.bulk(['{CTRL}{ALT}X'])
        # self.root.key.menu(['{ALT}|V|PN|HP'])


class SinglePagesVertically(base.MacroBase):

    name = 'Single Pages Vertically'

    def run(self):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|V|PV'])
        self.root.key.menu(['{ALT}|V|FP'])
        self.root.key.bulk(['{CTRL}{HOME}|{CTRL}{PAGEUP}'])


class Invisibles(base.MacroBase):

    name = 'Invisibles'

    def run(self):

        includes = ['Invisibles group']
        excludes = ['Page Margins', 'Hidden Objects']

        self.root.key.esc()
        self.root.key.menu(['{ALT}|V'])
        self.root.key.esc()

        for include in excludes:
            base.Control(self.root).get('CheckBoxControl', includes=includes + [include]).set_checkbox(True)

        base.Control(self.root).filter('CheckBoxControl', includes=includes, excludes=excludes).set_checkbox(False)
