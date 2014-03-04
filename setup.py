from setuptools import setup

setup(
    name='pyzendesk',
    version='0.0.1',
    packages=['pyzendesk, tests'],
    install_requires=[
        'simplejson >= 3.3.3',
        'requests >= 2.2.1',
        'setuptools >= 2.2',
    ],
    url='',
    license='MIT',
    author='bevans',
    author_email='ben@kevans.org',
    description='Python wrapper for Zendesk API'
)
