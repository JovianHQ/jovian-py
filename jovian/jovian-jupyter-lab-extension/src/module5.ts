import {
  ILabShell
} from '@jupyterlab/application';

import {
  Widget,
  PanelLayout
} from '@lumino/widgets'

import {
  searchIcon, 
  jsonIcon, 
  LabIcon, 
  ellipsesIcon
} from '@jupyterlab/ui-components';

import { 
  getSlug, 
  getGist,
  getShell
} from './commands'

import { 
  getUrl, 
  shareToFacebook,
  shareToTwitter,
  shareToLinkedIn
} from './module4';

let sidebar:any = undefined;
let url:string = undefined;

export default async function showSidebar():Promise<void> {
  /**
   * Show the sidebar on the left
   */
  if (sidebar != undefined) {
    sidebar.close();
  }
  let div:HTMLElement = addEmptySidebar();
  div.appendChild(addText("Jovian", "h1"));
  div.appendChild(addLine());
  // check if we have the slug of this notebook
  let slug:string|undefined = undefined, gist:any;
  await getUrl().then(
    (res) => url = res
  );
  await getSlug().then(
    (res) => slug = res
  );
  if (slug != undefined) {
    await getGist(slug).then(
      (res) => gist = res
    );
    let username: string = gist.currentUser.username;
    let projectId:string = username + "/" + gist.title;
    div.appendChild(addText(projectId, "p"));
    div.appendChild(addSubTitle("Version", searchIcon));
    div.appendChild(addVersions(gist));
    div.appendChild(addLine());
    div.appendChild(addText("Share with friends", "h3"));
    div.appendChild(addShareSection());
    div.appendChild(addLine());
    div.appendChild(addSubTitle("Collaborators", jsonIcon));
    div.appendChild(addCollaborators(gist));
  } else {
    let warning = 
      addText("Please commit to Jovian first, and then reopen the sidebar.", "h2");
    warning.style.background = "pink";
    div.appendChild(warning);
  }
}

function addEmptySidebar():HTMLElement {
  /**
   * Add an empty sidebar on the left, and returns the layout
   * (HTMLElement) of this sidebar
   */
  let sidebar = new Sidebar();
  let layer = new PanelLayout();
  let div = new Widget();
  let labShell:ILabShell = getShell();
  sidebar.addClass("jp-extensionmanager-view");
  sidebar.id = "jovian_sidebar";
  sidebar.title.caption = "Jovian Sidebar";
  sidebar.title.icon = ellipsesIcon;
  sidebar.layout = layer;
  labShell.add(sidebar, 'left', { rank: 1100 });
  layer.addWidget(div);
  labShell.activateById(sidebar.id);
  (<any> window).sb = sidebar;
  return div.node;
}

function addIcon(icon: LabIcon, size: number, vb:string):SVGElement {
  /**
   * returns a SVGElement with corresponding icon data
   * from LabIcons of JupyterLab
   */
  let svg:SVGElement = <SVGElement>(icon.element().firstChild);
  svg.setAttribute("width", size.toString() + "px");
  svg.setAttribute("viewBox", vb);
  return svg;
}

function addText(_text:string, type:string):HTMLElement {
  /**
   * returns a text element with corresponding type, and
   * it is align in the middle
   */
  let text = document.createElement(type);
  text.innerText = _text;
  (<any>text).style['text-align'] = 'center';
  return text;
}

function addSubTitle(text:string, icon:LabIcon):HTMLElement {
  /**
   * returns a h3 elements with corresponding text and icon
   */
  let h3 = addText(text,"h3");
  let svg = addIcon(icon, 18, "0 0 20 20");
  h3.appendChild(svg);
  return h3;
}

function addLine():HTMLElement {
  /**
   * returns a horizontal line
   */
  return document.createElement("hr");
}

function addMembers(username:string, avatar:string = undefined):HTMLElement {
  /**
   * returns a single user element, which can be added to
   * the collaborator section
   */
  let imgUrl:string = "https://jovian.ml/api/user/" + username + "/avatar";
  if (avatar != undefined) {
    imgUrl = avatar;
  };
  let homePage:string = "https://jovian.ml/" + username;
  let div:HTMLElement = document.createElement("a");
  div.style.display = "inline";
  div.style.padding = "2%";
  div.setAttribute("title", username);
  div.setAttribute("href", homePage);
  div.setAttribute("target", "_blank");
  let img:HTMLElement = document.createElement("img");
  img.style.width = "30px";
  img.style.height = "30px";
  img.setAttribute("src", imgUrl);
  div.appendChild(img)
  return div;
}

