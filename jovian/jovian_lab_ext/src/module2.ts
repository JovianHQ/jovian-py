import NBKernel from './NBKernel';

let body:any;

function askParameters():void{
  let header:HTMLElement = initialHeader();
  (header as any).style["max-height"] = "1000px";
  header.appendChild(createSecretNB());
  header.appendChild(fileName());
  header.appendChild(additionalScripts());
  header.appendChild(toCaptrue());
  header.appendChild(whichEnv());
  header.appendChild(base64Id());
  header.appendChild(newNB());
  header.appendChild(artifacts());
  header.appendChild(addButtons("Commit"));
  openWindow();
}

function commit(jvn_params:any = null):void {
  let commit:string = "\tcommit()\n";
  if (jvn_params != null){
    
  }
  getAPIKeys().then(
    (result) => {
      if (result == true){
        const jvn_commit =
          "from jovian import commit\n" +
          "import io\n" +
          "from contextlib import redirect_stdout\n" +
          "f = io.StringIO()\n" +
          "with redirect_stdout(f):\n" +
          commit +
          "out = f.getvalue().splitlines()[-1]\n" +
          "if(out.split()[1] == 'Committed'):\n" +
          "\tprint(out.split()[-1])\n" +
          "else:\n" +
          "\tprint(out)";
        NBKernel.execute(jvn_commit).then(
          (result) => {
            committedWindow((result as string).trim());
          }
        );
      } else {
        askAPIKeys();
      }
    }
  );
}

function askAPIKeys():void {
  let header:HTMLElement = initialHeader();
  let div:HTMLElement = document.createElement("div");
  let span:HTMLElement = addText("Please enter your API key from ");
  let a:HTMLElement = addLink("Jovian", "https://jovian.ml");
  let input:HTMLElement = addInput();
  span.appendChild(a);
  div.className = "jvn_API_Keys";
  div.appendChild(span);
  div.appendChild(input);
  header.appendChild(div);
  header.appendChild(addButtons("Save", ()=>{
    setAPIKeys(getInputText(input));
  }));
  openWindow();
}

function setAPIKeys(value:string):void {
  const api_key = value;
  const write_api =
    "from jovian.utils.credentials import write_api_key\n" +
    "write_api_key('" +
    api_key +
    "')\n";
  NBKernel.execute(write_api).then(
    ()=>{
      alert("Congrats! You have saved a valid API key, now you can commit directly from the Commit toolbar button");
      closeWindow();
    }
  );
}

function committedWindow(url:string):void {
  let header:HTMLElement = initialHeader();
  let div:HTMLElement = document.createElement("div");
  if (url.startsWith("https://")) {
    let label = addText("Committed Successfully!");
    let nb_link = addLink(url,url);
    div.appendChild(label);
    div.appendChild(document.createElement("br"));
    div.appendChild(document.createElement("br"));
    div.appendChild(nb_link);
  } else {
    let label = addText("Commit failed! " + url);
    div.appendChild(label);
  }
  header.appendChild(div);
  header.appendChild(addButtons(null));
  openWindow();
}

async function getAPIKeys() {
  const validate_api =
    "from jovian.utils.credentials import validate_api_key\n" +
    "from jovian.utils.credentials import read_api_key_opt, creds_exist\n" +
    "key_status = 'nil'\n" +
    "if creds_exist():\n" +
    "\tcurrent_key, _ = read_api_key_opt()\n" +
    "\tif(validate_api_key(current_key)):\n" +
    '\t\tkey_status = "valid"\n' +
    "\telse:\n" +
    '\t\tkey_status = "invalid"\n' +
    "print(key_status)\n";
  return new Promise((res) => {
    NBKernel.execute(validate_api).then(
      (result) => {
        if ((result as string).trim() == "valid"){
          res(true);
        } else {
          res(false);
        }
      }
    )
  });
}

function createSecretNB():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.className = "jvn_params_secrete";
  div.appendChild(addText("Create a secret notebook?"));
  div.appendChild(addTrueOrFalse());
  return div;
}

function fileName():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.className = "jvn_params_nbName";
  div.appendChild(addText("The filename of the jupyter notebook"));
  div.appendChild(addInput());
  return div;
}

function additionalScripts():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.className = "jvn_params_additions";
  div.appendChild(addText("Any additional scripts(.py files), CSVs that are required to run the notebook."));
  div.appendChild(addInput());
  return div;
}

