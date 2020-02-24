import NBKernel from './NBKernel';

let body:any;
let lock:boolean = false;

async function askParameters():Promise<void>{
  let header:HTMLElement = initialHeader();
  (header as any).style["max-height"] = "1000px";
  (header as any).style["font-size"] = "11px";
  (header as any).style["top"] = "-43px";
  let params = {
    message: message(),
    filename: filename(),
    files: files(),
    environment: environment(),
    new_project: new_project(),
    project_id: project_id(),
    privacy: privacy(),
    outputs: outputs(),
    git_commit: git_commit(),
    git_message: git_message()
  }
  header.appendChild(params.message);
  header.appendChild(params.filename);
  header.appendChild(params.files);
  header.appendChild(params.environment);
  header.appendChild(params.new_project);
  header.appendChild(params.project_id);
  header.appendChild(params.privacy);
  header.appendChild(params.outputs);
  header.appendChild(params.git_commit);
  header.appendChild(params.git_message);
  header.appendChild(addButtons("Commit",()=>commitWithParams(params)));
  await setParameters(params);
  openWindow();
}

async function setParameters(htmlParams:any):Promise<void> {
  let project_id_helper = async ()=> {
    let params = getParams();
    if (params != null && params.project_id.length != 0) {
      setInputText(htmlParams.project_id, params.project_id);
      return;
    }
    await getProjectTitle().then(t => {
      if(t != undefined){
        setInputText(htmlParams.project_id, t);
      }
    });
  };
  let params = getParams();
  if (params != null) {
    setInputText(htmlParams.message, params.message);
    setInputText(htmlParams.filename, params.filename);
    setInputText(htmlParams.files, params.files);
    setEnvs(htmlParams.environment, params.environment);
    await project_id_helper();
    setTrueOrFalse(htmlParams.new_project, params.new_project == "True" ? true : false);
    setPrivacy(htmlParams.privacy, params.privacy);
    setInputText(htmlParams.outputs, params.outputs);
    setTrueOrFalse(htmlParams.git_commit, params.git_commit == "True" ? true : false);
    setInputText(htmlParams.git_message, params.git_message);
  } else {
    setInputText(htmlParams.filename, NBKernel.currentNotebookName().replace(".ipynb", ""));
    setTrueOrFalse(htmlParams.new_project, false);
    setTrueOrFalse(htmlParams.git_commit, true);
    setEnvs(htmlParams.environment, "auto");
    setPrivacy(htmlParams.privacy, "auto");
  }
  let show = (target:HTMLElement, list:[{element:HTMLElement, show:boolean}]) => {
    list.forEach(e => {
      if (getTrueOrFalse(target) == "True") {
        if (e.show) {
          disable(e.element, false);
        } else {
          disable(e.element);
        }
      } else {
        if (e.show) {
          disable(e.element);
        } else {
          disable(e.element, false);
        }
      }
    });
  };
  show(htmlParams.new_project, [{element:htmlParams.project_id, show:false}]);
  htmlParams.new_project.onchange = async ()=> {
    await project_id_helper();
    show(htmlParams.new_project, [{element:htmlParams.project_id, show:false}]);
  };
}

function setDefault():void{
  //same as askParameters but set parameters to defaults values
  clearParams();
  askParameters();
}

function commitWithParams(params:any):void {
  closeWindow();
  let filename:string[] = NBKernel.currentNotebookName().split(".");
  filename.pop();
  filename.join();
  let jvn_params = {
    message: getInputText(params.message),
    filename: filename,
    files: getInputText(params.files),
    environment: getEnvs(params.environment),
    new_project: getTrueOrFalse(params.new_project),
    project_id: getInputText(params.project_id),
    privacy: getPrivacy(params.privacy),
    outputs: getInputText(params.outputs),
    git_commit: getTrueOrFalse(params.git_commit),
    git_message: getInputText(params.git_message)
  }
  storeParams(jvn_params);
  commit(getFinalCommit(jvn_params));
}

