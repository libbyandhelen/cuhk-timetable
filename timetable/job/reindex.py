import datetime
import subprocess

import os

import time

PROJECT_PATH = '/Users/yingbozhang/Desktop/myproj/timetable2/timetable'
PYTHON_PATH = '/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6'


def run():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(st)
    print('reindexing ...')
    os.chdir(PROJECT_PATH)
    subprocess.call([PYTHON_PATH, 'manage.py', 'update_index'], shell=True)
