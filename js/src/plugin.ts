import {
  Application, IPlugin,
} from "@lumino/application";

import {
  Widget,
} from "@lumino/widgets";

import {
  IJupyterWidgetRegistry,
} from "@jupyter-widgets/base";

import {
  MODULE_VERSION,
} from "./version";

const EXTENSION_ID = "ipydagred3:plugin";

/**
 * The example plugin.
 */
const examplePlugin: IPlugin<Application<Widget>, void> = {
  activate: activateWidgetExtension,
  autoStart: true,
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
};

export default examplePlugin;


/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app: Application<Widget>, registry: IJupyterWidgetRegistry): void {
  registry.registerWidget({
    exports: async () => await import(/* webpackChunkName: "ipydagred3" */ "./widget"),
    name: "ipydagred3",
    version: MODULE_VERSION,
  });
}
