import { IDisposable } from "@lumino/disposable";
import {
  JupyterFrontEndPlugin,
  JupyterFrontEnd,
  ILabShell
} from "@jupyterlab/application";
import { ToolbarButton } from "@jupyterlab/apputils";
import { DocumentRegistry } from "@jupyterlab/docregistry";
import { NotebookPanel, INotebookModel } from "@jupyterlab/notebook";
import { downloadIcon } from "@jupyterlab/ui-components";
import { setApp, hasJovian } from "./commands";
import { commit } from "./commit";
import NK from "./NBKernel";

let positionIndex: number = 9; // The position will be used to add Jovian Icon

class JovainButtonExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
  /**
   * This class uses to add the Jovian button into
   * the jupyter lab toolbar
   */
  readonly app: JupyterFrontEnd;

  constructor(app: JupyterFrontEnd) {
    this.app = app;
    (<any>window).nb = NK;
  }

  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    // Create the on-click callback for the toolbar button.
    let callback: any = () => {
      hasJovian(commit);
    };

    // Create the toolbar button
    let button = new ToolbarButton({
      className: "jovian-lab-ext",
      icon: downloadIcon,
      onClick: callback,
      tooltip: "commit to jovian"
    });

    // Add the toolbar button to the notebook
    panel.toolbar.insertItem(positionIndex, "jovian", button);

    button.node.addEventListener(
      "DOMNodeInserted",
      () => {
        let jovian_button: any = button.node.firstChild;
        jovian_button.style["border-radius"] = 0;
        jovian_button.style.background = setIcon("white");
        jovian_button.firstChild.innerText = "Commit";
        jovian_button.firstChild.style.color = "black";
        jovian_button.firstChild.style["padding-left"] = "17px";

        // To set current slug when the notebook is loaded
        function delay(ms: number) {
          return new Promise(resolve => setTimeout(resolve, ms));
        }

        (async () => {
          await delay(3000);
          // TODO: Replace this delay when you discover kernel_ready type of event from Jlab
          // TODO: Also add event listener when you find one of kernel_restart like in notebook extension
          const code = `
from jovian.utils.slug import set_current_slug
set_current_slug("${NK.currentNotebookName()}")`;
          NK.execute(code);
        })();
      },
      {
        once: true,
        passive: true,
        capture: true
      }
    );

    button.node.onmouseenter = () => {
      let jovian_button: any = button.node.firstChild;
      jovian_button.style.background = setIcon("rgb(209, 207, 207)");
    };

    button.node.onmouseleave = () => {
      let jovian_button: any = button.node.firstChild;
      jovian_button.style.background = setIcon("white");
    };

    return button;
  }
}

function setIcon(color: string): string {
  /**
   * Helper function, which uses to set the icon for Jovian
   */
  let icon: string =
    color +
    " url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEIAAABCCAMAAADUivDaAAAAsVBMVEUAAAAKYf8LYv8LYP8LYf8LYv8KYv8MYP8JY/8MYP8JY/8RX/8AYv8Ab/8LYv8QYv////8OZP/9/f8jZf8FYP8UYf8aY//19/8dZP8mZv8AWP8BW/8ATf/6+/8qaP8AXv8AVP8ASv8Pav8AUv9ti/8AUP/x8/9Xfv/v8v/c4v9Ccv8ARv/r7v/U2//O1v93kv9Pef9Ld//W3P9ihP87b//g5f/V3P/J0v/H0P8waf8APv8gm8uUAAAADnRSTlMA/tj33vSLy8a3fG8IB6vY0CcAAAGsSURBVFjD7ZjZdoIwEIabunRnIgmBALIIuFF3a6vv/2ClQLH1HE5j4EKt/91/853MMJNhclO3HptI+VvN9nMp4aHXUQTU6d29lBCeeg0kgkCo1y5B3HeQIqZOswRxK4yAVnVE4yQQFxPIGSM0rSLCIJbFDQTyCMOzx2vfIxQkEcCicKTrm1XEKUghQAtCFSfSVx5BUggNgiXuYlXFk92WggQCwBrrOD3G0KBMqYhglEkGEuWBTHdbBHLp9MIuTtQfmIRKf9TVpD+cDgJOQb60fIfEyRmgSoG7LmEIqrUZnEKzXxFXRE0I0A5b/kgE467LDQq//RFthgwzJs6PuZF7Lt7szJtPh/1lGGUMyPwmtB3BKweYuejjRN0wIGkWzHnuo4QhhCDxB+6qqopHPk8Hsp94nHpH8BTIfcXZ+FpYLPGuUniTiCEoPUDAt5+LIkj8nh38zebwFYhdeEc4nQMdJ1JnUZbOwtuO6Ew1gsFE10czm+cfNfMpQby0/PXYDorS2vtjCtyyiIGgxIsg9r9ne3+m98U/QVzMStOqfdWVX7irr/3yjw8ofXyoVZ+79KZpyz4GvQAAAABJRU5ErkJggg==')  no-repeat 3.5px center / 19px 17px";
  return icon;
}

async function activate(app: JupyterFrontEnd, labShell: ILabShell) {
  /**
   * Registers two buttons into JupyterLab toolbar
   *  - button1: Jovian button
   *  - button2: Dropdown button
   */
  app.docRegistry.addWidgetExtension(
    "Notebook",
    new JovainButtonExtension(app)
  );
  setApp(app, labShell);
}

const extension: JupyterFrontEndPlugin<void> = {
  /**
   * settings of this plugin
   */
  id: "jovian_lab_extension",
  autoStart: true,
  requires: [ILabShell],
  activate
};

export default extension;
