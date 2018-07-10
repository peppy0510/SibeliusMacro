# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import os
import sys

sys.path.insert(0, os.path.basename(__name__))

import base  # noqa


class MeasureNumbers(base.MacroBase):

    name = 'Measure Numbers'

    def run(self):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|T|ES'])


class HidePageNumbers(base.MacroBase):

    name = 'Hide Page Numbers'

    def run(self):
        self.root.key.esc()
        self.root.key.send(['{CTRL}A'])
        self.root.key.menu(['{ALT}|T|PN'])
        modal = base.Control(self.root).get('WindowControl', name='Page Number Change')
        base.Control(modal).get('CheckBoxControl', includes=['New page number']).set_checkbox(True)
        modal.key.bulk(['{TAB}{TAB}{HOME}{TAB}{END}{UP}{UP}{UP}{DOWN}{DOWN}'])
        modal.key.bulk(['{ENTER}'])
        modal = base.Control(self.root).get('WindowControl', includes=[
            'There is something selected which is not in view'])
        modal.key.bulk(['Y'])
        self.root.key.esc()


# def setTextNumbering(self):
#     self.root.sendkeys(['{Esc}{Esc}|{ALT}|T|BE'])
#     modal = base.Control(self.root).get('WindowControl', name='Engraving Rules')
#     modal.key.send(['{TAB}{TAB}{TAB}{Home}{Down}{Space}'])
#     base.Control(modal).get('CheckBoxControl', includes=['Show on first bar of sections']).set_checkbox(False)
#     base.Control(modal).get('CheckBoxControl', includes=['Hide at rehearsal marks']).set_checkbox(False)
#     base.Control(modal).get('CheckBoxControl', includes=['Count repeats:']).set_checkbox(False)
#     base.Control(modal).get('CheckBoxControl', includes=['Show range of bars on multirests']).set_checkbox(False)
#     modal.key.send(['{Enter}'])
