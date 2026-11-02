"""The legacy graph API hosted by Spaday's AnyWidget runtime."""

import base64
from pathlib import Path

import spaday.widget as spaday_widget
from ipywidgets import CallbackDispatcher
from spaday import SendPatch, Widget, event_value
from spaday_dagre import Dagre, package
from traitlets import Instance, observe

from .graph import Graph


def _module(source):
    encoded = base64.b64encode(source.encode()).decode()
    return f'await loadModule("{encoded}")'


def _widget_esm():
    dagre = (package.assets_dir / "cdn" / "index.js").read_text(encoding="utf-8")
    runtime = (Path(spaday_widget.__file__).parent / "extension" / "cdn" / "widget.js").read_text(encoding="utf-8")
    return (
        """
async function loadModule(encoded) {
    const url = URL.createObjectURL(new Blob([Uint8Array.from(atob(encoded), c => c.charCodeAt(0))], {type: "text/javascript"}));
    try { return await import(url); } finally { URL.revokeObjectURL(url); }
}
"""
        + f"{_module(dagre)};\nconst {{default: runtime}} = {_module(runtime)};\n"
        + """
export default {
    ...runtime,
    async render(args) {
        const dispose = await runtime.render(args);
        const decorate = () => {
            const host = args.el.querySelector("spaday-dagre");
            if (!host) return;
            const graph = host.graph;
            let relayout = false;
            for (const group of host.querySelectorAll("[data-node-id], [data-edge-source]")) {
                const id = group.getAttribute("data-node-id");
                const config = id !== null
                    ? graph.nodes.find(node => node.id === id)
                    : graph.edges.find(edge => edge.source === group.getAttribute("data-edge-source") && edge.target === group.getAttribute("data-edge-target"));
                if (!config) continue;
                let title = group.querySelector("title");
                if (!title) {
                    title = document.createElementNS("http://www.w3.org/2000/svg", "title");
                    group.prepend(title);
                }
                if (title.textContent !== config.tooltip) title.textContent = config.tooltip;
                const shape = group.querySelector(id !== null ? "rect, ellipse, polygon" : ".spaday-dagre-edge-line");
                if (shape) shape.setAttribute("style", config.style || "");
                let label = group.querySelector("text");
                if (id === null && config.label && !label) {
                    label = document.createElementNS("http://www.w3.org/2000/svg", "text");
                    label.setAttribute("class", "spaday-dagre-edge-label");
                    label.setAttribute("text-anchor", "middle");
                    label.setAttribute("dominant-baseline", "middle");
                    group.append(label);
                    relayout = true;
                }
                if (label) label.setAttribute("style", config.labelStyle || "");
                if (id === null && shape) shape.setAttribute("marker-end", graph.directed ? "url(#spaday-dagre-arrow)" : "none");
            }
            if (relayout) host.graph = {...graph};
        };
        const observer = new MutationObserver(decorate);
        observer.observe(args.el, {childList: true, subtree: true});
        args.model.on("change:_tree", decorate);
        decorate();
        return () => {
            observer.disconnect();
            args.model.off("change:_tree", decorate);
            dispose();
        };
    }
};
"""
    )


def _graph_config(graph):
    nodes = []
    for node in graph.nodes:
        config = {"id": node.name, "label": node.label, "shape": node.shape, "tooltip": node.tooltip, **node.attrs}
        if node.shape == "circle":
            config["shape"] = "ellipse"
            diameter = max(node.attrs.get("width", 0), node.attrs.get("height", 0), len(node.label) * 7 + 32, 60)
            config["width"] = config["height"] = diameter
        nodes.append(config)
    edges = {}
    for edge in graph.edges:
        key = (edge.v.name, edge.w.name)
        if graph.multigraph and key in edges:
            raise ValueError("spaday-dagre does not support parallel edges between the same nodes")
        edges[key] = {"source": edge.v.name, "target": edge.w.name, "label": edge.label, "tooltip": edge.tooltip, **edge.attrs}
    return {"nodes": nodes, "edges": list(edges.values()), "directed": graph.directed}


class DagreD3Widget(Widget):
    """Render a :class:`Graph` using ``spaday-dagre`` in an AnyWidget host."""

    _esm = _widget_esm()
    _css = (package.assets_dir / "css" / "index.css").read_text(encoding="utf-8")

    graph = Instance(Graph)

    def __init__(self, graph=None, *args, **kwargs):
        graph = graph if isinstance(graph, Graph) else Graph(*args, **kwargs)
        self._click_handlers = CallbackDispatcher()
        super().__init__(self._component(graph))
        self.on_intent(self._handle_click)
        self.graph = graph

    @staticmethod
    def _component(graph):
        def dimension(name, default):
            value = graph.attrs.get(name, default)
            return f"{value}px" if isinstance(value, (int, float)) else value

        layout = {"nodesep": 70, "ranksep": 50, "rankdir": "TB", "marginx": 20, "marginy": 20}
        layout.update({key: value for key, value in graph.attrs.items() if key not in {"height", "width"}})
        return (
            Dagre(
                graph=_graph_config(graph),
                layout=layout,
                style=f"height: {dimension('height', 400)}; width: {dimension('width', '100%')}",
            )
            .on("dagre-node-click", SendPatch("ipydagred3", "node-click", event_value("id")))
            .on("dagre-edge-click", SendPatch("ipydagred3", "edge-click", event_value()))
        )

    def on_click(self, callback, remove=False):
        self._click_handlers.register_callback(callback, remove=remove)

    def click(self, value):
        self._click_handlers(self, value)

    def _handle_click(self, content):
        detail = content.get("detail", {})
        if detail.get("model") != "ipydagred3":
            return
        if detail.get("field") == "node-click":
            self.click(detail["value"])
        elif detail.get("field") == "edge-click":
            value = detail["value"]
            self.click([value["source"], value["target"]])

    def addGraph(self, *args, **kwargs):
        self.graph.addGraph(*args, **kwargs)

    def setGraph(self, *args, **kwargs):
        self.graph.setGraph(*args, **kwargs)

    def addNode(self, *args, **kwargs):
        self.graph.addNode(*args, **kwargs)

    def setNode(self, *args, **kwargs):
        self.graph.setNode(*args, **kwargs)

    def addEdge(self, *args, **kwargs):
        self.graph.addEdge(*args, **kwargs)

    def setEdge(self, *args, **kwargs):
        self.graph.setEdge(*args, **kwargs)

    def post(self, msg):
        self.update(self._component(self.graph))

    @observe("graph")
    def _observe_graph(self, change):
        old = change["old"]
        if isinstance(old, Graph):
            old._setWidget(None)
        change["new"]._setWidget(self)
        self.post(None)
