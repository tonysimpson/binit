from setuptools import find_packages, setup, Extension

setup(
    name='binit',
    packages=find_packages(),
    version='0.0.1',
#    ext_modules=[Extension('_binit', sources=['_binit.c'])],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
    
