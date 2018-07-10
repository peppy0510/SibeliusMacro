# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import os
import sys
import threading
import time
import uiautomation

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import base  # noqa
import sibelius  # noqa

from base import Params as SibeliusParams  # noqa


class SibeliusStatus():

    def __init__(self, total):
        self.done = 0
        self.left = total
        self.total = total
        self.name = ''

    def count(self, name):
        self.left -= 1
        self.done += 1
        self.name = name


class Sibelius():

    def __init__(self,
                 params=base.Params(staff_size=7.2,
                                    staves_size=10,
                                    systems_size=25,
                                    show_instrument_name=False,
                                    instrument_staff_margin=12,
                                    instrument_name_barline_gap=1,
                                    auto_breaks_bars=4),
                 targets=[], includes=[], excludes=[]):

        self.initialize_macros()
        self.initialize_thread()
        self.mouse = base.Mouse()
        self.root = base.Control(uiautomation).get(
            'WindowControl', includes=includes + [' - Sibelius'], excludes=excludes)

        self.params = params
        self.targets = targets
        self.macros = self.targets_to_macros(targets)
        self.status = SibeliusStatus(len(self.macros))

        # sibelius.layout.AutoBreaks(self.root, self.params)
        if len(self.root.controls) > 0:
            self.run()

    def initialize_macros(self):
        self.file = sibelius.file
        self.view = sibelius.view
        self.text = sibelius.text
        self.title = sibelius.title
        self.layout = sibelius.layout
        self.appearance = sibelius.appearance

    def initialize_thread(self):
        self.thread = None
        self.thread_stop = False
        self.thread_interval = 50

    def targets_to_macros(self, targets):
        attrs = []
        for target in targets:
            for tab in (self.file, self.view, self.text,
                        self.title, self.layout, self.appearance):
                if hasattr(tab, target):
                    attrs += [getattr(tab, target)]
        return attrs

    def run(self):

        while True:

            if self.thread_stop:
                return

            if self.thread and self.thread.isAlive():
                time.sleep(self.thread_interval * 0.001)
                continue
            else:
                self.thread = None

            if len(self.macros) == 0 and self.thread is None:
                return

            macro = self.macros.pop(0)
            self.status.count(macro.name)
            self.thread = threading.Thread(target=macro, args=(self.root, self.params))
            # self.thread.setDaemon(True)
            self.thread.run()

    def stop(self):
        self.thread_stop = True

    # def test(self):
    #     sibelius.view.HidePanels(self.root, self.params)
    #     sibelius.view.Invisibles(self.root, self.params)
    #     sibelius.view.SinglePagesVertically(self.root, self.params)
    #     sibelius.layout.UnlockFormat(self.root, self.params)
    #     sibelius.layout.AutoBreaks(self.root, self.params)
    #     sibelius.layout.DocumentSetup(self.root, self.params)
    #     sibelius.layout.StaffSpacing(self.root, self.params)
    #     sibelius.layout.StaffSpacingOptimize(self.root, self.params)
    #     sibelius.appearance.InstrumentNames(self.root, self.params)
    #     sibelius.appearance.NoteSpace(self.root, self.params)
    #     sibelius.text.HidePageNumbers(self.root, self.params)
    #     sibelius.text.MeasureNumbers(self.root, self.params)
    #     sibelius.title.RemoveTitle(self.root, self.params)
    #     sibelius.file.ExportSVG(self.root, self.params)
    #     sibelius.file.SaveProject(self.root, self.params)
    #     sibelius.file.Undo(self.root, self.params)


def test():
    # sibelius.layout.AutoBreaks(self.root, self.params)
    Sibelius(targets=['AutoBreaks'])
    Sibelius(targets=['HidePageNumbers'])
    # Sibelius(targets=['HidePanels', 'Invisibles'])
    # Sibelius(targets=[
    #     'HidePanels', 'Invisibles', 'SinglePagesVertically',
    #     'UnlockFormat', 'AutoBreaks', 'DocumentSetup',
    #     'StaffSpacing', 'StaffSpacingOptimize', 'InstrumentNames',
    #     'NoteSpace', 'HidePageNumbers', 'MeasureNumbers', 'RemoveTitle'])
    # Sibelius(targets=['Undo'])
    # Sibelius(targets=['ExportSVG', 'SaveProject'])


if __name__ == '__main__':
    from io import TextIOWrapper
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    test()
