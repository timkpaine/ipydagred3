// tslint:disable: max-classes-per-file
import {DOMWidgetView} from '@jupyter-widgets/base';
import {graphlib, render} from 'dagre-d3';
import {createPopper} from '@popperjs/core';
import * as d3 from 'd3';


// Import the CSS
import '../css/widget.css'


export interface DagreD3Message {
  type: "setNode" | "setEdge" | "graph" | "node" | "edge";
  source: any;
  attr: string;
  value: any;
}


export
class DagreD3View extends DOMWidgetView {
  graph: graphlib.Graph;
  svg: any;
  inner: any;

  render() {
    this.model.on("msg:custom", this._handle_message, this);
    this.el.classList.add('dagred3');

    const el = d3.select(this.el);
    this.svg = el.append("svg");
    this.svg.attr("height", "600");
    this.svg.attr("width", "800");

    this.inner = this.svg.append("g");
    this.inner.attr("height", "600");
    this.inner.attr("width", "800");
    this.graph = new graphlib.Graph().setGraph({height: 400, width: 400});

    const observer = new MutationObserver(this._render.bind(this));
    observer.observe(this.el, {
        attributes: true,
        attributeFilter: ["style"],
        subtree: false
    });

    this.displayed.then(() => {
      // Set up zoom support
      const zoom = d3.zoom()
        .on("zoom", () => {
          this.inner.attr("transform", d3.event.transform);
      });
      this.svg.call(zoom);

      // Center the graph
      const initialScale = 0.75;
      this.svg.call(zoom.transform, d3.zoomIdentity.translate((parseInt(this.svg.attr("width"), 10) - this.graph.graph().width * initialScale) / 2, 20).scale(initialScale));

      this.svg.attr('height', this.graph.graph().height * initialScale + 40);
      this.graph_changed();
    });
  }

  _render() {
    const renderer = new render();
    renderer(this.inner, this.graph);
  }

  _createTooltipNode(nodeName: string){
    const node = this.graph.node(nodeName);
    const name = node.name;
    const label = node.label;
    const description = node.description;
    return this._createTooltipCustom("<p class='name'>" + name + "</p><p class='name'>" + label + "<p class='description'>" + description + "</p>")
  }

  _createTooltipEdge(v: string, w: string){
    const edge = this.graph.edge(v, w);
    const name = edge.name;
    const label = edge.label;
    const description = edge.description;
    return this._createTooltipCustom("<p class='name'>" + name + "</p><p class='name'>" + label + "<p class='description'>" + description + "</p>")
  }

  _createTooltipCustom(innerHtml: string){
    const ret = document.createElement("div")
    ret.innerHTML = innerHtml;
    return ret
  }

  _handle_message(msg: DagreD3Message) {
    if(msg.type === "setNode") {
      this.graph.setNode(msg.source.name, msg.source.attrs);
      const node = this.graph.node(msg.source.name);
      createPopper(node.elem, this._createTooltipNode(msg.source.name), {
        placement: 'top',
      });
    } else if (msg.type === "setEdge") {
      this.graph.setEdge(msg.source.v.name, msg.source.w.name, msg.source.attrs);
    } else if (msg.type === "graph") {
      const ob = {} as any;
      ob[msg.attr] = msg.value;
      this.graph.setGraph(ob);
    } else if (msg.type === "node") {
      this.graph.setNode(msg.source.name, msg.source.attrs);
    } else if (msg.type === "edge") {
      this.graph.setEdge(msg.source.v.name, msg.source.w.name, msg.source.attrs);
    }
    this._render();
  }

  graph_changed() {
    const graph = this.model.get('_graph');

    const ob = {
      directed:  graph.directed,
      multigraph: graph.multigraph,
      compound: graph.compound,
    };

    this.graph.setGraph(ob);

    for(const n of graph.nodes) {
      this.graph.setNode(n.name, n.attrs);
    }
    for(const e of graph.edges) {
      this.graph.setEdge(e.v.name, e.w.name, e.attrs);
    }
    this._render();
  }
}
