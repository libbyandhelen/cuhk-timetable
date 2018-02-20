import subprocess
import datetime
import time

import os
from spider.course.settings import PROJECT_PATH
PYTHON_PATH = '/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6'
SCRAPY_PATH = '/Library/Frameworks/Python.framework/Versions/3.5/bin/scrapy'


def crawl():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print(st)

    os.chdir(PROJECT_PATH)
    for i in range(26):
        print('crawling %s ...' % str(i))
        subprocess.Popen([SCRAPY_PATH, 'crawl', '-a', 'alphanums=' + str(i), 'course'])
