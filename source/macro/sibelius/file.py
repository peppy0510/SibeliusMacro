# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''

import base
import os


class Undo(base.MacroBase):

    name = 'Undo'

    def run(self):
        self.root.set_focus()
        self.root.key.bulk(['{CTRL}Z' * 120])


class SaveProject(base.MacroBase):

    name = 'Save Project'

    def run(self):
        self.root.key.esc()
        self.root.key.menu(['{CTRL}S'])


class ExportSVG(base.MacroBase):

    name = 'Export SVG'

    def run(self):
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
