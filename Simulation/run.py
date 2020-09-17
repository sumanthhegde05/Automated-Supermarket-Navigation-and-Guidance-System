import os
from time import sleep

os.system('cmd /c "py admin.py"')
sleep(2)
os.system('cmd /c "py reference.py"')