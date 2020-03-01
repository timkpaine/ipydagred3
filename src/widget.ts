// tslint:disable: max-classes-per-file
import {DOMWidgetModel, DOMWidgetView, ISerializers} from '@jupyter-widgets/base';
import {MODULE_VERSION} from './version';
import {graphlib} from 'dagre-d3';


// Import the CSS
import '../css/widget.css'


export interface PerspectiveJupyterMessage {
  type: string;
  source: any;
  attr: string;
  value: any;
}


export
class DagreD3Model extends DOMWidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: DagreD3Model.modelName,
      _model_module: DagreD3Model.modelModule,
      _model_module_version: DagreD3Model.modelModuleVersion,
      _view_name: DagreD3Model.viewName,
      _view_module: DagreD3Model.viewModule,
      _view_module_version: DagreD3Model.viewModuleVersion,
      value : 'Hello World'
    };
  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
      // Add any extra serializers here
    }

  static modelName = 'DagreD3Model';
  static modelModule = "ipydagred3";
  static modelModuleVersion = MODULE_VERSION;
  static viewName = 'DagreD3View';   // Set to null if no view
  static viewModule = "ipydagred3";   // Set to null if no view
  static viewModuleVersion = MODULE_VERSION;
}


export
class DagreD3View extends DOMWidgetView {
  graph: graphlib.Graph;

  render() {
    this.el.classList.add('dagred3');
    this.graph = new graphlib.Graph().setGraph({});

    // this.value_changed();
    // this.model.on('change:value', this.value_changed, this);
  }

  _handle_message(msg: PerspectiveJupyterMessage) {
    // If in client-only mode (no Table on the python widget), message.data
    // is an object containing "data" and "options".
  }

  value_changed() {
    // this.el.textContent = this.model.get('value');
  }
}
