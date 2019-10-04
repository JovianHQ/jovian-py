import {
  JupyterFrontEnd, JupyterFrontEndPlugin
} from '@jupyterlab/application';


/**
 * Initialization data for the sampleButtonExt extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'sampleButtonExt',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension sampleButtonExt is activated!');
  }
};

export default extension;
