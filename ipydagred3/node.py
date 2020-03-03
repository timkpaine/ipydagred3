from traitlets import HasTraits, validate, observe, TraitError, Unicode, Dict


class Node(HasTraits):
    name = Unicode()
    label = Unicode()
    shape = Unicode(default_value="rect")  # rect, circle, ellipse, diamond
    tooltip = Unicode(default_value="")
    attrs = Dict()

    _graph = None

    def __init__(self, name, label="", shape="rect", tooltip="", **attrs):
        super(Node, self).__init__(self, name=name, label=label or name, shape=shape, tooltip=tooltip or label or name, attrs=attrs or {})

    def _setGraph(self, g):
        self._graph = g

    def _notify_change(self, attr, value):
        if not self._graph:
            return
        self._graph._notify_change(self, attr, value)

    @observe('name')
    def _observe_name(self, change):
        self._notify_change('name', change['new'])

    @observe('label')
    def _observe_label(self, change):
        self._notify_change('label', change['new'])

    @observe('shape')
    def _observe_shape(self, change):
        self._notify_change('shape', change['new'])

    @observe('tooltip')
    def _observe_tooltip(self, change):
        self._notify_change('tooltip', change['new'])

    @observe('attrs')
    def _observe_attrs(self, change):
        self._notify_change('attrs', change['new'])

    @validate("shape")
    def _validate_shape(self, proposal):
        if proposal.value not in ("rect", "circle", "ellipse", "diamond"):
            raise TraitError('Shape must be in ("rect", "circle", "ellipse", "diamond"), got: {}'.format(proposal))
        return proposal.value

    def to_dict(self):
        ret = {}
        ret["name"] = self.name
        ret["attrs"] = self.attrs
        ret["attrs"]["label"] = self.label
        ret["attrs"]["shape"] = self.shape
        ret["attrs"]["tooltip"] = self.tooltip or self.label
        return ret
