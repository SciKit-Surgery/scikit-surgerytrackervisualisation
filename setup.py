# coding=utf-8
"""
Setup for scikit-surgerytrackervisualisation
"""

from setuptools import setup, find_packages
import versioneer

# Get the long description
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='scikit-surgerytrackervisualisation',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Provides a live visualisation of tracking data from a scikit-surgerytracker source',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/SciKit-Surgery/scikit-surgerytrackervisualisation',
    author='Stephen Thompson',
    author_email='s.thompson@ucl.ac.uk',
    license='BSD-3 license',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',


        'License :: OSI Approved :: BSD License',


        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',

        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
    ],

    keywords='medical imaging',

    packages=find_packages(
        exclude=[
            'doc',
            'tests',
        ]
    ),

    install_requires=[
        'numpy',
        'vtk',
        'PySide2',
        'scikit-surgeryvtk>=0.9.0',
        'scikit-surgeryimage>=0.6.0',
        'scikit-surgerycore',
        'scikit-surgeryutils',
        'scikit-surgerynditracker',
        'scikit-surgeryarucotracker',
    ],

    entry_points={
        'console_scripts': [
            'sksurgerytrackervisualisation=sksurgerytrackervisualisation.__main__:main',
        ],
    },
)
