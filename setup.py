# *****************************************************************************
#
# Copyright (c) 2020, the ipydagred3 authors.
#
# This file is part of the ipydagred3 library, distributed under the terms of
# the Apache License 2.0.  The full license can be found in the LICENSE file.
#
from codecs import open
from os import path

from jupyter_packaging import get_data_files, npm_builder, wrap_installers
from setuptools import find_packages, setup

pjoin = path.join
name = "ipydagred3"
here = path.abspath(path.dirname(__file__))
jshere = path.abspath(pjoin(path.dirname(__file__), "js"))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read().replace("\r\n", "\n")

requires = [
    "ipywidgets>=7.5.1",
]

requires_test = [
    "pytest>=4.3.0",
    "pytest-cov>=2.6.1",
]

requires_dev = (
    requires
    + requires_test
    + [
        "black>=20.8b1",
        "bump2version>=1.0.0",
        "check-manifest",
        "flake8>=3.7.8",
        "flake8-black>=0.2.1",
        "jupyter_packaging",
        "Sphinx>=1.8.4",
        "sphinx-markdown-builder>=0.5.2",
    ]
)

ext_path = pjoin(name, "extension")
nb_path = pjoin(name, "nbextension", "static")
lab_path = pjoin(name, "labextension")

# Representative files that should exist after a successful build
jstargets = [
    pjoin(jshere, "lib", "index.js"),
]

data_spec = [
    # Lab extension installed by default:
    ("share/jupyter/nbextensions/ipydagred3", nb_path, "**"),
    ("etc/jupyter/nbconfig/notebook.d", ext_path, "ipydagred3.json"),
    (
        "share/jupyter/labextensions/ipydagred3",
        lab_path,
        "**",
    ),
    # Config to enable server extension by default:
    ("etc/jupyter/jupyter_server_config.d", ext_path, "*.json"),
]

ensured_targets = [
    pjoin(lab_path, "package.json"),
    pjoin(lab_path, "static", "style.js"),
    pjoin(nb_path, "index.js"),
]

builder = npm_builder(
    build_cmd="build", path=jshere, source_dir=pjoin(jshere, "src"), build_dir=lab_path
)

setup(
    name=name,
    version="0.3.5",
    description="ipywidgets wrapper around dagre-d3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timkpaine/ipydagred3",
    author="Tim Paine",
    author_email="t.paine154@gmail.com",
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Jupyter",
        "Framework :: Jupyter :: JupyterLab",
    ],
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "Jupyterlab", "Widgets", "IPython", "Graph", "Data", "DAG"],
    cmdclass=wrap_installers(
        post_develop=builder, pre_dist=builder, ensured_targets=ensured_targets
    ),
    data_files=get_data_files(data_spec),
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=requires,
    test_suite="ipydagred3.tests",
    tests_require=requires_test,
    extras_require={
        "dev": requires_dev,
        "develop": requires_dev,
    },
    python_requires=">=3.7",
)
