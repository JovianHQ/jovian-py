let body:any;

function askParameters():HTMLElement{
    let header:HTMLElement = initialHeader();
    (header as any).style["max-height"] = "1000px";
    header.appendChild(createSD());
    header.appendChild(breakN());//
    header.appendChild(addButtonFB());
    header.appendChild(breakN());//
    header.appendChild(addButtonTW());
    header.appendChild(breakN());//
    header.appendChild(addButtonIN());
    header.appendChild(breakN());//
    header.appendChild(addButtonCL());
    header.appendChild(addButtons());
    return body;
}

//<div id='fb-root'></div><script async defer crossorigin='anonymous' src='https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v5.0'></script><div class='fb-share-button' data-href='https://jovian.ml' data-layout='button_count' data-size='large'><a target='_blank' href='https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fjovian.ml%2F&amp;src=sdkpreparse' class='fb-xfbml-parse-ignore'></a></div>
function breakN():HTMLElement {
    let div:HTMLElement = document.createElement("BR");
    //div.className = "jvn_params_secrete";
    //div.appendChild(addText("   "));
    //div.style.alignSelf = 'center';
    //div.appendChild(addTrueOrFalse());
    return div;
}



function createSD():HTMLElement {
    let div:HTMLElement = document.createElement("div");
    div.className = "jvn_params_secrete";
    div.appendChild(addText("Share Dialogue"));
    div.style.alignSelf = 'center';
    //div.appendChild(addTrueOrFalse());
    return div;
}

