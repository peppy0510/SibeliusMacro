# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import os


class ObjectItem():

    def __init__(self, path):
        self.path = path
        self.extension = os.path.splitext(path)[-1]
        self.filename = os.path.basename(path)
        self.directory = os.path.basename(os.path.dirname(path))
        self.basename = os.path.basename(path)
