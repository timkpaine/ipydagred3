// tslint:disable: max-classes-per-file
import {
  DOMWidgetModel, DOMWidgetView, ISerializers
} from '@jupyter-widgets/base';

import {
  MODULE_NAME, MODULE_VERSION
} from './version';

// Import the CSS
import '../css/widget.css'


export
class ExampleModel extends DOMWidgetModel {
  defaults() {
    return {...super.defaults(),
      _model_name: ExampleModel.modelName,
      _model_module: ExampleModel.modelModule,
      _model_module_version: ExampleModel.modelModuleVersion,
      _view_name: ExampleModel.viewName,
      _view_module: ExampleModel.viewModule,
      _view_module_version: ExampleModel.viewModuleVersion,
      value : 'Hello World'
    };
  }

  static serializers: ISerializers = {
      ...DOMWidgetModel.serializers,
      // Add any extra serializers here
    }

  static modelName = 'ExampleModel';
  static modelModule = MODULE_NAME;
  static modelModuleVersion = MODULE_VERSION;
  static viewName = 'ExampleView';   // Set to null if no view
  static viewModule = MODULE_NAME;   // Set to null if no view
  static viewModuleVersion = MODULE_VERSION;
}


export
class ExampleView extends DOMWidgetView {
  render() {
    this.el.classList.add('custom-widget');

    this.value_changed();
    this.model.on('change:value', this.value_changed, this);
  }

  value_changed() {
    this.el.textContent = this.model.get('value');
  }
}
