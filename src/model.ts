// tslint:disable: max-classes-per-file
import {DOMWidgetModel, ISerializers} from '@jupyter-widgets/base';
import {MODULE_VERSION} from './version';


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

