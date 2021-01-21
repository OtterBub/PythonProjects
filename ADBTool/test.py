import copy
import os
import re
import subprocess
import sys
import threading
import tkinter
from multiprocessing import Process, Queue
from time import sleep
from tkinter import filedialog
from typing import Any, Callable, List, Mapping, Optional, Tuple
import glob

import traceback

from custom import quickEditMode

# print(os.path.isfile(os.path.curdir + "/nox.txt"))
# print(os.path.dirname(sys.argv[0]))

# if os.path.isfile(os.path.dirname(sys.argv[0]) + "/nox.txt"):
#     print("Active nox_adb")
#     sleep(1)
#     ADB = "nox_adb"
# try:
#     subprocess.run("dir > test.txt")
# except subprocess.CalledProcessError:
#     print("sub Process Error")
# except:
#     traceback.print_exc()
#     print("sub Error")

# try:
#     if os.system("Hello") != 0:
#         raise Exception("cmd error")
# except:
#     print("Error")


# cmd = [
#     "nox_adb devices",
#     'nox_adb install -r -d "C:\\Users\\User\\Desktop\\Python\\1. Project\\Appium\\Test\\ApiDemos-debug.apk"'
# ]

# # subprocess.run(c, shell=True, check=True)

# for c in cmd:
#     result = subprocess.run(c, shell=True, text=True)
#     print(result.returncode)

pattern = os.path.dirname(sys.argv[0]) + r"\ADB*.py"
for r in glob.glob(pattern):
    print(r)
    # os.path.curdir