function getFinalCommit(params:any = null):string {
  if (params == null){
    params = getParams();
  }
  const filename:string = getValInPython(params.filename);
  const new_project = params.new_project;
  const git_commit = params.git_commit;
  const files = getArrayInPython(params.files);
  const outputs = getArrayInPython(params.outputs);
  const privacy = getValInPython(params.privacy);
  const environment = getValInPython(params.environment);
  const project_id = getValInPython(params.project_id);
  const message = getValInPython(params.message);
  const git_message = getValInPython(params.git_message);
  const commit =
    "commit(" +
    "filename=" +
    filename +
    ",message=" +
    message +
    ",git_commit=" +
    git_commit +
    ",git_message=" +
    git_message +
    ",privacy=" +
    privacy +
    ",new_project=" +
    new_project +
    ",files=" +
    files +
    ",project=" +
    project_id +
    ",outputs=" +
    outputs +
    ",environment=" +
    environment +
    ")\n";
  return commit;
}

function getProjectTitle():Promise<string> {
  return new Promise(resolve => {
    const code =
      "from jovian.utils.commit import _parse_project as p\n" +
      "a = p(project=None, new_project=None, filename=None)\n" +
      "print(a[0])";
    NBKernel.execute(code).then(
      data => {
        let ms = data
          .trim()
          .replace(/.*?\"/, "")
          .split('"')
          .shift();
        if (ms.toLowerCase() == "none") {
          resolve(undefined);
        }
        resolve(ms);
      }
    );
  });
}

function storeParams(params:any):void {
  // This function will be used to stored
  // the settings of parameters
  localStorage.setItem(
    NBKernel.currentNotebookName(),
    JSON.stringify(params)
  );
}

function getParams():any {
  // get parameter settings from current notebook
  return JSON.parse(localStorage.getItem(NBKernel.currentNotebookName()));
}

function clearParams():void {
  localStorage.removeItem(NBKernel.currentNotebookName());
}

async function commit(commitWithParams:string|null = null):Promise<void> {
  let commit:string = "\tcommit()\n";
  if (lock == true) {
    return;
  }
  if (commitWithParams != null){
    commit = "\t" + commitWithParams.trim() + "\n";
  } else {
    commit = "\t" + getFinalCommit().trim() + "\n";
  }
  lock = true;
  getAPIKeys().then(
    async (result) => {
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
        await NBKernel.execute(jvn_commit).then(
          (result) => {
            committedWindow((result as string).trim());
          }
        );
      } else {
        askAPIKeys();
      }
      lock = false;
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

function message():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.appendChild(addText("A short message to be used as the title for this version"));
  div.appendChild(addInput());
  return div;
}

function filename():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  let inp:HTMLElement = addInput();
  disable(inp);
  div.appendChild(addText("The filename of the jupyter notebook"));
  div.appendChild(inp);
  return div;
}

function files():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.appendChild(addText("Any additional scripts(*.py/*.csv) such as `utils.py, inputs.csv`"));
  div.appendChild(addInput("utils.py, inputs.csv"));
  return div;
}

function environment():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.appendChild(addText("Which type of environment to be captured?"));
  div.appendChild(addEnvs());
  return div;
}

function new_project():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.appendChild(addText("To create a new project?"));
  div.appendChild(addTrueOrFalse());
  return div;
}

function project_id():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.appendChild(addText("Name of the Jovian.ml project like `user_name_on_jovian/notebook_name`"));
  div.appendChild(addInput());
  return div;
}

function privacy():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.appendChild(addText("Notebook privacy settings (applicable while creating a new notebook project)"));
  div.appendChild(addPrivacy());
  return div;
}

function outputs():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.appendChild(addText("Any outputs files or artifacts generated from the modeling processing such as `submission.csv, weights.h5`"));
  div.appendChild(addInput("submission.csv, weights.h5"));
  return div;
}

