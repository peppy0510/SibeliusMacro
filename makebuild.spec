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


__default_python_path__ = 'C:\\Program Files\\Python36'
__appname__ = 'SibeliusMacro'
__api_ms_win_crt_path__ = 'C:\\Windows\\WinSxS\\amd64_microsoft-windows-m..namespace-downlevel_31bf3856ad364e35_10.0.17763.1_none_b82ac495d943b9d7'


class Path():

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            kwargs[key] = os.path.abspath(kwargs[key])
        self.__dict__.update(kwargs)


def grapdatas(home, path, depth, mode, specs=None):
    datas = []
    for p in glob.glob(os.path.join(home, path, '*.*')):
        splpath = p.split(os.sep)
        if specs is None or splpath[-1] in specs:
            virpath = os.sep.join(splpath[-depth - 1:])
            datas += [(virpath, p, mode)]
    return datas


path = Path(
    home='',
    base=os.path.join('source', 'base'),
    assets=os.path.join('assets'),
    icon=os.path.join('assets', 'icon', 'icon.ico'),
    dlls=os.path.join('assets', 'dlls'),
    output=os.path.join('build', '{}.exe'.format(__appname__)),
    macro=os.path.join('source', 'macro'),
    winsxs=__api_ms_win_crt_path__,
    uiautomationbin=os.path.join(__default_python_path__, 'Lib\\site-packages\\uiautomation\\bin')
)


# path = Path(home=os.path.abspath(''),
#             assets='assets',
#             icon=os.path.join('assets', 'icon.ico'),
#             macro=os.path.join('source', 'macro'),
#             output=os.path.join('build', 'SibeliusMacro.exe'),
#             uiautomationbin=os.path.join(os.environ['PATH'].split(';')[0], 'Lib\\site-packages\\uiautomation\\bin'))


a = Analysis([os.path.join('source', 'main.pyw')],
             hookspath=[path.macro],
             pathex=[path.home, path.macro, path.assets,
                     path.uiautomationbin, path.dlls, path.winsxs],
             hiddenimports=['macro', 'macro.base', 'macro.sibelius'])

# a = Analysis([os.path.join('source', 'main.py')],
#              hookspath=[path.home, path.base, path.assets],
#              pathex=[path.home, path.assets, path.dlls, path.winsxs],
#              hiddenimports=['base'])

# a.datas += grapdatas(path.home, 'assets', 1, 'DATA', ['icon.ico'])

a.datas += grapdatas(path.assets, 'icon', 2, 'data', ['icon.ico'])

print('-' * 100)
for v in a.datas:
    print(v)
print('-' * 100)

pyz = PYZ(a.pure)

if onefile:
    exe = EXE(pyz, a.scripts + [('O', '', 'OPTION')],
              a.binaries, a.zipfiles, a.datas,
              uac_admin=True, uac_uiaccess=True,
              icon=path.icon, name=path.output,
              upx=upx, strip=None, debug=debug, console=debug)
    # runtime_tmpdir='%HOMEPATH%\\AppData\\Local\\Temp\\' + name
else:
    exe = EXE(pyz, a.scripts, name=path.output, icon=path.icon,
              uac_admin=True, uac_uiaccess=True, upx=upx, strip=None,
              debug=debug, console=debug, exclude_binaries=1)
    dist = COLLECT(exe, a.binaries, a.zipfiles, a.datas,
                   upx=upx, strip=None, name=__appname__)
