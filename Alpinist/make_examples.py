import glob
import os

make_scripts = glob.glob('examples/**/make_keyboard.py')

for s in make_scripts:
    print(s)
    os.system('python %s'%s)