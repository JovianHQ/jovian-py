import { JupyterFrontEnd, ILabShell } from "@jupyterlab/application";
import nb from "./NBKernel";
import { alertWindow } from "./commit";

let app: JupyterFrontEnd;
let labShell: ILabShell;

export function setApp(_app: JupyterFrontEnd, _labShell: ILabShell): void {
  /**
   * save the settings of JupyterLab
   */
  app = _app;
  labShell = _labShell;
}

export function getShell(): ILabShell {
  /**
   * returns ILabShell of JupyterLab system
   */
  return labShell;
}

export async function hasJovian(callBack: () => any): Promise<void> {
  /**
   * checks if Jovian library exists
   * if exists, it will run the callback function
   */
  let found: boolean = false;
  let code: string = "help('jovian')";
  await nb.execute(code).then(res => {
    if (!res.toLocaleLowerCase().includes("no python documentation found")) {
      found = true;
    }
  });
  if (found) {
    callBack();
  } else {
    alertWindow(
      "This extension requires jovian python library. Install using 'pip intsall jovian --upgrade' "
    );
  }
}

export async function saveNotebook(): Promise<void> {
  /**
   * save the current notebook
   */
  await app.commands.execute("docmanager:save");
}
