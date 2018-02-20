import datetime
import subprocess

import time


def run():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(st)
    subprocess.call('/Library/Frameworks/Python.framework/Versions/3.6/bin/crawl-course', shell=True)
