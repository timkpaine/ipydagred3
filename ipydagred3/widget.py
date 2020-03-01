# coding: utf-8

from ipywidgets import DOMWidget
from traitlets import Unicode


class Widget(DOMWidget):
    _model_name = Unicode('Model').tag(sync=True)
    _model_module = Unicode("ipydagred3").tag(sync=True)
    _model_module_version = Unicode("0.1.0").tag(sync=True)
    _view_name = Unicode('View').tag(sync=True)
    _view_module = Unicode("ipydagred3").tag(sync=True)
    _view_module_version = Unicode("0.1.0").tag(sync=True)

    value = Unicode('Hello World').tag(sync=True)