function addCollaborators(gist:string):HTMLElement {
  /**
   * returns the collaborator section with corresponding
   * members of this notebook
   */
  let div:HTMLElement = document.createElement("div");
  (<any>div.style)['text-align'] = "center";
  let infos:any = getInfos(gist);
  infos.members.forEach(
    (member:any) => {
      div.appendChild(addMembers(member.username, member.avatar));
    }
  );
  return div;
}

function facebookIcon():HTMLElement {
  /**
   * returns a facebook icon inside a div element, which
   * can be added to the share section
   */
  let div:HTMLElement = document.createElement("div");
  let svg:string = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Layer_1" x="0px" y="0px" width="30px" viewBox="0 0 266.893 266.895" enable-background="new 0 0 266.893 266.895" xml:space="preserve"><path id="Blue_1_" fill="#3C5A99" d="M248.082,262.307c7.854,0,14.223-6.369,14.223-14.225V18.812  c0-7.857-6.368-14.224-14.223-14.224H18.812c-7.857,0-14.224,6.367-14.224,14.224v229.27c0,7.855,6.366,14.225,14.224,14.225  H248.082z"/><path id="f" fill="#FFFFFF" d="M182.409,262.307v-99.803h33.499l5.016-38.895h-38.515V98.777c0-11.261,3.127-18.935,19.275-18.935  l20.596-0.009V45.045c-3.562-0.474-15.788-1.533-30.012-1.533c-29.695,0-50.025,18.126-50.025,51.413v28.684h-33.585v38.895h33.585  v99.803H182.409z"/></svg> ';
  div.style.display = "inline";
  div.style.cursor = "pointer";
  div.setAttribute("title", "Share to Facebook");
  div.innerHTML = svg;
  return div;
}

function twitterIcon():HTMLElement {
  /**
   * returns a twitter icon inside a div element, which
   * can be added to the share section
   */
  let div:HTMLElement = document.createElement("div");
  let svg:string = '<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="30px" viewBox="0 0 400 400" style="enable-background:new 0 0 400 400;" xml:space="preserve"><style type="text/css">.st0{fill:#1DA1F2;}.st1{fill:#FFFFFF;}</style><g id="Dark_Blue"><circle class="st0" cx="200" cy="200" r="200"/></g><g id="Logo__x2014__FIXED"><path class="st1" d="M163.4,305.5c88.7,0,137.2-73.5,137.2-137.2c0-2.1,0-4.2-0.1-6.2c9.4-6.8,17.6-15.3,24.1-25c-8.6,3.8-17.9,6.4-27.7,7.6c10-6,17.6-15.4,21.2-26.7c-9.3,5.5-19.6,9.5-30.6,11.7c-8.8-9.4-21.3-15.2-35.2-15.2c-26.6,0-48.2,21.6-48.2,48.2c0,3.8,0.4,7.5,1.3,11c-40.1-2-75.6-21.2-99.4-50.4c-4.1,7.1-6.5,15.4-6.5,24.2c0,16.7,8.5,31.5,21.5,40.1c-7.9-0.2-15.3-2.4-21.8-6c0,0.2,0,0.4,0,0.6c0,23.4,16.6,42.8,38.7,47.3c-4,1.1-8.3,1.7-12.7,1.7c-3.1,0-6.1-0.3-9.1-0.9c6.1,19.2,23.9,33.1,45,33.5c-16.5,12.9-37.3,20.6-59.9,20.6c-3.9,0-7.7-0.2-11.5-0.7C110.8,297.5,136.2,305.5,163.4,305.5"/></g></svg>';
  div.style.display = "inline";
  div.style.cursor = "pointer";
  div.setAttribute("title", "Share to LinkedIn");
  div.innerHTML = svg;
  return div;
}

