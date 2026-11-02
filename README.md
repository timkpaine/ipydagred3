# ipydagred3

Draw and update graphs in Jupyter with [Spaday](https://github.com/1kbgz/spaday)'s AnyWidget runtime
and [spaday-dagre](https://github.com/1kbgz/spaday-dagre).

[![Build Status](https://github.com/timkpaine/ipydagred3/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/timkpaine/ipydagred3/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/timkpaine/ipydagred3/branch/main/graph/badge.svg?token=3N6NOPL4RE)](https://codecov.io/gh/timkpaine/ipydagred3)
[![PyPI](https://img.shields.io/pypi/l/ipydagred3.svg)](https://pypi.python.org/pypi/ipydagred3)
[![PyPI](https://img.shields.io/pypi/v/ipydagred3.svg)](https://pypi.python.org/pypi/ipydagred3)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/timkpaine/ipydagred3/main?urlpath=lab)

## Installation

Install with Python 3.11 or later:

```bash
pip install ipydagred3
```

AnyWidget supplies the Jupyter integration. There is no labextension or nbextension to install.

## Usage

Create a graph and display its widget in a notebook cell:

```python
from ipydagred3 import DagreD3Widget, Graph

graph = Graph(attrs={"rankdir": "LR", "height": 400})
graph.setNode("start", label="Start", shape="circle", tooltip="Start here")
graph.setNode("finish", label="Finish", shape="diamond")
graph.setEdge("start", "finish", label="Next", tooltip="Continue")
widget = DagreD3Widget(graph)
widget
```

Edit existing objects or add graph elements from another cell to update the displayed graph:

```python
graph.setNode("start", style="fill: #7f7; stroke: #333")
graph.setNode("review", tooltip="Review the result")
graph.setEdge("finish", "review", label="Review")
```

Register a callback to inspect clicked nodes and edges:

```python
from IPython.display import display
from ipywidgets import Output

output = Output()


def clicked(widget, value):
    with output:
        print(value)  # node id, or [source, target] for an edge


widget.on_click(clicked)
display(output)
```

The widget supports zoom and pan, rectangular, circular, elliptical, and diamond nodes, custom
tooltips, and node/edge CSS. See [compatibility reference](docs/compatibility.md) for the supported
attributes and differences from dagre-d3.

## Examples

- [Network example](docs/examples/example.ipynb)
- [Tooltips and click events](docs/examples/tooltip.ipynb)
