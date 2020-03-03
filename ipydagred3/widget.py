# coding: utf-8
from ipywidgets import DOMWidget, CallbackDispatcher
from traitlets import observe, Unicode, Instance, Dict
from functools import wraps
from .graph import Graph
from ._version import __version__


class DagreD3Widget(DOMWidget):
    _model_name = Unicode('DagreD3Model').tag(sync=True)
    _model_module = Unicode("ipydagred3").tag(sync=True)
    _model_module_version = Unicode("^" + __version__).tag(sync=True)
    _view_name = Unicode('DagreD3View').tag(sync=True)
    _view_module = Unicode("ipydagred3").tag(sync=True)
    _view_module_version = Unicode("^" + __version__).tag(sync=True)

    graph = Instance(Graph, args=(), kwargs={})
    _graph = Dict().tag(sync=True)

    def __init__(self, graph=None, *args, **kwargs):
        super(DagreD3Widget, self).__init__()

        if not isinstance(graph, Graph):
            graph = Graph(*args, **kwargs)
        self.graph = graph

        # set widget for callbacks
        self.graph._setWidget(self)

        # for click events
        self._click_handlers = CallbackDispatcher()
        self.on_msg(self._handle_click_msg)

    def on_click(self, callback, remove=False):
        self._click_handlers.register_callback(callback, remove=remove)

    def click(self, value):
        self._click_handlers(self, value)

    def _handle_click_msg(self, _, content, buffers):
        if content.get('event', '') == 'click':
            self.click(content.get('value', ''))

    @wraps(Graph.setGraph)
    def setGraph(self, *args, **kwargs):
        self.graph.setGraph(*args, **kwargs)

    @wraps(Graph.setNode)
    def setNode(self, *args, **kwargs):
        self.graph.setNode(*args, **kwargs)

    @wraps(Graph.setEdge)
    def setEdge(self, *args, **kwargs):
        self.graph.setEdge(*args, **kwargs)

    def post(self, msg):
        self.send(msg)

    @observe('graph')
    def _observe_graph(self, change):
        self._graph = change['new'].to_dict()
