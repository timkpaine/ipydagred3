import pytest
from spaday import Widget

from ipydagred3 import DagreD3Widget, Edge, Graph, Node


def _value(value):
    if "Map" in value:
        return {key: _value(item) for key, item in value["Map"].items()}
    if "List" in value:
        return [_value(item) for item in value["List"]]
    return next(iter(value.values()))


def _config(widget):
    return _value(widget._tree["props"]["graph"])


def test_graph_renders_as_a_spaday_anywidget():
    graph = Graph(attrs={"rankdir": "LR", "height": 300, "width": "80%"})
    graph.setNode("a", label="Start", shape="diamond", tooltip="Enter", style="fill: red")
    graph.setEdge("a", "b", label="Next", tooltip="Continue", style="stroke: blue")
    widget = DagreD3Widget(graph)

    assert isinstance(widget, Widget)
    assert widget._tree["tag"] == "spaday-dagre"
    config = _config(widget)
    assert config["nodes"][0] == {"id": "a", "label": "Start", "shape": "diamond", "tooltip": "Enter", "style": "fill: red"}
    assert config["edges"][0] == {"source": "a", "target": "b", "label": "Next", "tooltip": "Continue", "style": "stroke: blue"}
    assert _value(widget._tree["props"]["layout"])["rankdir"] == "LR"
    assert _value(widget._tree["props"]["style"]) == "height: 300px; width: 80%"


def test_existing_graph_objects_update_the_rendered_tree():
    graph = Graph()
    node = graph.setNode("a")
    edge = graph.setEdge("a", "b")
    widget = DagreD3Widget(graph)

    node.label = "Changed"
    node.shape = "circle"
    node.tooltip = "Updated tooltip"
    node.attrs = {"style": "fill: green"}
    edge.label = "Updated edge"
    edge.tooltip = "Updated edge tooltip"
    edge.attrs = {"style": "stroke: red"}

    config = _config(widget)
    assert config["nodes"][0]["label"] == "Changed"
    assert config["nodes"][0]["tooltip"] == "Updated tooltip"
    assert config["nodes"][0]["style"] == "fill: green"
    assert config["nodes"][0]["shape"] == "ellipse"
    assert config["nodes"][0]["width"] == config["nodes"][0]["height"]
    assert config["edges"][0]["label"] == "Updated edge"
    assert config["edges"][0]["tooltip"] == "Updated edge tooltip"
    assert config["edges"][0]["style"] == "stroke: red"


def test_graph_replacement_detaches_previous_graph():
    old = Graph()
    old.setNode("old")
    widget = DagreD3Widget(old)
    replacement = Graph()
    replacement.setNode("new")

    widget.graph = replacement
    old.setNode("ignored")
    replacement.setNode("latest")

    assert old._widget is None
    assert [node["id"] for node in _config(widget)["nodes"]] == ["new", "latest"]


def test_widget_mutation_methods_redraw_graph():
    widget = DagreD3Widget(attrs={"height": "50vh"})
    widget.addNode("a")
    widget.setNode("b")
    widget.addEdge("a", "b", label="First")
    widget.setEdge("b", "a", label="Back")
    widget.addGraph({"directed": False})
    widget.setGraph({"attrs": {"rankdir": "BT", "height": 250}})

    assert widget.graph.nodeCount() == 2
    assert widget.graph.edgeCount() == 2
    assert _config(widget)["directed"] is False
    assert _value(widget._tree["props"]["layout"])["rankdir"] == "BT"
    assert _value(widget._tree["props"]["style"]) == "height: 250px; width: 100%"


@pytest.mark.parametrize("field,value,expected", [("node-click", "a", "a"), ("edge-click", {"source": "a", "target": "b"}, ["a", "b"])])
def test_click_intents_keep_legacy_callback_values(field, value, expected):
    widget = DagreD3Widget()
    seen = []

    def callback(owner, clicked):
        seen.append((owner, clicked))

    widget.on_click(callback)
    content = {"type": "spaday:patch", "detail": {"model": "ipydagred3", "field": field, "value": value}}
    widget._on_msg(widget, content, [])
    widget.on_click(callback, remove=True)
    widget._on_msg(widget, content, [])

    assert seen == [(widget, expected)]


def test_serialization_does_not_mutate_node_or_edge_attributes():
    node = Node("a", style="fill: red")
    edge = Edge(node, Node("b"), style="stroke: blue")
    node.to_dict()
    edge.to_dict()

    assert node.attrs == {"style": "fill: red"}
    assert edge.attrs == {"style": "stroke: blue"}


def test_parallel_edges_raise_instead_of_disappearing():
    graph = Graph(multigraph=True)
    graph.setEdge("a", "b", label="First")
    graph.setEdge("a", "b", label="Second")

    with pytest.raises(ValueError, match="parallel edges"):
        DagreD3Widget(graph)


def test_repeated_edge_in_simple_graph_uses_latest_value():
    graph = Graph()
    graph.setEdge("a", "b", label="First")
    graph.setEdge("a", "b", label="Second")

    assert [edge["label"] for edge in _config(DagreD3Widget(graph))["edges"]] == ["Second"]
