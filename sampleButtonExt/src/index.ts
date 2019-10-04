import {
  JupyterFrontEnd, JupyterFrontEndPlugin, JupyterLab
} from '@jupyterlab/application';
import {
  IDisposable
} from '@phosphor/disposable';

import {
  ToolbarButton
} from '@jupyterlab/apputils';

import {
  DocumentRegistry
} from '@jupyterlab/docregistry';

import {
  NotebookPanel, INotebookModel
} from '@jupyterlab/notebook';
import { constructor } from 'react';

function activate (app: JupyterFrontEnd): void {
 let buttonExt = new RunAllButtonExt;
 app.docRegistry.addWidgetExtension('Notebook', buttonExt);
}
/**
 * Initialization data for the sampleButtonExt extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'sampleButtonExt',
  autoStart: true,
  activate
};

class RunAllButtonExt implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>{
  createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
    //create a onClick call back
    let runAllButton = () =>{
      console.log('Running all cells.')
    };

    //create a toolbar button
    let button = new ToolbarButton({
      className: 'runAllCells',
      iconClassName: 'fa fa-fast-forward',
      onClick: runAllButton,
      tooltip: 'Run all cells'
    });

    //add the button to the toolbar
    panel.toolbar.insertItem(6, 'runAllButton', button);

    return button
  }
}
export default extension;
