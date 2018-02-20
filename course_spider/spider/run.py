import subprocess

import os
from spider.course.settings import PROJECT_PATH
PYTHON_PATH = '/Library/Frameworks/Python.framework/Versions/3.6/bin/python3.6'
SCRAPY_PATH = '/Library/Frameworks/Python.framework/Versions/3.5/bin/scrapy'


def crawl():
    os.chdir(PROJECT_PATH)
    for i in range(26):
        print('crawling %s ...' % str(i))
        subprocess.Popen([SCRAPY_PATH, 'crawl', '-a', 'alphanums=' + str(i), 'course'])