function addButtonFB():HTMLElement{
    let div:HTMLElement = document.createElement("div");
    let icon1:HTMLElement = document.createElement("div");
    let cancle:HTMLElement = document.createElement("div");
    let FBBut:HTMLElement = document.createElement("button");
    FBBut.style.width = '50px';
    FBBut.style.height = '50px';
    FBBut.style.background =
    "white url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAb1BMVEVCZ7L///+5w95GarM2YK80Xq+pttc+ZbFfe7s6YrCHmsmZqdA8Y7Ds8PdSdLlffr3V3OyQpNFrh8Lg5vIvW633+fyCmsxKb7fG0eier9WtutnAy+Ta4e91jsR8k8eMn8zP1ulvh8Dx9PkmVqvo7ff2SOu1AAAEYklEQVR4nO3da3uqOBSG4YDBmDYkHEStp1qn//83jqfuvWemoxGarBWu9/myP9XNfS0sIJGK7FpZ1Y0VY8k2dVXeZOL6T+6kNtTb9YMZLV3+h7B1cky8a0a69ktYWU29OUHStroKWzu+AV4ztr0I3TgneE67szCX1NsRMJlnonRj3UfPGVeKaswjPA2xEvV434XndC2aMe+kp920EeM5Vfu+sfsQQgghhBBCCCGEEPJJKWOM1lpKfc5cUkoo6g37mbQshG12+8XLe/1+6mWx3+8+GjezSyXnRXESq1SpyuhiPlmsq21bHrvudrc667ruWJafn227rQ6b9euisUWStySUFM3r6pfrfq/pEc18Oa2OfryzMLW7Lnry4Tu9JGeoin31DC+1GSrjDk/NL7UZmsn0aV9SM5R2+7wvoRmq4q3HABMSnoC9fMnspWqy6glMZIbKbPoCU5lhf2AaMyym/YFJzFDXA4ApzNA0/qfZSc5QyWfPRFOboR7yJkxBaNygfTSBvXTe+1CfyAyNGwjkPkOlhv2a4T9Ds+t3QZHODE0+FMh8hmo5eITMZygHna+lMEPZ63OLhITGlY8FD4Wc91LZ95OLfwgZz1ANufD9LWQ8Q2U/f0LIeIZm9gSk267y9Xo9/XfrD8bfFtELX95xs58tJ0rLb2IMFIXnCU05nRQmyRvbc7+jYTXTCeIuSa9r343ivB/eb+kjLJfpAk3jc9q9Y3wweJTZewhXyS4nEZ4XFu8Jj1Do18fA0iY8Qq/z7kNBvZVD8rkfM01aKNceb0PGFw6P8zlpS/tL2D7C2eiFSf8q9RIuqTdyUD7CCfVGDgpCCPkHIYT8gxBC/kEIIf8ghJB/EELIv1EI1Xc33r/6y0NoinuvcIr4E2Pl/rt24o88bnLf+/FLb7RE/fLYMLDP+diFK9pbNxGEa9o7qBGExKvaIghfxi7sdrQ3p8ILqR9FHl7YEt9+Cy+sJmMXHoiX24QX5sRrNcIL30Y/wz3xSobwQuq/WxFeSOuLIOxor50iCNvRCzfUC/uCC8mXLgYX1tQriIMLqQ+HwYUd+eLM0MLSUS9dDC3cki/ODC08EF8dhhduqN+GwYXEH5ZGENJ/BTiwsCM/HAYXkh8OQwuP9OvcQwupz7uDC7fUV4cn4XtQIfG9w3Nq6Wb/n/V4ZsS9n59x+LuG6l5zj5UKwtx5AWrdw0ax2uRuEELIPwgh5B+EEPIPQgj5ByGE/IMQQv5BCCH/IISQfxBCyD8IIeQfhBDyD0II+QchhPyDEEL+QQgh/yCEkH8QQsg/CCHkH4QQ8g9CCPkHIYT8gxBC/kEIIf8g/EEh0bMJogmtIHrMSyyhaURN8zCiWEJdi4rmgVKxhLISRA82jyQ0rhRZTjLESEKZZyLrHMU7MY5Qu+wkzFpLsJ9GERrbXoRZZeNPMYZQ2yq7CrPWydhjDC800rXZlzDrcid1VGRgodHS3f4HcXu1sqqbmCdwYYW2qavy9ip/A3YKUMidEST2AAAAAElFTkSuQmCC') no-repeat 5px / 50px 50px";//15px 17px
    //body.className = "p-Widget jp-Dialog-footer";
    body.className = "fa fa-bookmark-o";
    icon1.className = "jp-Dialog-buttonIcon";
    cancle.className = "jp-Dialog-buttonLabel";
    FBBut.className = "jp-Dialog-button jp-mod-reject jp-mod-styled";
    //cancle.innerText = "Cancle";
    cancle.innerText = "";
    FBBut.appendChild(icon1);
    FBBut.appendChild(cancle);
    div.appendChild(FBBut);
    (<any>FBBut).onclick = ()=>{
        body.parentNode.removeChild(body);
    };
    return div;
}

function addButtonTW():HTMLElement{
    let div:HTMLElement = document.createElement("div");
    let icon1:HTMLElement = document.createElement("div");
    let cancle:HTMLElement = document.createElement("div");
    let TWBut:HTMLElement = document.createElement("button");
    TWBut.style.width = '50px';
    TWBut.style.height = '50px';
    TWBut.style.background =
    "white url('data:image/png;base64,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') no-repeat 5px / 50px 50px";
    //body.className = "p-Widget jp-Dialog-footer";
    body.className = "fa fa-bookmark-o"
    icon1.className = "jp-Dialog-buttonIcon";
    cancle.className = "jp-Dialog-buttonLabel";
    TWBut.className = "jp-Dialog-button jp-mod-reject jp-mod-styled";
    //cancle.innerText = "Cancle";
    cancle.innerText = "";
    TWBut.appendChild(icon1);
    TWBut.appendChild(cancle);
    div.appendChild(TWBut);
    (<any>TWBut).onclick = ()=>{
        body.parentNode.removeChild(body);
    };
    return div;
}

