from setuptools import setup, find_packages

setup(
    name="course_spider",
    packages=find_packages(),
    version='0.0.1',
    description="course spider",
    author="libbyandhelen",
    author_email='libbyandhelen@163.com',
    classifiers=[],
    entry_points={
        'console_scripts': [
            'crawl-course = spider.run:crawl',
        ]
    },
    install_requires=[
        'scrapy',
    ]
)