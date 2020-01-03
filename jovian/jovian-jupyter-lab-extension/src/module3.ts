import { setDefault, askAPIKeys } from './module2';
import NBKernel from './NBKernel';
let body:any;

function setting():void{
  initialHeader();
  let header:HTMLElement = initialHeader();
  let setDefaultparams:HTMLElement = addCheckBox("Set Default options for commit");
  let clearAPI:HTMLElement = addCheckBox("Clear the API key");
  let changeAPI:HTMLElement = addCheckBox("Change the API key");
  let disabled:HTMLElement = addCheckBox("Disable the extension");
  setCheckBox(clearAPI,true);
  header.appendChild(setDefaultparams);
  header.appendChild(clearAPI);
  header.appendChild(changeAPI);
  header.appendChild(disabled);
  header.appendChild(addButtons("Submit",()=>{
    if (getCheckBox(setDefaultparams)){
      setDefault();
      closeWindow();
    };
    if (getCheckBox(clearAPI)){
      NBKernel.execute("import jovian as jvn\njvn.utils.credentials.purge_creds()").then(
        ()=>closeWindow()
      );
    };
    if (getCheckBox(changeAPI)){
      NBKernel.execute("import jovian as jvn\njvn.utils.credentials.purge_creds()").then(
        ()=>askAPIKeys()
      );
      closeWindow();
    };
    if (getCheckBox(disabled)){
      NBKernel.execute("import os\nos.system('jupyter labextension disable Jovian')").then(
        ()=>{
          alert("You have disabled the Jovian extension, please refresh your browser.");
          closeWindow();
        }
      );
    };
    if (!getCheckBox(clearAPI) && !getCheckBox(setDefaultparams) && !getCheckBox(disabled)){
      alert("Settings unchanged!");
      closeWindow();
    }
  }));
  openWindow();
}

function addCheckBox(value:string):HTMLElement{
  let div:HTMLElement = document.createElement("div");
  let checkBox:any = document.createElement("input");
  let label:any = document.createElement("h2");
  label.innerText = value;
  label.className = "p-Widget jp-Dialog-header";
  checkBox.setAttribute('type', "checkbox");
  checkBox.className = "form-check-input";
  checkBox.style["margin-top"] = "20px";
  div.className = "p-Widget jp-Input-Dialog jp-Dialog-body form-check";
  div.appendChild(checkBox);
  div.appendChild(label);
  return div;
}

function getCheckBox(inp:HTMLElement):boolean{
  if ((inp.getElementsByTagName("input")[0] as any).checked == true){
    return true;
  }
  return false;
}

function setCheckBox(inp:HTMLElement, value:boolean):void{
  (inp.getElementsByTagName("input")[0] as any).checked = value;
}

function addButtons(name:string|null, callBack = ()=>{}):HTMLElement{
  let footer:HTMLElement = document.createElement("div");
  let icon1:HTMLElement = document.createElement("div");
  let icon2:HTMLElement = document.createElement("div");
  let cancle:HTMLElement = document.createElement("div");
  let ok:HTMLElement = document.createElement("div");
  let cancleBut:HTMLElement = document.createElement("button");
  let okBut:HTMLElement = document.createElement("button");
  footer.className = "p-Widget jp-Dialog-footer";
  icon1.className = "jp-Dialog-buttonIcon";
  icon2.className = "jp-Dialog-buttonIcon";
  cancle.className = "jp-Dialog-buttonLabel";
  ok.className = "jp-Dialog-buttonLabel";
  cancleBut.className = "jp-Dialog-button jp-mod-reject jp-mod-styled";
  okBut.className = "jp-Dialog-button jp-mod-accept jp-mod-styled";
  cancle.innerText = "Close";
  cancleBut.appendChild(icon1);
  cancleBut.appendChild(cancle);
  footer.appendChild(cancleBut);
  (<any>cancleBut).onclick = ()=>{
    closeWindow();
  };
  if (name!=null){
    cancle.innerText = "Cancle";
    ok.innerText = name;
    okBut.appendChild(icon2);
    okBut.appendChild(ok);
    footer.appendChild(okBut);
    (<any>okBut).onclick = callBack;
  }
  return footer;
}

function openWindow():void {
  insertAfter(body, document.getElementById("main"));
}

function closeWindow():void {
  body.parentNode.removeChild(body);
}

function initialHeader():HTMLElement{
  let header:HTMLElement = document.createElement("div");
  let subHeader:HTMLElement = document.createElement("div");
  header.className = "p-Widget jp-Dialog";
  subHeader.className = "p-Widget p-Panel jp-Dialog-content";
  header.appendChild(subHeader);
  body = header;
  return subHeader;
}

function insertAfter(newNode:any, referenceNode:any):void {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

export default setting;