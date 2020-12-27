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

import traceback

from custom import quickEditMode

print(os.path.isfile(os.path.curdir + "/nox.txt"))
print(os.path.dirname(sys.argv[0]))

if os.path.isfile(os.path.dirname(sys.argv[0]) + "/nox.txt"):
    print("Active nox_adb")
    sleep(1)
    ADB = "nox_adb"