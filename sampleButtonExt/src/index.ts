import $ from "jquery";
import { IDisposable } from "@phosphor/disposable";

import {
  JupyterFrontEndPlugin,
  JupyterFrontEnd
} from "@jupyterlab/application";

import { ToolbarButton } from "@jupyterlab/apputils";

import { DocumentRegistry } from "@jupyterlab/docregistry";

import { NotebookPanel, INotebookModel } from "@jupyterlab/notebook";

import "../style/index.css";

class RunAllCellsButtonExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
  constructor(app: JupyterFrontEnd) {
    this.app = app;
  }

  readonly app: JupyterFrontEnd;

  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    // Create the on-click callback for the toolbar button.
    let runAllCells = () => {
      alert($(document.body).html());
      this.app.commands.execute("notebook:run-all-cells");
    };

    // Create the toolbar button
    let button = new ToolbarButton({
      className: "runAllCellsButton",
      iconClassName: "fa fa-fast-forward",
      onClick: runAllCells,
      tooltip: "Run All Cells"
    });

    // Add the toolbar button to the notebook
    panel.toolbar.insertItem(6, "runAllCells", button);

    // The ToolbarButton class implements `IDisposable`, so the
    // button *is* the extension for the purposes of this method.
    return button;
  }
}

function activate(app: JupyterFrontEnd): void {
  let buttonExtension = new RunAllCellsButtonExtension(app);
  app.docRegistry.addWidgetExtension("Notebook", buttonExtension);
  app.contextMenu.addItem({
    selector: ".jp-Notebook",
    command: "notebook:run-all-cells",
    rank: -0.5
  });
}

const extension: JupyterFrontEndPlugin<void> = {
  id: "runall-extension",
  autoStart: true,
  activate
};

export default extension;
