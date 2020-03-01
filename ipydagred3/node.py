from traitlets import HasTraits, observe, Unicode, Dict


class Node(HasTraits):
    name = Unicode()
    attrs = Dict()
    _graph = None

    def __init__(self, name, attrs=None):
        super(Node, self).__init__(self, name=name, attrs=attrs or {})

    def _setGraph(self, g):
        self._graph = g

    def _notify_change(self, attr, value):
        if not self._graph:
            return
        self._graph._notify_change(self, attr, value)

    @observe('name')
    def _observe_name(self, change):
        self._notify_change('name', change['new'])

    @observe('attrs')
    def _observe_attrs(self, change):
        self._notify_change('attrs', change['new'])

    def to_dict(self):
        ret = {}
        ret["name"] = self.name
        ret["attrs"] = self.attrs
        return ret