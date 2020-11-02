import os
import re
import setuptools

VERSIONFILE = "./jovian/_version.py"
FLAVORFILE = "./jovian/_flavor.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
pkg_name = os.getenv("PKG_NAME", "jovian")

if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

with open(FLAVORFILE, "w") as f:
    f.write("__flavor__ = \"{}\"".format(pkg_name))


with open("README.md", "rb") as fh:
    long_description = fh.read().decode('utf-8', errors='ignore')

setuptools.setup(
    name=pkg_name,
    version=verstr,
    author="Jovian",
    author_email="hello@jovian.ai",
    entry_points={
        'console_scripts': ['jovian=jovian.__main__:main'],
    },
    description="Jovian Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://jovian.ai/?utm_source=pypi",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={"jovian": ['jovian_nb_ext/*']},
    data_files=[("share/jupyter/nbextensions/jovian_nb_ext", ["jovian/jovian_nb_ext/main.js"]),
                ("etc/jupyter/nbconfig/notebook.d", ["jovian/jovian_nb_ext/jovian_nb_ext.json"])],
    include_package_data=True,
    install_requires=['requests', 'uuid', 'pyyaml', 'click']
)
