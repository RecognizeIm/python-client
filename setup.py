from setuptools import setup

setup(
    name='Recognize.im',
    version='0.1',
    author='Michal Czyzycki',
    packages=['recognizeim', 'SOAPpy','SOAPpy/wstools'],
    install_requires=['ClientCookie', 'fpconst'],
    description='Recognize.im Api.',
    long_description=open('README.md').read(),
)