# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import os
import sys
import time

from . keyboard import Keyboard  # noqa
from . mouse import Mouse  # noqa
from . control import Control  # noqa
from . params import Params  # noqa


class MacroBase():

    def __init__(self, root, params=None):
        self.root = root
        self.mouse = Mouse()
        self.params = params
        self.run()

    def wait(self, wait):
        time.sleep(wait * 0.001)