function addButtonIN():HTMLElement{
    let div:HTMLElement = document.createElement("div");
    let icon1:HTMLElement = document.createElement("div");
    let cancle:HTMLElement = document.createElement("div");
    let INBut:HTMLElement = document.createElement("button");
    INBut.style.width = '50px';
    INBut.style.height = '50px';
    INBut.style.background =
    "white url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASIAAACuCAMAAAClZfCTAAAAkFBMVEUCdLP////S4O0Aaq7t8fY3f7gAdLIAZa0AaK3L2+o6drMAb7GVsNIAaq0Ac7QAbbCNsNEAY6zY4+3t8fTH1eY0erf5/P3j6/L09vm4y+B9osvS4e10mcajvtnC1uYldrRjlcJGhLylwNqCqM2WtNNNir2qx94uc7Szx99vnshbj8BTiL4AXaglebSVuNSetdS2GV8jAAAE10lEQVR4nO2ciVrqOhRGW1LacIo7UIYWZR7k6hl8/7e7HfAydScev3hL5F/qp0jBdpnsjLueBwAAAAAAAAAAAAAAAAAAAIA1KP8kFfX7UlH1EJxCxYdcTGfzJJnPpgsZN31GNwdRGC2HY//AeLiMPC9s+qxui3jU8c/ojFCQjpAXisexf8mLbPrEbocwN3QlKGcjEbMPkKo15PuPCg2bVwRqj9r1hnx/RVBUQFHCKUpE0yd3E1DMVLOyqqEYFRVNsIXI99N+0+d3E6x4Q77/s+mzuwEo7ukUbVXTJ3gDRHOdohb6j57XT3WKUrRpuaJApyjDSM0Lo0yraE/oYesrWiBgKOy3dIoShGvy1FqnaAJFuaSlTtH07qtZMdBXmiZtjDa/QM14RWuBCeyCPdvsjxcY6ZeoDaeoixHaATmpNzSM0CmqIFJPdYZasUcIRQdIdK4NzRWK0AkUbS8j9RbrsSfkpSUU7bOANGljgegauei2gnFefoJOb4HRaw15pVKRGK1WP0QUl91ucAlVW4yokEVQxHAIz7ADAPh+ILKZwDCPI+89xEJGUkqhYvoOK021/+rQO780TV+JTn8ISYn97vHtedhpDefPs+50txci9qpul5PIiOF85jq/Ou7A44COik767i25mMnMkn+WKnK2R6omHYb12awj0e9W/XFPL8crV/set14wXKo4dNKRZOeuny4WQNhNkb13lyqeXW9PPpJuZBmXXPMk2VWi1kVNMyqSG+0OgULSq3ROkEVF8UK7+H3g2cGJFhuK4mJW7qepCFUkpU+nukt2FNGDZuftOcHCtWJkR1F9kgTjSDnWQbKiSE0/bqjc8353ilRb19Zfs3ZrU44NRb+0e91qeL23UrS5XIYzEkQNXe2nsKBo8rHm/pSNS3txLSj6BIPYoZ5RM4qcylJqSFHSd2fU35Aif+ROTWtK0dadvaZNKXJo23tTisajhi7472lKkf/iTJtmXVEWpOngA53JmQodidhWFWXraXsvpFCLXdc0bnuSrqzVWlSUTvuCqrkg8uL+q15S5kxugD1Fs4f/Bl6lplhpE2/9366sZltTtInobF2WTMnJr//7tX4SW4rerpd/KBS61NtHNyJRrmhgRVHSr4m9pE13++NKjoklRav6IsHftKXMmXSjHNmpaMP6G0JRzOYp+X7HlalHO4qYyWjyFP+a5K4UBcywnXQ1LZX31OjzqdiaxNLAlbG+FUUv3LsT8YuQmSu5OFYUjZh9n3kHcqdR5IYhK4p0w60Ru1DrzE1bbChK+baJNBnc+6++NkvY6Dq2NLfJ5O+VML6nUjTRTNULfkrkxx3ForVmtCVq87crRXfUL5pBUYlG0ZsmqkBRSVej6IHfRwtFFVAERSdAERSxQJERKDICRUagyAgUGYEiI1BkBIqMfLUiAUVQdASKoIgF4doIFBmBIiNQZASKjECRESgyAkVGoMgIFBmBIiNQZASKjNjYyAdFFVAERSyIRUagyAgUGYEiI1BkBIqMNKnoiy/NFryi8/tdh/z9rv3tJ7emO5IDIpLgnUEwGORfQfEtZ3ietkDtrHi6eL48+P3BIMh6GkVqWL318S+Uryt+4UopIiEZHi5uMETcgVLpggr7/sKRQgQAAAAAAAAAAAAAAAAAAAAA+P78C6DvYQRnRttfAAAAAElFTkSuQmCC') no-repeat 5px / 50px 50px";
    //body.className = "p-Widget jp-Dialog-footer";
    body.className = "fa fa-bookmark-o"
    icon1.className = "jp-Dialog-buttonIcon";
    cancle.className = "jp-Dialog-buttonLabel";
    INBut.className = "jp-Dialog-button jp-mod-reject jp-mod-styled";
    //cancle.innerText = "Cancle";
    cancle.innerText = "";
    INBut.appendChild(icon1);
    INBut.appendChild(cancle);
    div.appendChild(INBut);
    (<any>INBut).onclick = ()=>{
        body.parentNode.removeChild(body);
    };
    return div;
}

