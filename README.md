# ipydagred3

Draw and update graphs in Jupyter with [Spaday](https://github.com/1kbgz/spaday)'s AnyWidget runtime
and [spaday-dagre](https://github.com/1kbgz/spaday-dagre).

[![Build Status](https://github.com/timkpaine/ipydagred3/workflows/Build%20Status/badge.svg?branch=main)](https://github.com/timkpaine/ipydagred3/actions?query=workflow%3A%22Build+Status%22)
[![codecov](https://codecov.io/gh/timkpaine/ipydagred3/branch/main/graph/badge.svg?token=3N6NOPL4RE)](https://codecov.io/gh/timkpaine/ipydagred3)
[![PyPI](https://img.shields.io/pypi/l/ipydagred3.svg)](https://pypi.python.org/pypi/ipydagred3)
[![PyPI](https://img.shields.io/pypi/v/ipydagred3.svg)](https://pypi.python.org/pypi/ipydagred3)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/timkpaine/ipydagred3/main?urlpath=lab)

## Try in your browser

Open the [example notebooks](https://timkpaine.github.io/ipydagred3/lite/lab/index.html)
in JupyterLite and run all cells. The first cell installs `ipydagred3` from the site's build.
Pyodide runs Python and widget callbacks in your browser. The first load downloads the Python runtime
and dependencies.

To build and serve the site locally:

```bash
uv pip install -e '.[develop,lite]'
make jupyterlite
python -m http.server 8000 --directory dist
```

Open `http://localhost:8000/lite/lab/index.html`. To check both notebooks in Chromium, install
Node.js and pnpm, then run `make test-jupyterlite`.

The build copies `docs/examples/*.ipynb` into the site, adds the install cell, and clears saved
outputs and widget state.

Configure GitHub Pages to serve the root of `gh-pages`. The publishing workflow updates that
branch after a successful `main` build.

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

Update the displayed graph from another cell:

```python
graph.setNode("start", style="fill: #7f7; stroke: #333")
graph.setNode("review", tooltip="Review the result")
graph.setEdge("finish", "review", label="Review")
```

Handle node and edge clicks:

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

Nodes can be rectangles, circles, ellipses, or diamonds. The graph supports pan, zoom, custom
tooltips, and CSS for nodes and edges. See the [compatibility reference](docs/compatibility.md) for supported
attributes and differences from dagre-d3.

## Examples

- [Network example](docs/examples/example.ipynb)
- [Tooltips and click events](docs/examples/tooltip.ipynb)

> [!NOTE]
> Project scaffolding is maintained with [Copier](https://copier.readthedocs.io/en/stable/)
> and the [Base Python Project Template](https://github.com/python-project-templates/base).
