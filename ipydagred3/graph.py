from traitlets import HasTraits, observe, Bool, Instance, List, Dict
from .edge import Edge
from .node import Node


class Graph(HasTraits):
    directed = Bool(default_value=True)
    multigraph = Bool(default_value=False)
    compound = Bool(default_value=False)
    attrs = Dict()

    edges = List(trait=Instance(Edge))
    nodes = List(trait=Instance(Node))

    _widget = None

    def __init__(self, directed=True, multigraph=False, compound=False, attrs=None):
        super(Graph, self).__init__(directed=directed, multigraph=multigraph, compound=compound, attrs=attrs or {})

    def isDirected(self):
        return self.directed

    def isMultiGraph(self):
        return self.multigraph

    def setGraph(self, config):
        config = config or {}
        self.directed = config.get("directed", self.directed)
        self.multigraph = config.get("multigraph", self.multigraph)
        self.compound = config.get("compound", self.compound)
        self.attrs = config.get("attrs", self.attrs)

    def edgeCount(self):
        return len(self.edges)

    def hasEdge(self, edge):
        if isinstance(edge, Edge):
            return edge in self.edges
        elif isinstance(edge, tuple):
            if isinstance(edge[0], Node):
                return any((e for e in self.edges if e.v == edge[0] and e.w == edge[1]))
            else:
                return any((e for e in self.edges if e.v.name == edge[0] and e.w.name == edge[1]))
        return edge in (e.label for e in self.edges)

    # inEdges(inNodeName: string, outNodeName?: string): Edge[]|undefined;
    # outEdges(outNodeName: string, inNodeName?: string): Edge[]|undefined;
    # removeEdge(outNodeName: string, inNodeName: string): Graph;
    # setDefaultEdgeLabel(callback: string|((v: string, w: string, name?: string) => string|Label)): Graph;
    def setEdge(self, edge_or_node1, node2=None, label="", **attrs):
        if isinstance(edge_or_node1, Edge):
            if edge_or_node1.v not in self.nodes:
                self.setNode(edge_or_node1.v)
            if edge_or_node1.w not in self.nodes:
                self.setNode(edge_or_node1.w)
            self.edges.append(edge_or_node1)
            edge_or_node1['label'] = label or edge_or_node1.label
            edge_or_node1['tooltip'] = attrs.pop("tooltip", edge_or_node1.tooltip)
            edge_or_node1['labelpos'] = attrs.pop("labelpos", edge_or_node1.labelpos)
            edge_or_node1['labeloffset'] = attrs.pop("labeloffset", edge_or_node1.labeloffset)
            edge_or_node1['attrs'].update(attrs)
            return edge_or_node1
        if isinstance(edge_or_node1, Node):
            node1 = edge_or_node1
        else:
            # create and add node
            node1 = self.setNode(edge_or_node1)
        if not isinstance(node2, Node):
            node2 = self.setNode(node2)

        edge = Edge(node1, node2, label=label, **attrs)
        edge._setGraph(self)
        self.edges.append(edge)
        self.post({"type": "setEdge",
                   "source": edge.to_dict()})
        return edge

    # TODO
    # children(parentName: string): string|undefined;

    def hasNode(self, node):
        if isinstance(node, Node):
            return node in self.nodes
        return node in (n.name for n in self.nodes)

    # neighbors(name: string): Node[]|undefined;

    def nodeCount(self):
        return len(self.nodes)

    # parent(childName: string): string|undefined;
    # predecessors(name: string): Node[]|undefined;
    # removeNode(name: string): Graph;
    # setDefaultNodeLabel(callback: string|((nodeId: string) => string|Label)): Graph;

    def setNode(self, node, **attrs):
        if not isinstance(node, Node):
            # find existing
            for n in self.nodes:
                if n.name == node:
                    node = n
                    break
            # doesnt exist, make new
            if not isinstance(node, Node):
                node = Node(node, **attrs)
                self.nodes.append(node)
            else:
                node.shape = attrs.pop("shape", node.shape)
                node.label = attrs.pop("label", node.label)
                node.attrs.update(attrs)
        else:
            if node not in self.nodes:
                self.nodes.append(node)
            else:
                node.shape = attrs.pop("shape", node.shape)
                node.label = attrs.pop("label", node.label)
                node.attrs.update(attrs)

        node._setGraph(self)
        self.post({"type": "setNode",
                   "source": node.to_dict()})
        return node

    # setParent(childName: string, parentName: string): void;
    # sinks(): Node[];
    # sources(): Node[];
    # successors(name: string): Node[]|undefined;

    # internal
    def _setWidget(self, w):
        self._widget = w

    def post(self, msg):
        if self._widget:
            self._widget.post(msg)
        return

    def _notify_change(self, source, attr, value):
        if isinstance(source, Edge):
            self.post({"type": "edge",
                       "source": (source.v, source.w),
                       "attr": attr,
                       "value": value})

        elif isinstance(source, Node):
            self.post({"type": "node",
                       "source": source.name,
                       "attr": attr,
                       "value": value})
        elif source == self:
            self.post({"type": "graph",
                       "source": "",
                       "attr": attr,
                       "value": value})
        else:
            raise Exception('Unknown source: {}'.format(source))

    @observe('directed')
    def _observe_directed(self, change):
        self._notify_change(self, 'directed', change['new'])

    @observe('multigraph')
    def _observe_multigraph(self, change):
        self._notify_change(self, 'multigraph', change['new'])

    @observe('compound')
    def _observe_compound(self, change):
        self._notify_change(self, 'compound', change['new'])

    @observe('attrs')
    def _observe_attrs(self, change):
        self._notify_change(self, 'attrs', change['new'])

    def to_dict(self):
        ret = {}
        ret["directed"] = self.directed
        ret["multigraph"] = self.multigraph
        ret["compound"] = self.compound
        ret["attrs"] = self.attrs
        ret["nodes"] = [n.to_dict() for n in self.nodes]
        ret["edges"] = [e.to_dict() for e in self.edges]
        return ret
