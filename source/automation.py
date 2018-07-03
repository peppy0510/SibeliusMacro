# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import os
import sibtool
import sys
import time
import uiautomation
# import win32clipboard

from io import TextIOWrapper

# import subprocess
# from pywinauto.application import Application

sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def searchChildren(self, controls, depth=0, path=[0]):
    response = []
    controls = controls if isinstance(controls, list) else controls.GetChildren()
    for i, control in enumerate(controls):
        response += [(depth, path + [i], control)]
        response += self.searchChildren(control, depth=depth + 1, path=path + [i])
    return response


class SibeliusUIAutomation():

    def __init__(self):

        staff_size = 7.2
        staff_margin = 25
        show_instrument = False
        show_instrument_margin = 3
        fullnames_margin = show_instrument_margin + 6
        shortnames_margin = show_instrument_margin + 6

        self.mouse = sibtool.mouse()
        self.root = sibtool.control(uiautomation).get('WindowControl', includes=['- Sibelius'])
        self.hidePanels()
        self.setViewDocumentViewSinglePagesVertically()
        self.setViewInvisibles()
        self.setAppearanceInstrumentNames(show_instrument=show_instrument,
                                          show_instrument_margin=show_instrument_margin)
        self.setTextNumberingPageNumberChange()
        self.setTextNumberingEverySystem()
        self.setLayoutFormatUnlock()
        self.setLayoutDocumentSetup(staff_size=staff_size,
                                    staff_margin=staff_margin,
                                    fullnames_margin=fullnames_margin,
                                    shortnames_margin=shortnames_margin)
        self.setLayoutStaffSpacing(staves=10, systems=staff_margin)
        self.setLayoutStaffSpacingOptimize()
        self.setLayoutAutoBreak(4)
        self.setAppearanceResetNotesResetNoteSpacing()
        self.removeTitle()
        self.exportGraphicAsSVG()

    def hidePanels(self):
        self.root.key.esc()
        self.root.key.bulk(['{CTRL}{ALT}X'])
        # self.root.key.menu(['{ALT}|V|PN|HP'])

    def setLayoutStaffSpacing(self, staves=10, systems=20, extra_spaces=3):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|L|SE'])
        modal = sibtool.control(self.root).get('WindowControl', name='Engraving Rules')
        modal.key.bulk(['{TAB}{TAB}{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f' %
                        (staves, extra_spaces, extra_spaces, extra_spaces, systems)])
        modal.key.bulk(['{ENTER}'])

    def setLayoutStaffSpacingOptimize(self):
        self.root.key.esc()
        self.root.key.send(['{CTRL}A'])
        self.root.key.menu(['{ALT}|L|OS'])
        self.root.key.menu(['{ALT}|L|RB'])
        self.root.key.menu(['{ALT}|L|RA'])
        self.root.key.esc()
        # self.root.key.send(['{CTRL}{ALT}{Shift}.'], wait=200)
        # self.root.key.send(['{CTRL}{ALT}{Shift},'], wait=200)
        # self.root.key.send(['{CTRL}{ALT}{Shift}/'], wait=200)

    def setAppearanceResetNotesResetNoteSpacing(self):
        self.root.key.esc()
        self.root.key.send(['{CTRL}A'])
        self.root.key.menu(['{ALT}|A|RN'])
        self.root.key.esc()
        # self.root.key.send(['{CTRL}{ALT}{Shift}N'], wait=200)

    def removeTitle(self):

        def set_layout():
            self.root.key.menu(['{ALT}|V|FP'])
            self.root.key.bulk(['{CTRL}{HOME}|{CTRL}{PAGEUP}'])

        def get_position_title_modal():
            self.root.key.esc()
            self.root.key.menu(['{ALT}|A|DP'])
            modal = sibtool.control(self.root).get('WindowControl', name='Default Positions')
            modal.key.bulk(['{TAB}{END}' + '{UP}' * 6])
            modal.key.bulk(['{TAB}' * 5])
            return modal

        def get_position_composer_modal():
            self.root.key.esc()
            self.root.key.menu(['{ALT}|A|DP'])
            modal = sibtool.control(self.root).get('WindowControl', name='Default Positions')
            modal.key.bulk(['{TAB}{HOME}' + '{DOWN}' * 15])
            modal.key.bulk(['{TAB}' * 5])
            return modal

        def get_documentsetup_top_margin_modal():
            self.root.key.esc()
            self.root.key.bulk(['{CTRL}D'])
            # self.root.key.send(['{ALT}|L|DS'])
            modal = sibtool.control(self.root).get('WindowControl', name='Document Setup')
            # modal.key.bulk(['{ALT}M{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}'])
            return modal

        modal = get_position_title_modal()
        title_margin = modal.key.get_text()
        modal.key.bulk(['100{TAB}100'])
        modal.key.bulk(['{ENTER}'])

        modal = get_position_composer_modal()
        composer_margin = modal.key.get_text()
        # modal.key.bulk(['{TAB}'])
        # modal.key.get_text()
        modal.key.bulk(['100{TAB}100'])
        modal.key.bulk(['{ENTER}'])

        self.root.key.menu(['{ALT}|V|PV'])
        modal = get_documentsetup_top_margin_modal()
        modal.key.bulk(['{ALT}M{TAB}{TAB}'])
        page_width = float(modal.key.get_text())
        modal.key.bulk(['{ALT}M' + '{TAB}' * 9])
        prev_top_margin = modal.key.get_text()
        modal.key.bulk(['%0.2f' % (page_width + 15)])
        modal.key.bulk(['{ENTER}'])
        self.root.key.menu(['{ALT}|V|ZM|PW'])
        self.root.key.bulk(['{CTRL}{HOME}|{CTRL}{PAGEUP}'])

        score = sibtool.control(self.root).get('WindowControl', name='Score')
        rect = score.get_rect()
        position = self.mouse.get_position()

        margin = 1
        x = rect.x + margin
        y = rect.y + margin
        self.mouse.move(x, y)
        self.root.key.down('{SHIFT}')
        self.mouse.down(x, y)
        x = x + rect.width - margin * 2 - 19
        y = y + rect.width - margin * 2
        self.mouse.move(x, y)
        self.root.key.up(['{SHIFT}|{LSHIFT}|{RSHIFT}'])
        self.wait(50)
        self.mouse.up(x, y)
        self.wait(50)
        self.mouse.move(position.x, position.y)
        self.wait(50)
        self.root.key.send(['{DEL}'])
        modal = sibtool.control(self.root).get('WindowControl', includes=[
            'Deleting this text will remove it from the score and all of your parts.'])
        modal.key.bulk(['N'])
        modal = sibtool.control(self.root).get('WindowControl', name='Sibelius')
        modal.key.bulk(['{ENTER}'])

        modal = get_documentsetup_top_margin_modal()
        modal.key.bulk(['{ALT}M' + '{TAB}' * 9])
        modal.key.bulk(['%s' % (prev_top_margin)])
        modal.key.bulk(['{ENTER}'])
        self.root.key.menu(['{ALT}|V|FP'])
        self.root.key.bulk(['{CTRL}{HOME}|{CTRL}{PAGEUP}'])

        modal = get_position_title_modal()
        modal.key.bulk(['%s{TAB}%s' % (title_margin, title_margin)])
        modal.key.bulk(['{ENTER}'])

        modal = get_position_composer_modal()
        modal.key.bulk(['%s{TAB}%s' % (composer_margin, composer_margin)])
        modal.key.bulk(['{ENTER}'])

    def setViewDocumentViewSinglePagesVertically(self):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|V|PV'])
        self.root.key.menu(['{ALT}|V|FP'])
        self.root.key.bulk(['{CTRL}{HOME}|{CTRL}{PAGEUP}'])

    def setTextNumberingPageNumberChange(self):
        self.root.key.esc()
        self.root.key.send(['{CTRL}A'])
        self.root.key.menu(['{ALT}|T|PN'])
        modal = sibtool.control(self.root).get('WindowControl', name='Page Number Change')
        sibtool.control(modal).get('CheckBoxControl', includes=['New page number']).set_checkbox(True)
        modal.key.bulk(['{TAB}{TAB}{HOME}{TAB}{END}{UP}{UP}{UP}{DOWN}{DOWN}'])
        modal.key.bulk(['{ENTER}'])
        modal = sibtool.control(self.root).get('WindowControl', includes=[
            'There is something selected which is not in view'])
        modal.key.bulk(['Y'])
        self.root.key.esc()

    def setTextNumberingEverySystem(self):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|T|ES'])

    def setLayoutFormatUnlock(self):
        self.root.key.esc()
        self.root.key.send(['{CTRL}A'])
        self.root.key.bulk(['{CTRL}{SHIFT}U'])
        # self.root.key.menu(['{ALT}|L|UF'])
        self.root.key.esc()

    def setLayoutDocumentSetup(self, margin=14, staff_size=7.2, staff_margin=20,
                               fullnames_margin=8, shortnames_margin=8, nonames_margin=0):

        self.root.key.esc()
        self.root.key.bulk(['{CTRL}D'])
        # self.root.key.menu(['{ALT}|L|DS'])
        modal = sibtool.control(self.root).get('WindowControl', name='Document Setup')
        sibtool.control(modal).get('CheckBoxControl', name='After first page:').set_checkbox(True)
        modal.key.bulk(['{ALT}M{TAB}{HOME}{DOWN}{DOWN}{DOWN}{DOWN}'])
        modal.key.send(['{ALT}O'])
        modal.key.bulk(['{TAB}{TAB}{TAB}%0.2f' % (staff_size)])
        modal.key.send(['{ALT}A'])
        modal.key.bulk(['{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f' %
                        (margin, margin, margin, margin)])
        modal.key.bulk(['{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f' %
                        (staff_margin, fullnames_margin, shortnames_margin, nonames_margin, staff_margin)])
        modal.key.bulk(['{TAB}{TAB}%0.2f{TAB}%0.2f' % (staff_margin, staff_margin)])
        modal.key.bulk(['{Enter}'])

    def setLayoutAutoBreak(self, bars):
        self.root.key.esc()
        self.root.key.send(['{CTRL}A'])
        self.root.key.menu(['{ALT}|L|AB'])
        modal = sibtool.control(self.root).get('WindowControl', name='Auto Breaks')
        sibtool.control(modal).get('CheckBoxControl', name='Use auto system breaks').set_checkbox(True)
        sibtool.control(modal).get('CheckBoxControl', name='Use multirests').set_checkbox(False)
        sibtool.control(modal).get('CheckBoxControl', name='Use auto page breaks').set_checkbox(False)
        modal.key.bulk(['{TAB}{SPACE}{TAB}%d' % (bars)])
        modal.key.bulk(['{Enter}'])
        self.root.key.esc()
        self.root.key.bulk(['{CTRL}{HOME}|{CTRL}{PAGEUP}'])

    def setViewInvisibles(self):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|V'])
        self.root.key.esc()
        sibtool.control(self.root).filter('CheckBoxControl', includes=[
            'Invisibles group']).set_checkbox(False)
        sibtool.control(self.root).get('CheckBoxControl', includes=[
            'Invisibles group', 'Displays hidden objects in light gray']).set_checkbox(True)

    def setAppearanceInstrumentNames(self, show_instrument=False, show_instrument_margin=3):
        value = '{HOME}' if show_instrument else '{END}'
        show_instrument_margin = show_instrument_margin if show_instrument else 0
        self.root.key.esc()
        self.root.key.menu(['{ALT}|A|IE'])
        modal = sibtool.control(self.root).get('WindowControl', name='Engraving Rules')
        modal.key.bulk(['{TAB}{TAB}{TAB}%s{TAB}{END}{TAB}{END}' % (value)])
        modal.key.bulk(['{TAB}{TAB}%0.2f' % (show_instrument_margin)])
        sibtool.control(self.root).get('CheckBoxControl', includes=[
            'Change instrument names at start of system']).set_checkbox(False)
        modal.key.bulk(['{Enter}'])

    # def setTextNumbering(self):
    #     self.root.sendkeys(['{Esc}{Esc}|{ALT}|T|BE'])
    #     modal = sibtool.control(self.root).get('WindowControl', name='Engraving Rules')
    #     modal.key.send(['{TAB}{TAB}{TAB}{Home}{Down}{Space}'])
    #     sibtool.control(modal).get('CheckBoxControl', includes=['Show on first bar of sections']).set_checkbox(False)
    #     sibtool.control(modal).get('CheckBoxControl', includes=['Hide at rehearsal marks']).set_checkbox(False)
    #     sibtool.control(modal).get('CheckBoxControl', includes=['Count repeats:']).set_checkbox(False)
    #     sibtool.control(modal).get('CheckBoxControl', includes=['Show range of bars on multirests']).set_checkbox(False)
    #     modal.key.send(['{Enter}'])

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

    def exportGraphicAsSVG(self):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|F|E|GR|GF'])
        self.root.key.bulk(['{End}|{Enter}'])
        self.root.key.menu(['{ALT}|E|AL'])
        self.root.key.menu(['{ALT}|E|FI'])
        filename = self.root.key.get_text()
        self.root.key.menu(['{ALT}|E|FO'])
        directory = self.root.key.get_text()
        # print(os.path.join(directory, filename))
        for path in os.listdir(directory):
            fullpath = os.path.join(directory, path)
            name, ext = os.path.splitext(path)
            banename = '_'.join(name.split('_')[:-1])
            if ext.lower() == '.svg' and filename == banename:
                os.remove(fullpath)

        self.wait(100)
        self.root.key.menu(['{ALT}|E|O'])

    def wait(self, wait):
        time.sleep(wait * 0.001)


