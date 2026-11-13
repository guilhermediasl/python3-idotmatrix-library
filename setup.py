import re
from pathlib import Path

from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")
# Read the version without importing the package: importing it would pull in
# bleak/pillow, which are not installed yet in pip's isolated build env.
__version__ = re.search(
    r'__version__\s*=\s*"([^"]+)"',
    (this_directory / "idotmatrix" / "version.py").read_text(encoding="utf-8"),
).group(1)

setup(
    name="idotmatrix",
    version=__version__,
    description="configure any iDotMatrix compatible 16x16 or 32x32 pixel display without the chinese iDotMatrix android / iOS app.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/guilhermediasl/python3-idotmatrix-library",
    author="Kalle Minkner",
    author_email="info@kalleminkner.de",
    maintainer="Guilherme Dias de Andrade Lima",
    license="GPLv3",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.8",
    install_requires=[
        "bleak>=0.22",
        "pillow",
        "cryptography",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
    ],
)
