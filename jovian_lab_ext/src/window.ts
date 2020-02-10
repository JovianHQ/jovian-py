let body:any;

function askParameters():HTMLElement{
    let header:HTMLElement = initialHeader();
    header.appendChild(addText("File Name:"));
    header.appendChild(addInput());
    header.appendChild(addText("Private or not?"));
    header.appendChild(addInput());
    header.appendChild(addButtons());
    return body;
}


function addText(title:string):HTMLElement{
    let text:HTMLSpanElement = document.createElement("span");
    text.className = "p-Widget jp-Dialog-header";
    text.innerText = title;
    (<any>text.style)["margin-top"] = "0.5em";
    return text;
}

function addInput(dValue:string = ""):HTMLElement{
    let div:HTMLElement = document.createElement("div");
    let inp:HTMLInputElement = document.createElement("input");
    div.className = "p-Widget jp-Input-Dialog jp-Dialog-body";
    inp.className = "jp-mod-styled";
    inp.type = "text";
    inp.defaultValue = dValue;
    div.appendChild(inp);
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
    cancle.innerText = "testing";
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