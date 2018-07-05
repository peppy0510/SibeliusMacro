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


class SibeliusRemoveTitle():

    def removeTitle(self, event=None):

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
        # return True


class SibeliusLayoutDocumentSetup():

    def hidePanels(self, event=None):
        self.root.key.esc()
        self.root.key.bulk(['{CTRL}{ALT}X'])
        # self.root.key.menu(['{ALT}|V|PN|HP'])

    def setLayoutStaffSpacing(self, event=None):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|L|SE'])
        modal = sibtool.control(self.root).get('WindowControl', name='Engraving Rules')
        modal.key.bulk(['{TAB}{TAB}{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f' %
                        (self.staves, self.extra_spaces, self.extra_spaces, self.extra_spaces, self.systems)])
        modal.key.bulk(['{ENTER}'])

    def setLayoutStaffSpacingOptimize(self, event=None):
        self.root.key.esc()
        self.root.key.send(['{CTRL}A'])
        self.wait(150)
        self.root.key.menu(['{ALT}|L|RB'])
        self.root.key.menu(['{ALT}|L|RA'])
        self.root.key.menu(['{ALT}|L|OS'])
        self.root.key.esc()
        # self.root.key.send(['{CTRL}{ALT}{Shift}.'], wait=200)
        # self.root.key.send(['{CTRL}{ALT}{Shift},'], wait=200)
        # self.root.key.send(['{CTRL}{ALT}{Shift}/'], wait=200)

    def setLayoutDocumentSetup(self, event=None):
        self.root.key.esc()
        self.root.key.bulk(['{CTRL}D'])
        # self.root.key.menu(['{ALT}|L|DS'])
        modal = sibtool.control(self.root).get('WindowControl', name='Document Setup')
        sibtool.control(modal).get('CheckBoxControl', name='After first page:').set_checkbox(True)
        modal.key.bulk(['{ALT}M{TAB}{HOME}{DOWN}{DOWN}{DOWN}{DOWN}'])
        modal.key.menu(['{ALT}O'])
        modal.key.bulk(['{TAB}{TAB}{TAB}%0.2f' % (self.staff_size)])
        modal.key.menu(['{ALT}A'])
        modal.key.bulk(['{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f' %
                        (self.page_margin, self.page_margin, self.page_margin, self.page_margin)])
        modal.key.bulk(['{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f{TAB}%0.2f' %
                        (self.staff_margin, self.fullnames_margin,
                            self.shortnames_margin, self.nonames_margin, self.staff_margin)])
        modal.key.bulk(['{TAB}{TAB}%0.2f{TAB}%0.2f' % (self.staff_margin, self.staff_margin)])
        modal.key.bulk(['{Enter}'])


class SibeliusUIAutomation(SibeliusLayoutDocumentSetup):

    def __init__(self, parent=None):

        self.parent = parent
        self.stop = False
        self.staff_size = 7.2
        self.staves = 10
        self.staff_margin = 25
        self.systems = self.staff_margin
        self.show_instrument = False
        self.show_instrument_margin = 3
        self.extra_spaces = 3
        self.page_margin = 14
        names_margin = int(self.staff_size * 1.9 + self.show_instrument_margin - 2)
        self.fullnames_margin = names_margin
        self.shortnames_margin = names_margin
        self.nonames_margin = 0
        self.auto_break_bars = 4
        self.mouse = sibtool.mouse()
        self.root = sibtool.control(uiautomation).get('WindowControl', includes=['- Sibelius'])
        # self.runall()

    def runall(self, event=None):
        self.hidePanels()
        self.setViewDocumentViewSinglePagesVertically()
        self.setViewInvisibles()
        self.setAppearanceInstrumentNames()
        self.setTextNumberingPageNumberChange()
        self.setTextNumberingEverySystem()
        self.setLayoutFormatUnlock()
        self.setLayoutDocumentSetup()
        self.setLayoutStaffSpacing(staves=self.staves, systems=self.staff_margin)
        self.setLayoutStaffSpacingOptimize()
        self.setLayoutAutoBreak()
        self.setAppearanceResetNotesResetNoteSpacing()
        self.removeTitle()
        self.exportGraphicAsSVG()

    def setLayout(self, event=None):
        self.setAppearanceInstrumentNames()
        self.setLayoutDocumentSetup()
        self.setLayoutStaffSpacing()
        self.setLayoutStaffSpacingOptimize()

    def setAppearanceResetNotesResetNoteSpacing(self, event=None):
        self.root.key.esc()
        self.root.key.send(['{CTRL}A'])
        self.root.key.menu(['{ALT}|A|RN'])
        self.root.key.esc()
        # self.root.key.send(['{CTRL}{ALT}{Shift}N'], wait=200)

    def setViewDocumentViewSinglePagesVertically(self, event=None):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|V|PV'])
        self.root.key.menu(['{ALT}|V|FP'])
        self.root.key.bulk(['{CTRL}{HOME}|{CTRL}{PAGEUP}'])

    def setTextNumberingPageNumberChange(self, event=None):
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

    def setTextNumberingEverySystem(self, event=None):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|T|ES'])

    def setLayoutFormatUnlock(self, event=None):
        self.root.key.esc()
        self.root.key.send(['{CTRL}A'])
        self.root.key.bulk(['{CTRL}{SHIFT}U'])
        # self.root.key.menu(['{ALT}|L|UF'])
        self.root.key.esc()

    def setLayoutAutoBreak(self, event=None):
        self.root.key.esc()
        self.root.key.send(['{CTRL}A'])
        self.root.key.menu(['{ALT}|L|AB'])
        modal = sibtool.control(self.root).get('WindowControl', name='Auto Breaks')
        sibtool.control(modal).get('CheckBoxControl', name='Use auto system breaks').set_checkbox(True)
        sibtool.control(modal).get('CheckBoxControl', name='Use multirests').set_checkbox(False)
        sibtool.control(modal).get('CheckBoxControl', name='Use auto page breaks').set_checkbox(False)
        modal.key.bulk(['{TAB}{SPACE}{TAB}%d' % (self.auto_break_bars)])
        modal.key.bulk(['{Enter}'])
        self.root.key.esc()
        self.root.key.bulk(['{CTRL}{HOME}|{CTRL}{PAGEUP}'])

    def setViewInvisibles(self, event=None):
        self.root.key.esc()
        self.root.key.menu(['{ALT}|V'])
        self.root.key.esc()
        sibtool.control(self.root).filter('CheckBoxControl', includes=[
            'Invisibles group']).set_checkbox(False)
        sibtool.control(self.root).get('CheckBoxControl', includes=[
            'Invisibles group', 'Page Margins']).set_checkbox(True)
        sibtool.control(self.root).get('CheckBoxControl', includes=[
            'Invisibles group', 'Hidden Objects']).set_checkbox(True)

    def setAppearanceInstrumentNames(self, event=None):
        value = '{HOME}' if self.show_instrument else '{END}'
        show_instrument_margin = self.show_instrument_margin if self.show_instrument else 0
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

    def exportGraphicAsSVG(self, event=None):
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
        # return True

    def saveProjectFile(self, event=None):
        self.root.key.esc()
        self.root.key.menu(['{CTRL}S'])
        return True

    def wait(self, wait):
        time.sleep(wait * 0.001)


def main():
    SibeliusUIAutomation()


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
