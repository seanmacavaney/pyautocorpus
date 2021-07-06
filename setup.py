from glob import glob
import os
import sys
from glob import glob
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

windows = sys.platform.startswith("win")

include_dirs = [
    os.path.realpath(os.path.join(__file__, '..', 'AutoCorpus', 'src', 'common')),
    os.path.realpath(os.path.join(__file__, '..', 'AutoCorpus', 'src', 'wikipedia')),
]
lib_dirs = []
libs = ['pcre']
comp = []

if windows:
    PCRE_HOME = os.environ.get("PCRE_HOME", os.path.realpath(os.path.join(__file__, '..', 'pcre')))
    print('PCRE_HOME', PCRE_HOME)
    include_dirs.append(PCRE_HOME)
    lib_dirs.append(PCRE_HOME)
    comp.append('-D_POSIX_C_SOURCE=199309L')
else:
    comp.append('-std=c++11')

setuptools.setup(
    name="pyautocorpus",
    version="0.0.1",
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
    python_requires='>=3.6',
    ext_modules=[setuptools.Extension("pyautocorpus", [
        "src/pyautocorpus.cpp",
        "AutoCorpus/src/common/utilities.cpp",
        "AutoCorpus/src/wikipedia/Textifier.cpp",
    ], include_dirs=include_dirs, libraries=libs, extra_compile_args=comp)],
)
