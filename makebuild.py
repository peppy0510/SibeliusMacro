# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import os
import shutil
import subprocess
import sys


path = os.environ['PATH']
os.environ['PATH'] = ';'.join([path, os.path.join(path.split(';')[0], 'Scripts')])


class Build():

    @classmethod
    def run(self):
        self.remove()
        self.makebuild()
        # self.runtest()
        self.makeinstaller()

    @classmethod
    def remove(self):
        remove_paths = ['dist', 'build']
        for path in remove_paths:
            path = os.path.abspath(path)
            if os.path.isdir(path):
                try:
                    shutil.rmtree(path)
                    # print('removing %s' % (path))
                except Exception:
                    print('removing failed %s' % (path))

    @classmethod
    def makebuild(self):
        # proc = subprocess.Popen('pyinstaller --uac-admin makebuild.spec', shell=True)
        proc = subprocess.Popen('pyinstaller makebuild.spec', shell=True)
        proc.communicate()

        # uiautomationbin = os.path.join(os.environ['PATH'].split(';')[0], 'Lib\\site-packages\\uiautomation\\bin')
        # for name in os.listdir(uiautomationbin):
        #     print(name, '*' * 100)
        #     shutil.copyfile(os.path.join(uiautomationbin, name),
        #                     os.path.abspath(os.path.join('dist', name)))

        os.mkdir(os.path.join('dist', 'assets'))
        shutil.copyfile(os.path.join('assets', 'icon.ico'),
                        os.path.join('dist', 'assets', 'icon.ico'))

    @classmethod
    def runtest(self):
        command = os.path.join('dist', 'SibeliusMacro.exe')
        proc = subprocess.Popen(command, shell=True)
        proc.communicate()

    @classmethod
    def makeinstaller(self):

        for name in os.listdir('dist'):
            if os.path.splitext(name)[0][-1].isdigit():
                os.remove(os.path.join('dist', name))

        issc = r'''"C:\\Program Files (x86)\\Inno Setup 5\\ISCC.exe"'''
        command = '''%s "makeinstaller.iss"''' % (issc)
        proc = subprocess.Popen(command, shell=True)
        proc.communicate()


if __name__ == '__main__':
    from io import TextIOWrapper
    sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    Build.run()