function toCaptrue():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.className = "jvn_params_caps";
  div.appendChild(addText("To capture and and upload Python environment along with the notebook?"));
  div.appendChild(addTrueOrFalse());
  return div;
}

function whichEnv():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.className = "jvn_params_env";
  div.appendChild(addText("Which type of environment to be captured?"));
  div.appendChild(addEnvs());
  return div;
}

function base64Id():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.className = "jvn_params_base64Id";
  div.appendChild(addText("To provide the base64 ID(present in the URL) of an notebook hosted on Jovian?"));
  div.appendChild(addInput());
  return div;
}

function newNB():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.className = "jvn_params_new";
  div.appendChild(addText("To create a new notebook?"));
  div.appendChild(addTrueOrFalse());
  return div;
}

function artifacts():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.className = "jvn_params_base64Id";
  div.appendChild(addText("Any outputs files or artifacts generated from the modeling processing?"));
  div.appendChild(addInput());
  return div;
}

/* *******************************************************
 *
 * Start here will all be helper functions:
 *
 * ******************************************************/

function addText(title:string):HTMLElement{
  let text:HTMLSpanElement = document.createElement("span");
  text.className = "p-Widget jp-Dialog-header";
  text.innerText = title;
  (<any>text.style)["margin-top"] = "0.5em";
  return text;
}

function addInput(dValue:string = ""):HTMLElement{
  let div:HTMLElement = document.createElement("div");
  let div1:HTMLElement = document.createElement("div");
  let inp:HTMLInputElement = document.createElement("input");
  div.className = "p-Widget jp-Input-Dialog jp-Dialog-body";
  div1.className = "jp-select-wrapper";
  inp.className = "jp-mod-styled";
  inp.type = "text";
  inp.defaultValue = dValue;
  div.appendChild(div1);
  div1.appendChild(inp);
  return div;
}

function getInputText(input:HTMLElement):string{
  let text:string = input.getElementsByTagName("input")[0].value;
  //let text:string = (input.firstElementChild.firstElementChild as HTMLInputElement).value;
  return text.trim();
}

function addTrueOrFalse(dValue:string = ""):HTMLElement{
  let div:HTMLElement = document.createElement("div");
  let div1:HTMLElement = document.createElement("div");
  let selection:any = document.createElement("select");
  let isTrue:any = document.createElement("option");
  let isFalse:any = document.createElement("option");
  div.className = "p-Widget jp-Input-Dialog jp-Dialog-body";
  div1.className = "jp-select-wrapper";
  selection.className = "jp-mod-styled";
  isTrue.value = "isTrue";
  isFalse.value = "isFalse";
  isTrue.innerText = "True";
  isFalse.innerText = "False";
  div.appendChild(div1);
  div1.appendChild(selection);
  selection.appendChild(isTrue);
  selection.appendChild(isFalse);
  return div;
}

function addLink(text:string, link:string):HTMLElement{
  let a:HTMLElement = document.createElement("a");
  a.setAttribute('href', link);
  a.setAttribute("target", "_blank")
  a.style.color = "rgb(27, 87, 177)";
  a.innerText = text;
  return a;
}

function addEnvs():HTMLElement{
  let div:HTMLElement = document.createElement("div");
  let div1:HTMLElement = document.createElement("div");
  let selection:any = document.createElement("select");
  let isTrue:any = document.createElement("option");
  let isFalse:any = document.createElement("option");
  div.className = "p-Widget jp-Input-Dialog jp-Dialog-body";
  div1.className = "jp-select-wrapper";
  selection.className = "jp-mod-styled";
  isTrue.value = "isConda";
  isFalse.value = "isPip";
  isTrue.innerText = "conda";
  isFalse.innerText = "pip";
  div.appendChild(div1);
  div1.appendChild(selection);
  selection.appendChild(isTrue);
  selection.appendChild(isFalse);
  return div;
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

function initialHeader():HTMLElement{
  let header:HTMLElement = document.createElement("div");
  let subHeader:HTMLElement = document.createElement("div");
  header.className = "p-Widget jp-Dialog";
  subHeader.className = "p-Widget p-Panel jp-Dialog-content";
  header.appendChild(subHeader);
  body = header;
  return subHeader;
}

function openWindow():void {
  insertAfter(body, document.getElementById("main"));
}

function closeWindow():void {
  body.parentNode.removeChild(body);
}

function insertAfter (newNode:any, referenceNode:any):void {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

export { askParameters, commit };