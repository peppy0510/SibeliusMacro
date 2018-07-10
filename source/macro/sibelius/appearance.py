# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import base  # noqa


class NoteSpace(base.MacroBase):

    name = 'Note Space'

    def run(self, event=None):
        self.root.key.esc()
        self.root.key.send(['{CTRL}A'])
        self.root.key.menu(['{ALT}|A|RN'])
        self.root.key.esc()
        # self.root.key.send(['{CTRL}{ALT}{Shift}N'], wait=200)


class InstrumentNames(base.MacroBase):

    name = 'Instrument Names'

    def run(self, event=None):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|A|IE'])
        modal = base.Control(self.root).get('WindowControl', name='Engraving Rules')
        modal.key.bulk([''.join([
            ('{TAB}' * 3),
            ('{HOME}' if self.params.show_instrument_name else '{END}'),
            ('{TAB}{END}' * 2)
        ])])
        modal.key.bulk([''.join([
            ('{TAB}' * 2),
            ('%0.2f' % (self.params.instrument_name_barline_gap if self.params.show_instrument_name else 0)),
            ('{TAB}{END}' * 2)
        ])])
        base.Control(self.root).get('CheckBoxControl', includes=[
            'Change instrument names at start of system']).set_checkbox(False)
        modal.key.bulk(['{Enter}'])
