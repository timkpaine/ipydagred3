from setuptools import setup, find_packages
from codecs import open
from os import path

from jupyter_packaging import (
    create_cmdclass, install_npm, ensure_targets,
    combine_commands, ensure_python, get_version
)

ensure_python(('2.7', '>=3.7'))
pjoin = path.join
name = 'ipydagred3'
here = path.abspath(path.dirname(__file__))
version = get_version(pjoin(here, name, '_version.py'))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

requires = [
    "ipywidgets>=7.5.1"
]


data_spec = [
    # Lab extension installed by default:
    ('share/jupyter/lab/extensions',
     'lab-dist',
     'ipydagred3-*.tgz'),
    # Config to enable server extension by default:
    ('etc/jupyter',
     'jupyter-config',
     '**/*.json'),
]


cmdclass = create_cmdclass('js', data_files_spec=data_spec)
cmdclass['js'] = combine_commands(
    install_npm(here, build_cmd='build:all'),
    ensure_targets([
        pjoin(here, 'lib', 'index.js'),
        pjoin(here, 'css', 'widget.css')
    ]),
)


setup(
    name=name,
    version=version,
    description='ipywidgets wrapper around dagre-d3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/timkpaine/ipydagred3',
    author='Tim Paine',
    author_email='t.paine154@gmail.com',
    license='Apache 2.0',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Jupyter',
    ],

    cmdclass=cmdclass,
    keywords='jupyter jupyterlab',
    packages=find_packages(exclude=['tests', ]),
    install_requires=requires,
    extras_require={
        'dev': requires + ['pytest', 'pytest-cov', 'pylint', 'flake8', 'bump2version', 'autopep8', 'mock']
    },
    include_package_data=True,
    data_files=[
        ('share/jupyter/nbextensions/ipydagred3', [
            'ipydagred3/nbextension/static/extension.js',
            'ipydagred3/nbextension/static/index.js',
            'ipydagred3/nbextension/static/index.js.map',
        ]),
        ('etc/jupyter/nbconfig/notebook.d', ['ipydagred3.json'])
    ],
    zip_safe=False,

)
