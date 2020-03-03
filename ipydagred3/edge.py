from .node import Node
from traitlets import HasTraits, TraitError, observe, validate, Unicode, Instance, Float, Dict


class Edge(HasTraits):
    v = Instance(Node)
    w = Instance(Node)
    label = Unicode()
    attrs = Dict()
    tooltip = Unicode(default_value="")
    labelpos = Unicode(default_value="r")
    labeloffset = Float()
    arrowhead = Unicode(default_value="vee")

    _graph = None

    def __init__(self, v, w, label="", labelpos="r", labeloffset=0.0, tooltip="", **attrs):
        super(Edge, self).__init__(v=v, w=w, label=label, labelpos=labelpos, labeloffset=labeloffset, tooltip=tooltip or label or "{}->{}".format(v, w), attrs=attrs or {})

    def _setGraph(self, g):
        self._graph = g

    def _notify_change(self, attr, value):
        if not self._graph:
            return
        self._graph._notify_change(self, attr, value)

    @observe('v')
    def _observe_v(self, change):
        self._notify_change('v', change['new'])

    @observe('w')
    def _observe_w(self, change):
        self._notify_change('w', change['new'])

    @observe('label')
    def _observe_label(self, change):
        self._notify_change('label', change['new'])

    @observe('labelpos')
    def _observe_labelpos(self, change):
        self._notify_change('labelpos', change['new'])

    @observe('labeloffset')
    def _observe_labeloffset(self, change):
        self._notify_change('labeloffset', change['new'])

    @observe('tooltip')
    def _observe_tooltip(self, change):
        self._notify_change('tooltip', change['new'])

    @observe('attrs')
    def _observe_attrs(self, change):
        self._notify_change('attrs', change['new'])

    @validate("labelpos")
    def _validate_lablepos(self, proposal):
        if proposal.value not in ('l', 'c', 'r'):
            raise TraitError("lablepos must be in (l, c, r)")
        return proposal.value

    def to_dict(self):
        ret = {}
        ret["v"] = self.v.to_dict()
        ret["w"] = self.w.to_dict()
        ret["attrs"] = self.attrs
        ret["attrs"]["label"] = self.label
        ret["attrs"]["labelpos"] = self.labelpos
        ret["attrs"]["labeloffset"] = self.labeloffset
        ret["attrs"]["tooltip"] = self.tooltip
        ret["attrs"]["arrowhead"] = self.arrowhead
        return ret
