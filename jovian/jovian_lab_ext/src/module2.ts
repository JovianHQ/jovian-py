let body:any;

function askParameters():HTMLElement{
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
    header.appendChild(addButtons());
    return body;
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

// version 2
// function createSecretNB():HTMLElement{
//     let div:HTMLElement = document.createElement("div");
//     let span:any = document.createElement("span");
//     let div1:HTMLElement = document.createElement("div");
//     let checkBox:any = document.createElement("input");
//     div.className = "p-Widget jp-Input-Dialog jp-Dialog-body";
//     span.className = "p-Widget jp-Dialog-header";
//     div1.className = "jp-select-wrapper";
//     checkBox.className = "jp-mod-styled";
//     span.innerText = "Create a secret notebook?";
//     checkBox.type = "checkbox";
//     div.appendChild(span);
//     div.appendChild(div1);
//     div1.appendChild(checkBox);
//     return div;
// }


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

function addEnvs(dValue:string = ""):HTMLElement{
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

function addButtons():HTMLElement{
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
    ok.innerText = "Summit";
    cancle.innerText = "Cancle";
    cancleBut.appendChild(icon1);
    cancleBut.appendChild(cancle);
    okBut.appendChild(icon2);
    okBut.appendChild(ok);
    footer.appendChild(cancleBut);
    footer.appendChild(okBut);
    (<any>cancleBut).onclick = ()=>{
        body.parentNode.removeChild(body);
    };
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

export default askParameters;