function linkedInIcon():HTMLElement {
  /**
   * returns a LinkedIn icon inside a div element, which
   * can be added to the share section
   */
  let div:HTMLElement = document.createElement("div");
  let svg:string = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="30px"><linearGradient id="SUJNhpmDQDF27Y3OfwgfYa" x1="19" x2="19" y1="24.858" y2="49.041" gradientUnits="userSpaceOnUse" spreadMethod="reflect"><stop offset="0" stop-color="#6dc7ff"/><stop offset="1" stop-color="#e6abff"/></linearGradient><path fill="url(#SUJNhpmDQDF27Y3OfwgfYa)" fill-rule="evenodd" d="M22 48L22 26 16 26 16 48 22 48z" clip-rule="evenodd"/><linearGradient id="SUJNhpmDQDF27Y3OfwgfYb" x1="19.382" x2="19.382" y1="15.423" y2="23.341" gradientUnits="userSpaceOnUse" spreadMethod="reflect"><stop offset="0" stop-color="#6dc7ff"/><stop offset="1" stop-color="#e6abff"/></linearGradient><path fill="url(#SUJNhpmDQDF27Y3OfwgfYb)" fill-rule="evenodd" d="M19.358,23c2.512,0,4.076-1.474,4.076-3.554 c-0.047-2.126-1.564-3.649-4.028-3.649c-2.465,0-4.076,1.475-4.076,3.601c0,2.08,1.563,3.602,3.981,3.602H19.358L19.358,23z" clip-rule="evenodd"/><linearGradient id="SUJNhpmDQDF27Y3OfwgfYc" x1="37.386" x2="37.386" y1="14.125" y2="49.525" gradientUnits="userSpaceOnUse" spreadMethod="reflect"><stop offset="0" stop-color="#6dc7ff"/><stop offset="1" stop-color="#e6abff"/></linearGradient><path fill="url(#SUJNhpmDQDF27Y3OfwgfYc)" fill-rule="evenodd" d="M26.946,48H34V35.911c0-0.648,0.122-1.295,0.313-1.758 c0.52-1.295,1.877-2.635,3.867-2.635c2.607,0,3.821,1.988,3.821,4.901V48h6V35.588c0-6.657-3.085-9.498-7.826-9.498 c-3.886,0-5.124,1.91-6.072,3.91H34v-4h-7.054c0.095,2-0.175,22-0.175,22H26.946z" clip-rule="evenodd"/><linearGradient id="SUJNhpmDQDF27Y3OfwgfYd" x1="32" x2="32" y1="6.5" y2="57.5" gradientUnits="userSpaceOnUse" spreadMethod="reflect"><stop offset="0" stop-color="#1a6dff"/><stop offset="1" stop-color="#c822ff"/></linearGradient><path fill="url(#SUJNhpmDQDF27Y3OfwgfYd)" d="M50,57H14c-3.859,0-7-3.141-7-7V14c0-3.859,3.141-7,7-7h36c3.859,0,7,3.141,7,7v36 C57,53.859,53.859,57,50,57z M14,9c-2.757,0-5,2.243-5,5v36c0,2.757,2.243,5,5,5h36c2.757,0,5-2.243,5-5V14c0-2.757-2.243-5-5-5H14z"/></svg>';
  div.style.display = "inline";
  div.style.cursor = "pointer";
  div.setAttribute("title", "Share to Twitter");
  div.innerHTML = svg;
  return div;
}


function addShareSection():HTMLElement {
  /**
   * returns the share section with some share options
   */
  let newSpan = () => {
    let span = document.createElement("span");
    span.style.display = "inline-block";
    span.style.width = "25px";
    return span;
  };
  let div:HTMLElement = document.createElement("div");
  (<any>div.style)['text-align'] = "center";
  let fb = shareToFacebook(url, facebookIcon());
  let tt = shareToTwitter(url, twitterIcon());
  let li = shareToLinkedIn(url, linkedInIcon());
  div.appendChild(fb);
  div.appendChild(newSpan());
  div.appendChild(tt);
  div.appendChild(newSpan());
  div.appendChild(li);
  return div;
}

function addVersions(gist:string):HTMLElement{
  /**
   * return a selection element with all the versions
   * as options of the current notebook
   */
  let div:HTMLElement = document.createElement("div");
  let div1:HTMLElement = document.createElement("div");
  let selection:HTMLSelectElement = document.createElement("select");
  div.className = "p-Widget jp-Input-Dialog jp-Dialog-body";
  div1.className = "jp-select-wrapper";
  selection.className = "jp-mod-styled";
  let addOption = (value:string, title: string) => {
    let option:HTMLOptionElement = document.createElement("option");
    option.value = value;
    option.innerText = title;
    return option;
  };
  let infos:any = getInfos(gist);
  infos.versions.forEach(
    (version:any) => {
      selection.appendChild(addOption(version.url, version.title));
    }
  );
  div1.appendChild(selection);
  div.appendChild(div1);
  return div;
}

function getInfos(gist:any): {
  members: Array<{avatar:string, username:string}>,
  versions: Array<{title:string, url: string}>
} {
  /**
   * returns a object with only members and versions
   * of the current notebook
   */
  let currentUser:string = gist.currentUser.username;
  let res:any = {
    members: [],
    versions: []
  };
  // processing members
  gist.members.forEach(
    (member:any) => {
      let temp = {
        avatar: member.account.avatar, 
        username: member.account.username
      };
      res.members.push(temp);
    }
  );
  // processing versions
  gist.versions.forEach(
    (version:any) => {
      let temp = {
        title: version.title, 
        url: "https://jovian.ml/" + currentUser + "/v/" + version.id
      };
      res.versions.unshift(temp);
    }
  );
  return res;
}

class Sidebar extends Widget {
  /**
   * This is the class we use to create a sidebar
   */
  protected onAfterShow():void {
    // use to detect if open.
    sidebar = this;
  }
  protected onBeforeHide():void {
    sidebar = undefined;
    this.close();
  }
}