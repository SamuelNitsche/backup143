from sys import platform as _platform
import sys
import os
import ctypes
import time
import __main__
import threading

from bin.both.dbcon import dbmanager

db = dbmanager()
db.create()

from bin.both.log import LogginSystem

log = LogginSystem('service')
log.write('Detected Python version: ' + sys.version)

try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

if is_admin == False:
    print("[WARNING] You don't have Admin privileges! This may cause some Permission Error's while running a Backup!")
    
threads = []

if _platform == "win32" or _platform == "win64":
    log = LogginSystem('service')
    log.write('Detected OS: Windows')
    try:
        from bin.both.process import process

        p = process()
        t = threading.Thread(target=p.start)
        threads.append(t)
        t.start()
    except ImportError as e:
        log = LogginSystem('service')
        log.write(str(e))
elif _platform == "linux" or _platform == "linux2" or _platform == "darwin":
    log = LogginSystem('service')
    log.write('Detected OS: Linux')
    try:
        from bin.both.process import process

        p = process()
        t = threading.Thread(target=p.start)
        threads.append(t)
        t.start()
    except ImportError as e:
        print("[ERROR] Linux Service Failed: " + str(e))
        log = LogginSystem('service')
        log.write("Linux Service Failed: " + str(e))
else:
    print("Your OS isn't supported!")
