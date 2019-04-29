import os

from setuptools import setup, find_packages

version = '0.1.0'
requirements = [
    'requests>=2.21.0',
]

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='npyi',
    packages=find_packages(exclude=['test', 'test.*']),
    version=version,
    description='API wrapper around the NPPES API',
    author='Andy Huynh',
    license='BSD',
    author_email='andy.huynh312@gmail.com',
    url='https://github.com/andyh1203/npyi',
    keywords=['npyi', 'npi', 'nppes'],
    install_requests=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ],
)
