# encoding: utf-8


'''
author: Taehong Kim
email: peppy0510@hotmail.com
'''


import glob
import os


debug = False
upx = True
onefile = True


PYZ = PYZ  # noqa
EXE = EXE  # noqa
COLLECT = COLLECT  # noqa
Analysis = Analysis  # noqa


class Path():

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def grapdatas(home, path, depth, mode, specs=None):
    datas = []
    for p in glob.glob(os.path.join(home, path, '*.*')):
        splpath = p.split(os.sep)
        if specs is None or splpath[-1] in specs:
            virpath = os.sep.join(splpath[-depth - 1:])
            datas += [(virpath, p, mode)]
    # for data in datas:
    #     print(data)
    return datas


path = Path(home=os.path.abspath(''),
            assets='assets',
            icon=os.path.join('assets', 'icon.ico'),
            macro=os.path.join('source', 'macro'),
            output=os.path.join('build', 'SibeliusMacro.exe'),
            uiautomationbin=os.path.join(os.environ['PATH'].split(';')[0], 'Lib\\site-packages\\uiautomation\\bin'))

a = Analysis([os.path.join('source', 'main.pyw')],
             hookspath=[path.macro],
             pathex=[path.home, path.macro, path.assets, path.uiautomationbin],
             hiddenimports=['macro', 'macro.base', 'macro.sibelius'])

a.datas += grapdatas(path.home, 'assets', 1, 'DATA', ['icon.ico'])

pyz = PYZ(a.pure)

if onefile:
    exe = EXE(pyz, a.scripts + [('O', '', 'OPTION')], a.binaries, a.zipfiles, a.datas,
              icon=path.icon, name=path.output, upx=upx, strip=None, debug=debug, console=debug)
else:
    exe = EXE(pyz, a.scripts, name=path.output, icon=path.icon,
              upx=upx, strip=None, debug=debug, console=debug, exclude_binaries=1)
    dist = COLLECT(exe, a.binaries, a.zipfiles, a.datas, upx=upx, strip=None, name='SibeliusMacro')