def main():
    sibelius = SibeliusUIAutomation()


if __name__ == '__main__':
    main()


# def xxx():

#     print(sibeliusWindow.Name)
#     print(sibeliusWindow.ClassName)
#     print(dir(sibeliusWindow))
#     sibeliusWindow.MoveWindow(0, 0, 4000, 1000)
#     x = sibeliusWindow.CustomControl(searchDepth=10, Name='Layout ribbon tab L')
#     x = sibeliusWindow.Control(searchDepth=10, SubName='File')

#     response = searchChildren(sibeliusWindow.GetChildren())
#     for depth, path, control in response:
#         if ispath(path, [0, 1, 1, 1, 1, 0, 6, 0, 0, 0]):
#             print(depth, path, control)

#     control.Click()

#     break
#     [0, 0, 1, 1, 0]
#     [0, 0, 1, 1, 0, 0]
#     [0, 0, 1, 1, 0, 1]
#         control.Click()
#         print(depth, path, control)

#     print(dir(automation))
#     print(automation.GetRootControl())
#     subprocess.Popen('notepad.exe')
#     sibeliusWindow = automation.WindowControl(searchDepth=1, ClassName='Notepad')

#     menuBarControl = sibeliusWindow.MenuItemControl(searchDepth=10)

#     for i, titleBar in enumerate(sibeliusWindow.PaneControl().GetChildren()):
#         # print(i, titleBar)
#         for ii, menuBar in enumerate(titleBar.GetChildren()):
#             print(i, ii, menuBar)
#             if i == 0
#     for iii, x in enumerate(menuBar.GetChildren()):
#         print(i, ii, iii, x)
#     for iiii, xx in enumerate(x.GetChildren()):
#         print(i, ii, iii, iiii, xx)
#     for iiii, xxx in enumerate(xx.GetChildren()):
#         print(i, ii, iii, iiii, xxx)
#         if i == 1 and ii == 1 and iii == 1 and iiii == 4:
#             xxx.Click()
#     if i == 0 and ii == 10:
#         print(i, ii, menuBar)
#         menuBar.Click()
#     for v in menuBar.GetChildren():
#         print(v)

