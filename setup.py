import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = "1.0dev1"


setup(
    name='diffeo',
    author="Andrea Censi",
    author_email="andrea@cds.caltech.edu",
    url='http://andreacensi.github.io/diffeo/',
    version=version,
    description="Library for representing and learning diffeomorphisms",
    long_description=read('README.md'),
    keywords="",
    license="LGPL",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU Library or '
        'Lesser General Public License (LGPL)',
    ],

    package_dir={'':'src'},
    packages=find_packages('src'),
    entry_points={
     'console_scripts': [
       'diffeo = diffeo:diffeo_main',
      ]
    },
      
    install_requires=[
        'PyContracts',
        'PyGeometry',
        'compmake',
        'reprep',
        'QuickApp'
    ],

    tests_require=['nose']
)

