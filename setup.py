from glob import glob
import os
import sys
from glob import glob
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

windows = sys.platform.startswith("win")


sources = []
include_dirs = [
    os.path.realpath(os.path.join(__file__, '..', 'AutoCorpus', 'src', 'common')),
    os.path.realpath(os.path.join(__file__, '..', 'AutoCorpus', 'src', 'wikipedia')),
]
lib_dirs = []
libs = []
comp = []
# Build against the stable ABI (abi3) so one wheel covers CPython >= 3.7.
# Keep LIMITED_API_HEX and LIMITED_API_TAG in sync.
LIMITED_API_HEX = '0x03070000'
LIMITED_API_TAG = 'cp37'
macros = [('PCRE_STATIC', None), ('Py_LIMITED_API', LIMITED_API_HEX)]

if windows:
    # currently not supporting Windows
    sources = [
        'src/pyautocorpus_win_placeholder.cpp'
    ]
else:
    libs.append('pcre')
    comp += ['-std=c++11', '-I/opt/homebrew/include']
    sources = [
        "src/pyautocorpus.cpp",
        "src/utilities.cpp", # custom version of AutoCorpus/src/common/utilities.cpp because of the Windows build
        "src/Textifier.cpp", # custom version of AutoCorpus/src/wikipedia/Textifier.cpp because of the Windows build
    ]

setuptools.setup(
    name="pyautocorpus",
    version="0.1.19",
    author="Sean MacAvaney",
    author_email="sean.macavaney@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seanmacavaney/pyautocorpus",
    include_package_data = True,
    packages=setuptools.find_packages(include=['pyautocorpus']),
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
    ext_modules=[setuptools.Extension("pyautocorpus", sources, include_dirs=include_dirs, libraries=libs, library_dirs=lib_dirs, define_macros=macros, extra_compile_args=comp, py_limited_api=True)],
    options={'bdist_wheel': {'py_limited_api': LIMITED_API_TAG}},
)