#     print(menuBarControl)
#     for menu in menuBarControl.GetChildren():
#     print(menu)
#     for v in x.GetChildren():
#         print(v)
#     v.Click()
#     print(dir(v))
#     print(x.GetChildren())
#     print(dir(x))
#     print(searchChildren(x))
#     x.click()
#     optimize = sibeliusWindow.ButtonControl(searchDepth=10, SubName='Optimize')
#     x.Click()
#     x.SetFocus()
#     x.SetActive()

#     print(dir(x))

#     for v in sibeliusWindow.GetChildren():

#     for v in sibeliusWindow.GetChildren():
#         for vv in v.GetChildren():
#             print('vv', vv)
#             for vvv in vv.GetChildren():
#                 print('vvv', vvv)
#                 for vvvv in vvv.GetChildren():
#                     print('vvvv', vvvv)
#                     for vvvvv in vvvv.GetChildren():
#                         print('vvvvv', vvvvv)
#                         for vvvvvv in vvvvv.GetChildren():
#                             print('vvvvvv', vvvvvv)
#                             for vvvvvvv in vvvvvv.GetChildren():
#                                 print('vvvvvvv', vvvvvvv)
#                                 for vvvvvvvv in vvvvvvv.GetChildren():
#                                     print('vvvvvvvv', vvvvvvvv)
#     print(sibeliusWindow.GetChildren())
#     menuItemControl = sibeliusWindow.MenuControl(searchDepth=1, SubName='Layout')
#     print(menuItemControl)
#     MenuControl # MenuItemControl # TabControl
#     notepadWindow.SetTopmost(True)
#     edit = notepadWindow.EditControl()
#     edit.SetValue('Hello')
#     edit.SendKeys('{CTRL}{End}{Enter}World')
