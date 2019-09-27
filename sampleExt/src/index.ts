import {
  JupyterFrontEnd, JupyterFrontEndPlugin
} from '@jupyterlab/application';


/**
 * Initialization data for the sampleExt extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'sampleExt',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    console.log('JupyterLab extension sampleExt is activated!');
  }
};

export default extension;
