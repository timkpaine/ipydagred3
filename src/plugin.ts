import {
  Application, IPlugin
} from '@phosphor/application';

import {
  Widget
} from '@phosphor/widgets';

import {
  IJupyterWidgetRegistry
 } from '@jupyter-widgets/base';

import * as widgetExports from './widget';

import {
  MODULE_VERSION
} from './version';

const EXTENSION_ID = 'ipydagred3:plugin';

/**
 * The example plugin.
 */
const examplePlugin: IPlugin<Application<Widget>, void> = {
  id: EXTENSION_ID,
  requires: [IJupyterWidgetRegistry],
  activate: activateWidgetExtension,
  autoStart: true
};

export default examplePlugin;


/**
 * Activate the widget extension.
 */
function activateWidgetExtension(app: Application<Widget>, registry: IJupyterWidgetRegistry): void {
  registry.registerWidget({
    name: "ipydagred3",
    version: MODULE_VERSION,
    exports: widgetExports,
  });
}
