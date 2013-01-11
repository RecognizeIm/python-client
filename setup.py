from setuptools import setup

setup(
    name='Recognize.im',
    version='0.1',
    author='Michal Czyzycki',
    packages=['recognizeim'],
	install_requires=['SOAPpy', 'ClientCookie'],
    description='Recognize.im Api.',
    long_description=open('README.md').read(),
)