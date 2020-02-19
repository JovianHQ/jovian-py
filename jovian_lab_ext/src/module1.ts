import '../style/bootstrap.min.css';
import { askParameters } from './module2';
import setting from './module3';
//import { share }  from './module4';


let body:any;

function getDropdown():void{
  initialHeader();
  let header:HTMLElement = initialHeader();
  header.appendChild(addButton("Commit w/ options",askParameters)); // call commit with parameters
  //header.appendChild(addButton("Share Dialog",share));
  header.appendChild(addButton("Open sidebar",()=>{alert("Open sidebar");})); // call sidebar
  header.appendChild(addButton("Settings",setting)); // call setting
  addRemoveEvent(body);
  correctPosition(header);
  insertAfter(body, document.getElementById("main"));
}

function addButton(value: string,callback:any = ()=>{}):HTMLElement{
  let button:HTMLElement = document.createElement("button");
  button.className = "btn btn-light";
  button.innerText = value;
  button.onclick = callback;
  return button;
}

function initialHeader():HTMLElement{
  let header:HTMLElement = document.createElement("div");
  let subHeader:HTMLElement = document.createElement("div");
  header.className = "p-Widget jp-Dialog";
  subHeader.className = "btn-group-vertical";
  header.appendChild(subHeader);
  body = header;
  return subHeader;
}

function addRemoveEvent(body:HTMLElement):void{
  body.onclick = ()=>body.parentNode.removeChild(body);
}

function correctPosition(butGroup:HTMLElement):void {
  let jovian_btn:any = document.getElementsByClassName("jovian-lab-ext");
  let length:number = jovian_btn.length;
  let temp:any;
  for (let i = 0; i < length; i++){
    temp = jovian_btn[i];
    if (temp.getBoundingClientRect().left > 0){
      jovian_btn = temp;
      break;
    };
  };
  let position:any = jovian_btn.getBoundingClientRect();
  const left:number = position.left;
  const top:number = position.top + 25;
  butGroup.style.position = "absolute";
  butGroup.style.left = left + "px";
  butGroup.style.top = top + "px";
}

function insertAfter(newNode:any, referenceNode:any):void {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

export default getDropdown;