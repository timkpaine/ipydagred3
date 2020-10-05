/* eslint-disable @typescript-eslint/explicit-function-return-type */
/* eslint-disable no-underscore-dangle */
/* eslint-disable @typescript-eslint/unbound-method */
import {DOMWidgetView} from "@jupyter-widgets/base";
import {graphlib, render} from "dagre-d3";
import * as d3 from "d3";


// Import the CSS
import "../css/widget.css";


export interface DagreD3Message {
  type: "setNode" | "setEdge" | "graph" | "node" | "edge";
  source: any;
  attr: string;
  value: any;
}


export
class DagreD3View extends DOMWidgetView {
  public graph: graphlib.Graph;
  public svg: any;
  public inner: any;
  public tooltip: HTMLDivElement | null;
  public renderer: any;
  public throttle: any;
  public queued: boolean;

  public render(): void {
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
    this.svg.attr("height", "600");
    this.svg.attr("width", "800");

    this.inner = this.svg.append("g");
    this.inner.attr("height", "600");
    this.inner.attr("width", "800");
    this.graph = new graphlib.Graph().setGraph({height: 400, width: 400});

    this.renderer = new render();

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

      this.svg.attr("height", this.graph.graph().height * initialScale + 40);
      this.graph_changed();
    });
  }

  public _render(): void {
    if (this.throttle) {
      // do not schedule a render
      // eslint-disable-next-line no-console
      console.log("[ipydagred3] throttling...");
      this.queued = true;
      return;
    }

    this.throttle = 1; // set guard

    this.renderer(this.inner, this.graph);

    const tooltip = d3.select("#dagred3tooltip");
    this.inner.selectAll("g.node")
      .attr("data-tooltip", (v: string) => (this.graph.node(v) as any).tooltip)
      .on("click", (v: string) => {
        this.send({event: "click", value: v});
      })
      .on("mouseover", () => tooltip.style("visibility", "visible"))
      .on("mousemove", (v: string) => {
        tooltip.text((this.graph.node(v) as any).tooltip)
          .style("top", (d3.event.pageY - 10) + "px")
          .style("left", (d3.event.pageX + 10) + "px");
      })
      .on("mouseout", () => tooltip.style("visibility", "hidden"));

    // any queued will now have been rendered
    this.queued = false;

    // remove guard after timeout, rerender if any queue
    this.throttle = setTimeout(() => {
      // since this sets throttle, if any render
      // requests come in during the 200ms cooldown,
      // they'll set queued and a rerender will be triggered
      this.throttle = undefined;
      if (this.queued) {
        this._render();
      }
    }, 200);
  }

  public _handle_message(msg: DagreD3Message): void {
    if (msg.type === "setNode") {
      this.setNode(msg.source.name, msg.source.attrs);
    } else if (msg.type === "setEdge") {
      this.setEdge(msg.source.v.name, msg.source.w.name, msg.source.attrs);
    } else if (msg.type === "graph") {
      const ob = {} as any;
      ob[msg.attr] = msg.value;
      this.graph.setGraph(ob);
    } else if (msg.type === "node") {
      this.setNode(msg.source.name, msg.source.attrs);
    } else if (msg.type === "edge") {
      this.setEdge(msg.source.v.name, msg.source.w.name, msg.source.attrs);
    }
    this._render();
  }

  public setNode(name: string, attrs: any): void {
    this.graph.setNode(name, attrs);
  }

  public setEdge(v: string, w: string, attrs: any): void {
    const tooltip = d3.select("#dagred3tooltip");
    const label = document.createElement("u");
    label.onmouseover = () => tooltip.style("visibility", "visible");

    label.onmouseout = () => tooltip.style("visibility", "hidden");

    label.onmousemove = (e: MouseEvent) => tooltip.text(attrs.tooltip)
      .style("top", (e.pageY - 10) + "px")
      .style("left", (e.pageX + 10) + "px");

    label.onclick = () => {
      this.send({event: "click", value: [v, w]});
    };

    label.innerHTML = attrs.label;
    attrs.label = label;
    attrs.labelType = "html";
    this.graph.setEdge(v, w, attrs);
  }

  public graph_changed() {
    const graph = this.model.get("_graph");

    const ob = {
      compound: graph.compound,
      directed:  graph.directed,
      multigraph: graph.multigraph,
    };

    this.graph.setGraph(ob);

    for (const n of graph.nodes) {
      this.setNode(n.name, n.attrs);
    }
    for (const e of graph.edges) {
      this.setEdge(e.v.name, e.w.name, e.attrs);
    }
    this._render();
  }
}
