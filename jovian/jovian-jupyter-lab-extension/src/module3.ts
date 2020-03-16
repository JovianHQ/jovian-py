import { setDefault, askAPIKeys } from './module2';
import NBKernel from './NBKernel';
let body:any;

function setting():void{
  initialHeader();
  let header:HTMLElement = initialHeader();
  let setDefaultparams:HTMLElement = addButton("Set Default options for commit");
  let clearAPI:HTMLElement = addButton("Clear the API key");
  let changeAPI:HTMLElement = addButton("Change the API key");
  let disabled:HTMLElement = addButton("Disable the extension");
  header.appendChild(setDefaultparams);
  header.appendChild(clearAPI);
  header.appendChild(changeAPI);
  header.appendChild(disabled);
}

function addButton(value:string):HTMLElement{
  let div:HTMLElement = document.createElement("div");
  let button:any = document.createElement("input");
  let label:any = document.createElement("h2");
  label.innerText = value;
  label.className = "p-Widget jp-Dialog-header";
  button.setAttribute('type', "button");
  button.className = "form-check-input";
  button.style["margin-top"] = "20px";
  div.className = "p-Widget jp-Input-Dialog jp-Dialog-body form-check";
  div.appendChild(button);
  div.appendChild(label);
  button.onclick(getsetting(value));
  return div;
}

function getsetting(value:string){
  if (value == "Set Default options for commit"){
    setDefault();
    closeWindow();
  };
  if (value == "Clear the API key"){
    NBKernel.execute("import jovian as jvn\njvn.utils.credentials.purge_creds()").then(
      ()=>closeWindow()
    );
  };
  if (value == "Change the API key"){
    NBKernel.execute("import jovian as jvn\njvn.utils.credentials.purge_creds()").then(
      ()=>askAPIKeys()
    );
    closeWindow();
  };
  if (value == "Disable the extension"){
    NBKernel.execute("import os\nos.system('jupyter labextension disable Jovian')").then(
      ()=>{
        alert("You have disabled the Jovian extension, please refresh your browser.");
        closeWindow();
      }
    );
  };
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