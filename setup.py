import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-ga-puller',
    version='0.1.1',
    packages=['ga_puller', 'ga_puller.management', 'ga_puller.management.commands'],
    include_package_data=True,
    license='MIT License',
    description='Django app used to pull daily Google Analytics data into your django database.',
    long_description=README,
    url='https://github.com/CIGIHub/django-ga-puller/',
    author='Caroline Simpson',
    author_email='csimpson@cigionline.org',
    install_requires=[
        'google-api-python-client >= 1.2',
        'pycrypto >= 2.6.1',
    ],
    setup_requires=[
        'google-api-python-client >= 1.2',
        'pycrypto >= 2.6.1',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)