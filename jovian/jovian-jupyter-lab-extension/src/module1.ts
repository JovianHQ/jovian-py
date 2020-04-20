import '../style/bootstrap.min.css';
import { askParameters } from './module2';

let body:any;
let lock:boolean = false;

function getDropdown():void{
  /**
   * This is the function we use to construct a dropdown menu
   * and insert into a correct position of the main window
   */
  if (lock == true) {
    return;
  }
  lock = true;
  initialHeader();
  let header:HTMLElement = initialHeader();
  header.appendChild(addButton("Commit with options",()=>askParameters())); // call commit with parameters
  addRemoveEvent(body); // when clicks outside of the dropdown menu, it disappear the dropdown menu
  correctPosition(header);
  insertAfter(body, document.getElementById("main"));
}

function addButton(value: string,callback:any = ()=>{}):HTMLElement{
  /**
   * Use to generate a dropdown item, which will be later merge into the dropdown menu
   */
  let button:HTMLElement = document.createElement("button");
  button.className = "btn btn-light";
  button.innerText = value;
  button.onclick = callback;
  return button;
}

function initialHeader():HTMLElement{
  /**
   * Use to create a modal, so we can add HTMLElements into this new modal
   */
  let header:HTMLElement = document.createElement("div");
  let subHeader:HTMLElement = document.createElement("div");
  header.className = "p-Widget jp-Dialog";
  subHeader.className = "btn-group-vertical";
  header.appendChild(subHeader);
  body = header;
  return subHeader;
}

function addRemoveEvent(body:HTMLElement):void{
  /**
   * Use to add a click event on the whole modal,
   * When we click this modal, it will disappear itself
   */
  body.onclick = () => {
    body.parentNode.removeChild(body);
    lock = false;
  };
}

function correctPosition(butGroup:HTMLElement):void {
  /**
   * Use to find the corresponding position of the dropdown menu
   * So, it make sure the dropdown menu will appear right below 
   * the Jovian Icon
   */
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
  /**
   * Insert modal into the corresponding position of Document.body
   */
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

export default getDropdown;