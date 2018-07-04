# encoding: utf-8

################################################################################
# MACROBOX Main
#-------------------------------------------------------------------------------
# author: Taehong Kim / MUTEKLAB
# email: peppy0510@hotmail.com / thkim@muteklab.com
################################################################################

################################################################################
# Project Environment
#-------------------------------------------------------------------------------
import os, sys, re, psutil, shutil, subprocess
#-------------------------------------------------------------------------------
# end of Project Environment
################################################################################

################################################################################
# Main Entry
#-------------------------------------------------------------------------------
def main():
	#---------------------------------------------------------------------------
	remove_paths = [r'build', r'dist\pyrenamer']
	for path in remove_paths:
		path = os.path.abspath(path)
		print 'removing %s' % (path)
		try: shutil.rmtree(path)
		except: pass
	#---------------------------------------------------------------------------
	builder_path = r'''C:\Program Files (x86)\Python27\Lib'''
	builder_path += r'''\site-packages\pyinstaller\pyinstaller.py'''
	commands = ['python -O "%s" "pyrenamer.spec"' % (builder_path)]
	for command in commands:
		proc = subprocess.Popen(command, shell=True)
		resp = proc.communicate()[0]; proc.terminate()
	#---------------------------------------------------------------------------
	src = os.path.abspath(r'dist\scripts')
	dst = os.path.abspath(r'dist\pyrenamer\scripts')
	shutil.copytree(src, dst)
	#---------------------------------------------------------------------------
	issc = r'''"C:\Program Files (x86)\Inno Setup 5\ISCC.exe"'''
	command = '''%s "pyrenamer.iss"''' % (issc)
	proc = subprocess.Popen(command, shell=True)
	resp = proc.communicate()[0]; proc.terminate()
#-------------------------------------------------------------------------------
if __name__ == '__main__':
	main()
#-------------------------------------------------------------------------------
# end of Main Entry
################################################################################
