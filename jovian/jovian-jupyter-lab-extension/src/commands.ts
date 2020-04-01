import {
  JupyterFrontEnd,
  ILabShell
} from '@jupyterlab/application';

import nb from './NBKernel'

let app:JupyterFrontEnd;
let labShell: ILabShell;

export function setApp(_app:JupyterFrontEnd, _labShell: ILabShell):void {
  /**
   * save the settings of JupyterLab
   */
  app = _app;
  labShell = _labShell;
}

export function getShell(): ILabShell{
  /**
   * returns ILabShell of JupyterLab system
   */
  return labShell;
}

export async function hasJovian(callBack:()=>any):Promise<void> {
  /**
   * checks if Jovian library exists
   * if exists, it will run the callback function
   */
  let found:boolean = false;
  let code:string = "help('jovian')";
  await nb.execute(code).then(
    (res) => {
      if (!res.toLocaleLowerCase().includes("no python documentation found")){
        found = true;
      }
    }
  );
  if (found){
    callBack();
  } else {
    alert(
      "We found that Jovian is not installed on your computer! " +
      "Please install Jovian to use this extension."
    );
  }
}

export async function getProjectId():Promise<string> {
  /**
   * returns the project id of the current notebook
   */
  let slug:string|undefined = undefined, gist:any;
  let projectId:string|undefined = undefined;
  await getSlug().then(
    (res) => slug = res
  );
  if (slug != undefined) {
    await getGist(slug).then(
      (res) => gist = res
    );
    let username: string = gist.currentUser.username;
    projectId = username + "/" + gist.title;
  }
  return projectId;
}

export async function getSlug():Promise<string> {
  /**
   * returns the slug number of the current notebook
   */
  let code:string = "import json\n" +
    "with open('.jovianrc') as f:\n" +
    "\tjovianrc = json.load(f)\n" +
    "\tprint(jovianrc)";
  let list:any;
  await nb.execute(code).then(
    (res) => list = eval("("+res+")")
  );
  if (list.notebooks && list.notebooks[nb.currentNotebookName()]) {
    return (list.notebooks[nb.currentNotebookName()].slug);
  }
  return undefined;
}

export async function getGist(slug: string): Promise<any> {
  /**
   * returns details of the current notebook
   */
  let code:string = "import json\n" +
    "import jovian.utils.api as api\n" +
    "print(json.dumps(api.get_gist('" + slug + "')))";
  let list:any;
  await nb.execute(code).then(
    (res) => list = JSON.parse(res)
  );
  list = list === false ? undefined : list;
  return list;
}

export async function saveNotebook():Promise<void> {
  /**
   * save the current notebook
   */
  await app.commands.execute('docmanager:save');
}

export async function triggerSidebar():Promise<void> {
  /**
   * open or close the sidebar
   */
  await app.commands.execute('application:toggle-left-area');
}