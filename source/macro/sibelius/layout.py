# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import base


class UnlockFormat(base.MacroBase):

    name = 'Unlock Format'

    def run(self, event=None):
        self.root.key.esc()
        self.root.selectall()
        self.root.key.bulk(['{CTRL}{SHIFT}U'])
        # self.root.key.menu(['{ALT}|L|UF'])
        self.root.key.esc()


class AutoBreaks(base.MacroBase):

    name = 'Auto Breaks'

    def run(self):
        self.root.key.esc()
        self.root.selectall()
        self.root.key.menu(['{ALT}|L|AB'])
        modal = base.Control(self.root).get('WindowControl', name='Auto Breaks')
        # modal = base.Control(self.root).get('WindowControl', excludes=['Score'])
        base.Control(modal).get('CheckBoxControl', includes=['Use auto system breaks']).set_checkbox(True)
        base.Control(modal).get('CheckBoxControl', includes=['Use multirests']).set_checkbox(False)
        base.Control(modal).get('CheckBoxControl', includes=['Use auto page breaks']).set_checkbox(False)
        modal.key.bulk(['{TAB}{SPACE}{TAB}%d' % (self.params.auto_breaks_bars)])
        modal.key.bulk(['{Enter}'])
        self.root.key.esc()
        self.root.key.bulk(['{CTRL}{HOME}|{CTRL}{PAGEUP}'])


class StaffSpacing(base.MacroBase):

    name = 'Staff Spacing'

    def run(self):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|L|SE'])
        modal = base.Control(self.root).get('WindowControl', name='Engraving Rules')
        # modal = base.Control(self.root).get('WindowControl', excludes=['Score'])
        modal.key.bulk([''.join([
            ('{TAB}{TAB}{TAB}%0.2f' % (self.params.staves_size)),
            ('{TAB}%0.2f' % (self.params.page_extra_spaces)) * 3,
            ('{TAB}%0.2f' % (self.params.systems_size))
        ])])
        modal.key.bulk(['{ENTER}'])


class StaffSpacingOptimize(base.MacroBase):

    name = 'Staff Spacing Optimize'

    def run(self):
        self.root.key.esc()
        self.root.selectall()
        self.wait(150)
        self.root.key.menu(['{ALT}|L|RB'])
        self.root.key.menu(['{ALT}|L|RA'])
        self.root.key.menu(['{ALT}|L|OS'])
        self.root.key.esc()
        # self.root.key.send(['{CTRL}{ALT}{Shift}.'], wait=200)
        # self.root.key.send(['{CTRL}{ALT}{Shift},'], wait=200)
        # self.root.key.send(['{CTRL}{ALT}{Shift}/'], wait=200)


class DocumentSetup(base.MacroBase):

    name = 'Document Setup'

    def run(self):
        self.root.key.esc()
        self.root.key.bulk(['{CTRL}D'])
        # self.root.key.menu(['{ALT}|L|DS'])
        modal = base.Control(self.root).get('WindowControl', name='Document Setup')
        # modal = base.Control(self.root).get('WindowControl', excludes=['Score'])
        base.Control(modal).get('CheckBoxControl', includes=['After first page']).set_checkbox(True)
        modal.key.bulk([('{ALT}M{TAB}{HOME}') + ('{DOWN}' * 4)])
        modal.key.menu(['{ALT}O'])
        modal.key.bulk(['{TAB}{TAB}{TAB}%0.2f' % (self.params.staff_size)])
        modal.key.menu(['{ALT}A'])
        modal.key.bulk([('{TAB}%0.2f' % (self.params.page_margin)) * 4])
        modal.key.bulk([''.join([
            ('{TAB}%0.2f' % (self.params.staff_margin)),
            ('{TAB}%0.2f' % (self.params.instrument_staff_margin)),
            ('{TAB}%0.2f' % (self.params.instrument_staff_margin)),
            ('{TAB}%0.2f' % (0)),
            ('{TAB}%0.2f' % (self.params.staff_margin))
        ])])
        modal.key.bulk([''.join([
            ('{TAB}'),
            ('{TAB}%0.2f' % (self.params.staff_margin)),
            ('{TAB}%0.2f' % (self.params.staff_margin))
        ])])
        modal.key.bulk(['{Enter}'])

# def setLayoutDocumentSetupMargins(self):
#     self.sendKeys(['{Esc}|{ALT}|l|ma|{Home}|{Enter}'])

# def setLayoutDocumentSetupOrientation(self):
#     self.sendKeys(['{Esc}|{ALT}|l|or|{Home}|{Enter}'])

# def setLayoutDocumentSetupSize(self):
#     self.sendKeys(['{Esc}|{ALT}|l|ps|{Home}{Down}{Down}{Down}{Down}|{Enter}'])

# def setLayoutDocumentSetupNormalStaffSize(self, value=7.2):
#     self.sendKeys(['{Esc}|{ALT}|l|ss|%.02f|{Enter}' % (value)])

# def setLayoutStaffSpacingStaves(self, value=10):
#     self.sendKeys(['{Esc}|{ALT}|l|st|%.02f{Enter}' % (value)])

# def setLayoutStaffSpacingSystems(self, value=20):
#     self.sendKeys(['{Esc}|{ALT}|l|sy|%.02f{Enter}' % (value)])

# def setLayoutStaffSpacingOptimize(self):
#     self.sendKeys(['{Esc}|{CTRL}a|{ALT}|l|rb',
#                    '{Esc}|{CTRL}a|{ALT}|l|ra',
#                    '{Esc}|{CTRL}a|{ALT}|l|os'])
