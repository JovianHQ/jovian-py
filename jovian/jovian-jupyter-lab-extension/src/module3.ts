import { setDefault, askAPIKeys } from './module2';
import NBKernel from './NBKernel';
let body:any;

function setting():void{
  /**
   * This is the function we use to construct a setting window
   * and insert into the main window (Document.body), it includes
   * setting option(s) with corresponding callback function(s)
   */
  initialHeader();
  let header:HTMLElement = initialHeader();
  let setDefaultparams:HTMLElement = addSettingItem(
    "Set Default Commit Parameters", 
    "Set Default",
    () => {
      setDefault();
      closeWindow();
    }
  );
  let clearAPI:HTMLElement = addSettingItem(
    "Clear API Key", 
    "Clear",
    () => {
      NBKernel.execute("import jovian as jvn\njvn.utils.credentials.purge_creds()").then(
        ()=>closeWindow()
      );
    }
  );
  let changeAPI:HTMLElement = addSettingItem(
    "Change API Key", 
    "Change",
    () => {
      NBKernel.execute("import jovian as jvn\njvn.utils.credentials.purge_creds()").then(
        ()=>askAPIKeys()
      );
      closeWindow();
    }
  );;
  let disabled:HTMLElement = addSettingItem(
    "Disable Jovian Extension", 
    "Disable",
    () => {
      NBKernel.execute("import os\nos.system('jupyter labextension disable jovian_lab_extension')").then(
        ()=>{
          alert("You have disabled the Jovian extension, please refresh your browser. Run !jovian enable-extension in the lab to renable the Jovian extension");
          closeWindow();
        }
      );
    }
  );;
  header.appendChild(setDefaultparams);
  header.appendChild(clearAPI);
  header.appendChild(changeAPI);
  header.appendChild(disabled);
  header.appendChild(addButtons());
  openWindow();
}

function addSettingItem(labelText:string, buttonName:string, callBack:()=>void):HTMLElement{
  /**
   * Generate a setting option (item), with label, button and 
   * a callback function, which will be later merge into
   * the setting window
   */
  let div:HTMLElement = document.createElement("div");
  let label:any = document.createElement("h2");
  let icon:HTMLElement = document.createElement("div");
  let button:HTMLElement = document.createElement("button");
  let buttonInner:HTMLElement = document.createElement("div");
  div.className = "p-Widget jp-Input-Dialog jp-Dialog-body";
  label.className = "p-Widget jp-Dialog-header";
  icon.className = "jp-Dialog-buttonIcon";
  button.className = "jp-Dialog-button jp-mod-accept jp-mod-styled";
  buttonInner.className = "jp-Dialog-buttonLabel";
  label.innerText = labelText;
  buttonInner.innerText = buttonName;
  (button as any).style["width"] = "80%";
  (button as any).style["margin-left"] = "10%";
  (button as any).style["margin-top"] = "-10%";
  (button as any).style["font-size"] = "15px";
  button.appendChild(icon);
  button.appendChild(buttonInner);
  div.appendChild(label);
  div.appendChild(button);
  (<any>button).onclick = callBack;
  return div;
}

function addButtons():HTMLElement{
  /**
   * Create a footer for the window, and add necessary button(s) 
   * with corresponding callback function(s)
   */
  let footer:HTMLElement = document.createElement("div");
  let icon1:HTMLElement = document.createElement("div");
  let cancle:HTMLElement = document.createElement("div");
  let cancleBut:HTMLElement = document.createElement("button");
  footer.className = "p-Widget jp-Dialog-footer";
  icon1.className = "jp-Dialog-buttonIcon";
  cancle.className = "jp-Dialog-buttonLabel";
  cancleBut.className = "jp-Dialog-button jp-mod-reject jp-mod-styled";
  cancle.innerText = "Close";
  cancleBut.appendChild(icon1);
  cancleBut.appendChild(cancle);
  footer.appendChild(cancleBut);
  (<any>cancleBut).onclick = ()=>{
    closeWindow();
  };
  return footer;
}

function openWindow():void {
  /**
   * When the modal is ready, this function will show the modal (window)
   */
  insertAfter(body, document.getElementById("main"));
}

function closeWindow():void {
  /**
   * Close and clean the modal (window)
   */
  body.parentNode.removeChild(body);
}

function initialHeader():HTMLElement{
  /**
   * Use to create a modal, so we can add HTMLElements into this new modal
   */
  let header:HTMLElement = document.createElement("div");
  let subHeader:HTMLElement = document.createElement("div");
  header.className = "p-Widget jp-Dialog";
  subHeader.className = "p-Widget p-Panel jp-Dialog-content";
  header.appendChild(subHeader);
  body = header;
  return subHeader;
}

function insertAfter(newNode:any, referenceNode:any):void {
  /**
   * Insert modal into the corresponding position of Document.body
   */
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

export default setting;