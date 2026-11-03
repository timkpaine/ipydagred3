# Compatibility reference

`DagreD3Widget` is a `spaday.Widget` rendering `spaday-dagre`. The Python distribution contains
no JavaScript build or Jupyter extensions; frontend assets come from its Spaday dependencies.

## Graph API

`Graph`, `Node`, `Edge`, and the widget's `addGraph`, `setGraph`, `addNode`, `setNode`, `addEdge`,
and `setEdge` methods retain their existing names. Changes made through those methods or trait
assignments update the displayed graph. In-place edits to trait dictionaries and lists do not emit
trait notifications; reassign the trait or use the mutation methods to redraw.

Assigning `widget.graph` replaces the displayed graph and detaches the previous graph's callbacks.
`Graph.to_dict()` retains the legacy serialization format.

## Layout and appearance

`Graph.attrs` accepts Dagre layout options including `rankdir`, `align`, `nodesep`, `edgesep`,
`ranksep`, `marginx`, `marginy`, and `ranker`. Defaults retain top-to-bottom layout, 70-pixel node
spacing, 50-pixel rank spacing, and 20-pixel margins.

`height` and `width` accept numbers in pixels or CSS dimension strings. Defaults are `400px` and
`100%`. The component supports wheel zoom, drag pan, and double-click reset.

Node shapes are `rect`, `circle`, `ellipse`, and `diamond`. Circles use equal width and height.
Node attributes include `width`, `height`, `class`, `style`, and `labelStyle`. A node's `parent`
attribute names a compound cluster. Edge attributes include `class`, `style`, and `labelStyle`.
`style` applies CSS to the node shape or edge line; `labelStyle` applies CSS to the label.
Custom `tooltip` values render as native SVG titles, and labels render as plain text.

`directed=False` hides arrowheads. The `compound` flag remains available on the Python model;
browser clustering follows node `parent` attributes. `multigraph=True` is accepted for graphs with
one edge per ordered pair of nodes. Parallel edges raise `ValueError` because the component does
not route them separately. Repeated edges in a simple graph display the latest edge's attributes.

Dagre-d3-specific arrowhead variants, HTML labels, edge `labelpos` and `labeloffset`, and arbitrary
renderer attributes are not implemented by `spaday-dagre`. Those fields remain serializable in
the Python models but do not affect rendering. SVG geometry and animations follow Spaday's renderer.

## Click events

`widget.on_click(callback, remove=False)` registers or removes a callback. The callback receives
`(widget, node_id)` for a node and `(widget, [source, target])` for an edge. Both edge lines and
edge labels are clickable.
