import io

from setuptools import setup, find_packages

version = '0.1.2'
requirements = [
    'requests==2.21.0',
]

tests_requirements = [
    'flake==3.7.7',
    'pytest==4.4.1',
    'tox==3.9.0',
    'Sphix==2.0.1',
    'setuptools==41.0.0',
    'twice==1.13.0'
]

with io.open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='npyi',
    packages=find_packages(exclude=['test', 'test.*']),
    version=version,
    long_description=readme,
    description='API wrapper around the NPPES API',
    author='Andy Huynh',
    license='BSD',
    author_email='andy.huynh312@gmail.com',
    url='https://github.com/andyh1203/npyi',
    keywords=['npyi', 'npi', 'nppes'],
    install_requires=requirements,
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
    tests_require=tests_requirements
)
