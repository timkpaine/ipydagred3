from traitlets import HasTraits, observe, Unicode, Dict


class Node(HasTraits):
    name = Unicode()
    label = Unicode()
    attrs = Dict()
    _graph = None

    def __init__(self, name, label="", attrs=None):
        super(Node, self).__init__(self, name=name, label=label or name, attrs=attrs or {})

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

    @observe('attrs')
    def _observe_attrs(self, change):
        self._notify_change('attrs', change['new'])

    def to_dict(self):
        ret = {}
        ret["name"] = self.name
        ret["attrs"] = self.attrs
        ret["attrs"]["label"] = self.label
        return ret