function git_commit():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.appendChild(addText("To perform a Git commit? (only when the notebook is inside a Git repository)"));
  div.appendChild(addTrueOrFalse());
  return div;
}

function git_message():HTMLElement {
  let div:HTMLElement = document.createElement("div");
  div.appendChild(addText("Commit message for git"));
  div.appendChild(addInput());
  return div;
}

/* *******************************************************
 *
 * Start here will all be helper functions:
 *
 * ******************************************************/

function disable(inp:HTMLElement, dis:boolean = true):void {
  let element:any = null;
  if (inp.getElementsByTagName("input").length != 0) {
    element = inp.getElementsByTagName("input")[0];
  } else if (inp.getElementsByTagName("select").length != 0){
    element = inp.getElementsByTagName("select")[0];
  }
  if (element != null){
    element.disabled = dis;
    if (dis){
      element.style["color"] = "grey";
    } else {
      element.style["color"] = "";
    }
  }
  if (dis && inp.getElementsByTagName("input").length != 0){
    setInputText(inp,"");
  }
}

function addText(title:string):HTMLElement{
  let text:HTMLSpanElement = document.createElement("span");
  text.className = "p-Widget jp-Dialog-header";
  text.innerText = title;
  (<any>text.style)["margin-top"] = "0.5em";
  return text;
}

function addInput(placeHolder:string = ""):HTMLElement{
  let div:HTMLElement = document.createElement("div");
  let div1:HTMLElement = document.createElement("div");
  let inp:HTMLInputElement = document.createElement("input");
  div.className = "p-Widget jp-Input-Dialog jp-Dialog-body";
  div1.className = "jp-select-wrapper";
  inp.className = "jp-mod-styled";
  inp.type = "text";
  inp.placeholder = placeHolder;
  div.appendChild(div1);
  div1.appendChild(inp);
  return div;
}

function getInputText(input:HTMLElement):string{
  let text:string = input.getElementsByTagName("input")[0].value;
  return text.trim();
}

function setInputText(input:HTMLElement, value:string):void{
  input.getElementsByTagName("input")[0].value = value;
}

