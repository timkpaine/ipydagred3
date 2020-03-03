
# ipydagred3

ipywidgets wrapper around [dagre-d3](https://github.com/dagrejs/dagre-d3)

[![Build Status](https://dev.azure.com/tpaine154/jupyter/_apis/build/status/timkpaine.ipydagred3?branchName=master)](https://dev.azure.com/tpaine154/jupyter/_build/latest?definitionId=22&branchName=master)
[![Coverage](https://img.shields.io/azure-devops/coverage/tpaine154/jupyter/22)](https://dev.azure.com/tpaine154/jupyter/_build?definitionId=22&_a=summary)
[![PyPI](https://img.shields.io/pypi/l/ipydagred3.svg)](https://pypi.python.org/pypi/ipydagred3)
[![PyPI](https://img.shields.io/pypi/v/ipydagred3.svg)](https://pypi.python.org/pypi/ipydagred3)
[![npm](https://img.shields.io/npm/v/ipydagred3.svg)](https://www.npmjs.com/package/ipydagred3)


![](https://raw.githubusercontent.com/timkpaine/ipydagred3/master/docs/img/example.gif)

## Installation

You can install using `pip`:

```bash
pip install ipydagred3
```

Or if you use jupyterlab:

```bash
pip install ipydagred3
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] ipydagred3
```

## Features
- Dynamically create and modify graphs from python
- Change color, shape, tooltip, etc
- Click events (click on node or edge and get event in ipywidget indicating source, good for node inspector tools)


### Tooltips and Click events
![](https://raw.githubusercontent.com/timkpaine/ipydagred3/master/docs/img/example2.gif)
