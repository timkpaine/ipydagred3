
# ipydagred3

ipywidgets library for drawing directed acyclic graphs in jupyterlab using [dagre-d3](https://github.com/tbo47/dagre-es)

[![Build Status](https://github.com/timkpaine/ipydagred3/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/timkpaine/ipydagred3/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/timkpaine/ipydagred3/branch/main/graph/badge.svg?token=3N6NOPL4RE)](https://codecov.io/gh/timkpaine/ipydagred3)
[![PyPI](https://img.shields.io/pypi/l/ipydagred3.svg)](https://pypi.python.org/pypi/ipydagred3)
[![PyPI](https://img.shields.io/pypi/v/ipydagred3.svg)](https://pypi.python.org/pypi/ipydagred3)
[![npm](https://img.shields.io/npm/v/ipydagred3.svg)](https://www.npmjs.com/package/ipydagred3)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/timkpaine/ipydagred3/main?urlpath=lab)


![](https://raw.githubusercontent.com/timkpaine/ipydagred3/main/docs/img/example.gif)

## Installation

You can install using `pip`:

```bash
pip install ipydagred3
```

## Features

- Dynamically create and modify graphs from python
- Change color, shape, tooltip, etc
- Click events (click on node or edge and get event in ipywidget indicating source, good for node inspector tools)


### Tooltips and Click events

![](https://raw.githubusercontent.com/timkpaine/ipydagred3/main/docs/img/example2.gif)

## Examples

Network example from the first gif
[Network Example](https://github.com/timkpaine/ipydagred3/tree/main/docs/examples/example.ipynb)

Tooltip Example from the second gif
[Tooltip Example](https://github.com/timkpaine/ipydagred3/tree/main/docs/examples/example.ipynb)
