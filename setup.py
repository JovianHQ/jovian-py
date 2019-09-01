import os
import re
import setuptools

VERSIONFILE = "./jovian/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
pkg_name = os.getenv("PKG_NAME")

if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

if pkg_name is None:
    raise RuntimeError("Please provide valid package name")

with open("README.md", "rb") as fh:
    long_description = fh.read().decode('utf-8', errors='ignore')

setuptools.setup(
    name=pkg_name,
    version=verstr,
    author="SwiftAce",
    author_email="opensource@swiftace.ai",
    entry_points={
        'console_scripts': ['jovian=jovian.cli:main'],
    },
    description="Jovian Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://swiftace.ai/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={"jovian": ['jovian_nb_ext/*']},
    data_files=[("share/jupyter/nbextensions/jovian_nb_ext", ["jovian/jovian_nb_ext/main.js"]),
                ("etc/jupyter/nbconfig/notebook.d", ["jovian/jovian_nb_ext/jovian_nb_ext.json"])],
    include_package_data=True,
    install_requires=['requests', 'uuid', 'pyyaml']
)
