from glob import glob
import os
import sys
from glob import glob
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

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
    packages=setuptools.find_packages(include=['zlib_state']),
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
    ext_modules=[setuptools.Extension("pyautocorpus", [
            "src/pyautocorpus.cpp",
            "AutoCorpus/src/common/utilities.cpp",
            "AutoCorpus/src/wikipedia/Textifier.cpp",
        ], include_dirs=[
        os.path.realpath(os.path.join(__file__, '..', 'AutoCorpus', 'src', 'common')),
        os.path.realpath(os.path.join(__file__, '..', 'AutoCorpus', 'src', 'wikipedia')),
    ], libraries=['pcre'], extra_compile_args=['-std=c++11'])],
)