function addButtonCL():HTMLElement{
    let div:HTMLElement = document.createElement("div");
    let icon1:HTMLElement = document.createElement("div");
    let cancle:HTMLElement = document.createElement("div");
    let CLBut:HTMLElement = document.createElement("button");
    CLBut.style.width = '50px';
    CLBut.style.height = '50px';
    CLBut.style.background =
    "white url('data:image/png;base64,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') no-repeat 5px / 50px 50px";
    //body.className = "p-Widget jp-Dialog-footer";
    body.className = "fa fa-bookmark-o"
    icon1.className = "jp-Dialog-buttonIcon";
    cancle.className = "jp-Dialog-buttonLabel";
    CLBut.className = "jp-Dialog-button jp-mod-reject jp-mod-styled";
    //cancle.innerText = "Cancle";
    cancle.innerText = "";
    CLBut.appendChild(icon1);
    CLBut.appendChild(cancle);
    div.appendChild(CLBut);
    (<any>CLBut).onclick = ()=>{
        body.parentNode.removeChild(body);
    };
    return div;
}

function addButtons():HTMLElement{
    let footer:HTMLElement = document.createElement("div");
    let icon1:HTMLElement = document.createElement("div");
    //let icon2:HTMLElement = document.createElement("div");
    let cancle:HTMLElement = document.createElement("div");
    //let ok:HTMLElement = document.createElement("div");
    let cancleBut:HTMLElement = document.createElement("button");
    //let okBut:HTMLElement = document.createElement("button");
    footer.className = "p-Widget jp-Dialog-footer";
    icon1.className = "jp-Dialog-buttonIcon";
    //icon2.className = "jp-Dialog-buttonIcon";
    cancle.className = "jp-Dialog-buttonLabel";
    //ok.className = "jp-Dialog-buttonLabel";
    cancleBut.className = "jp-Dialog-button jp-mod-reject jp-mod-styled";
    //okBut.className = "jp-Dialog-button jp-mod-accept jp-mod-styled";
    //ok.innerText = "Summit";
    cancle.innerText = "Exit";
    cancleBut.appendChild(icon1);
    cancleBut.appendChild(cancle);
    //okBut.appendChild(icon2);
    //okBut.appendChild(ok);
    footer.appendChild(cancleBut);
    //footer.appendChild(okBut);
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

function addText(title:string):HTMLElement{
    let text:HTMLSpanElement = document.createElement("span");
    text.className = "p-Widget jp-Dialog-header";
    text.innerText = title;
    (<any>text.style)["margin-top"] = "0.5em";
    return text;
}

export default askParameters;