function addTrueOrFalse():HTMLElement{
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

function getTrueOrFalse(input:HTMLElement):string{
  let text:string = getSelection(input);
  if (text == "isTrue"){
    return "True";
  }
  return "False";
}

function setTrueOrFalse(input:HTMLElement, isTrue:boolean):void{
  if (isTrue){
    setSelection(input,"isTrue");
  } else {
    setSelection(input,"isFalse");
  }
}

function getSelection(input:HTMLElement):string{
  let text:string = input.getElementsByTagName("select")[0].value;
  return text.trim();
}

function setSelection(input:HTMLElement, value:string):void{
  input.getElementsByTagName("select")[0].value = value;
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
  let isConda:any = document.createElement("option");
  let isPip:any = document.createElement("option");
  let isAuto:any = document.createElement("option");
  let isNone:any = document.createElement("option");
  div.className = "p-Widget jp-Input-Dialog jp-Dialog-body";
  div1.className = "jp-select-wrapper";
  selection.className = "jp-mod-styled";
  isConda.value = "isConda";
  isPip.value = "isPip";
  isAuto.value = "isAuto";
  isNone.value = "isNone";
  isConda.innerText = "conda";
  isPip.innerText = "pip";
  isAuto.innerText = "auto";
  isNone.innerText = "None";
  div.appendChild(div1);
  div1.appendChild(selection);
  selection.appendChild(isAuto);
  selection.appendChild(isConda);
  selection.appendChild(isPip);
  selection.appendChild(isNone);
  return div;
}

function getEnvs(input:HTMLElement):string{
  let text:string = getSelection(input);
  if (text == "isConda"){
    return "conda";
  } else if (text == "isPip"){
    return "pip";
  } else if (text == "isNone"){
    return "None";
  }
  return "auto";
}

function setEnvs(input:HTMLElement, value:string):void{
  if (value.toLowerCase() == "conda"){
    setSelection(input,"isConda");
  } else if (value.toLowerCase() == "pip"){
    setSelection(input,"isPip");
  } else if (value.toLowerCase() == "none"){
    setSelection(input,"isNone");
  } else {
    setSelection(input,"isAuto");
  }
}

function addPrivacy():HTMLElement{
  let div:HTMLElement = document.createElement("div");
  let div1:HTMLElement = document.createElement("div");
  let selection:any = document.createElement("select");
  let isSecret:any = document.createElement("option");
  let isPublic:any = document.createElement("option");
  let isPrivate:any = document.createElement("option");
  let isAuto:any = document.createElement("option");
  div.className = "p-Widget jp-Input-Dialog jp-Dialog-body";
  div1.className = "jp-select-wrapper";
  selection.className = "jp-mod-styled";
  isSecret.value = "isSecret";
  isPublic.value = "isPublic";
  isAuto.value = "isAuto";
  isPrivate.value = "isPrivate";
  isSecret.innerText = "secret";
  isPublic.innerText = "public";
  isAuto.innerText = "auto";
  isPrivate.innerText = "private";
  div.appendChild(div1);
  div1.appendChild(selection);
  selection.appendChild(isAuto);
  selection.appendChild(isPublic);
  selection.appendChild(isSecret);
  selection.appendChild(isPrivate);
  return div;
}

function getPrivacy(input:HTMLElement):string{
  let text:string = getSelection(input);
  if (text == "isPublic"){
    return "public";
  } else if (text == "isSecret"){
    return "secret";
  } else if (text == "isPrivate"){
    return "private";
  }
  return "auto";
}

function setPrivacy(input:HTMLElement, value:string):void{
  if (value.toLowerCase() == "public"){
    setSelection(input,"isPublic");
  } else if (value.toLowerCase() == "secret"){
    setSelection(input,"isSecret");
  } else if (value.toLowerCase() == "private"){
    setSelection(input,"isPrivate");
  } else {
    setSelection(input,"isAuto");
  }
}

function addButtons(name:string|null, callBack = ()=>{}):HTMLElement{
  let footer:HTMLElement = document.createElement("div");
  let icon1:HTMLElement = document.createElement("div");
  let icon2:HTMLElement = document.createElement("div");
  let cancel:HTMLElement = document.createElement("div");
  let ok:HTMLElement = document.createElement("div");
  let cancelBut:HTMLElement = document.createElement("button");
  let okBut:HTMLElement = document.createElement("button");
  footer.className = "p-Widget jp-Dialog-footer";
  icon1.className = "jp-Dialog-buttonIcon";
  icon2.className = "jp-Dialog-buttonIcon";
  cancel.className = "jp-Dialog-buttonLabel";
  ok.className = "jp-Dialog-buttonLabel";
  cancelBut.className = "jp-Dialog-button jp-mod-reject jp-mod-styled";
  okBut.className = "jp-Dialog-button jp-mod-accept jp-mod-styled";
  cancel.innerText = "Close";
  cancelBut.appendChild(icon1);
  cancelBut.appendChild(cancel);
  footer.appendChild(cancelBut);
  (<any>cancelBut).onclick = ()=>{
    closeWindow();
  };
  if (name!=null){
    cancel.innerText = "Cancel";
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

function getArrayInPython(arrInString:string):string {
  // Helper function; which use to format a string
  // that can be used in commit() array arguments
  // such as outputs and files
  const arr =
    "[" +
    arrInString
      .split(",")
      .map(e => "'" + e.trim() + "'")
      .join(",") +
    "]";
  if (arr == "['']") {
    return "None";
  }
  return arr;
}

function getValInPython(val:string):string {
  // Helper function; which use to format a string
  // that can be used in commit() string arguments
  if (val === "") {
    return "None";
  }
  return '"' + val + '"';
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

export { askParameters, commit, setDefault, askAPIKeys };