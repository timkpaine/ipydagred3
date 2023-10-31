/* eslint-disable no-underscore-dangle */
import {DOMWidgetView} from "@jupyter-widgets/base";
import {graphlib, render} from "dagre-d3-es";
import * as d3 from "d3";
import throttle from "lodash/throttle";

// Import the CSS
import "../style/index.css";

export class DagreD3View extends DOMWidgetView {
  graph;

  svg;

  inner;

  tooltip;

  renderer;

  throttled_render;

  queued;

  render() {
    this.model.on("msg:custom", this._handle_message, this);
    this.el.classList.add("dagred3");

    this.tooltip = document.querySelector("#dagred3tooltip");
    if (!this.tooltip) {
      this.tooltip = document.createElement("div");
      this.tooltip.id = "dagred3tooltip";
      this.tooltip.style.visibility = "hidden";
      this.tooltip.style.position = "absolute";
      this.tooltip.style.zIndex = "1000";
      document.body.appendChild(this.tooltip);
    }

    const el = d3.select(this.el);
    this.svg = el.append("svg");

    this.inner = this.svg.append("g");
    this.graph = new graphlib.Graph({directed: this.model.get("_graph").directed});
    this.graph.setGraph({
      nodesep: this.model.get("_graph").attrs.nodesep || 70,
      ranksep: this.model.get("_graph").attrs.ranksep || 50,
      rankdir: this.model.get("_graph").attrs.rankdir || "TB",
      marginx: this.model.get("_graph").attrs.marginx || 20,
      marginy: this.model.get("_graph").attrs.marginy || 20,
    });

    // set height and width
    const model_height = this.model.get("_graph").attrs.height;
    const model_width = this.model.get("_graph").attrs.width;
    if (model_height) {
      this.svg.height = model_height;
    }
    if (model_width) {
      this.svg.width = model_width;
    }

    // eslint-disable-next-line new-cap
    this.renderer = new render();

    this.throttled_render = throttle(() => this._render(), 5);

    this.displayed.then(() => {
      // Set up zoom support
      const zoom = d3.zoom().on("zoom", (event) => {
        this.inner.attr("transform", event.transform);
      });
      this.svg.call(zoom);

      // Center the graph
      const initialScale = 0.75;
      const width = this.el.offsetWidth;
      const height = this.el.offsetHeight;
      this.svg.call(
        zoom.transform,
        d3.zoomIdentity.translate((width - (this.graph.graph().width || 0) * initialScale) / 2, (height - (this.graph.graph().height || 0) * initialScale) / 2).scale(initialScale),
      );

      this.graph_changed();
    });
  }

  _render() {
    this.renderer(this.inner, this.graph);

    const tooltip = d3.select("#dagred3tooltip");
    this.inner
      .selectAll("g.node")
      // TODO commenting out for d3v5 -> d3v7 seems to have no effect ¯\_(ツ)_/¯
      // .attr("data-tooltip", (event, value) => this.graph.node(value).tooltip)
      .on("click", (event, value) => {
        this.send({event: "click", value});
      })
      .on("mouseover", () => tooltip.style("visibility", "visible"))
      .on("mousemove", (event, value) => {
        tooltip
          .text(this.graph.node(value).tooltip)
          .style("top", `${event.pageY - 10}px`)
          .style("left", `${event.pageX + 10}px`);
      })
      .on("mouseout", () => tooltip.style("visibility", "hidden"));
  }

  _handle_message(msg) {
    if (msg.type === "setNode") {
      this.setNode(msg.source.name, msg.source.attrs);
    } else if (msg.type === "setEdge") {
      this.setEdge(msg.source.v.name, msg.source.w.name, msg.source.attrs);
    } else if (msg.type === "graph") {
      const ob = this.graph.graph();
      ob[msg.attr] = msg.value;
      this.graph.setGraph(ob);
    } else if (msg.type === "node") {
      this.setNode(msg.source.name, msg.source.attrs);
    } else if (msg.type === "edge") {
      this.setEdge(msg.source.v.name, msg.source.w.name, msg.source.attrs);
    }
    this.throttled_render();
  }

  setNode(name, attrs) {
    this.graph.setNode(name, attrs);
  }

  setEdge(v, w, attrs) {
    const tooltip = d3.select("#dagred3tooltip");
    const label = document.createElement("u");
    label.onmouseover = () => tooltip.style("visibility", "visible");

    label.onmouseout = () => tooltip.style("visibility", "hidden");

    label.onmousemove = (e) =>
      tooltip
        .text(attrs.tooltip)
        .style("top", `${e.pageY - 10}px`)
        .style("left", `${e.pageX + 10}px`);

    label.onclick = () => {
      this.send({event: "click", value: [v, w]});
    };

    label.innerHTML = attrs.label;
    // eslint-disable-next-line no-param-reassign
    attrs.label = label;
    // eslint-disable-next-line no-param-reassign
    attrs.labelType = "html";
    this.graph.setEdge(v, w, attrs);
  }

  graph_changed() {
    const graph = this.model.get("_graph");

    const ob = {
      compound: graph.compound,
      directed: graph.directed,
      multigraph: graph.multigraph,
      ...this.graph.graph(),
    };
    this.graph.setGraph(ob);

    graph.nodes.forEach((n) => {
      this.setNode(n.name, n.attrs);
    });
    graph.edges.forEach((e) => {
      this.setEdge(e.v.name, e.w.name, e.attrs);
    });
    this.throttled_render();
  }
}
