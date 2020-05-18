import NBKernel from "./NBKernel";
import { saveNotebook } from "./commands";

let body: any;
let lock: boolean = false;

async function commit(): Promise<void> {
  /**
   * This function will commit the current notebook to
   * Jovian, it can commit with default options or
   * commit with user-selected options
   */
  const nbFilename: string = NBKernel.currentNotebookName();
  let commit: string = `commit(filename="${nbFilename}")`;
  if (lock == true) {
    return;
  }
  lock = true;
  await saveNotebook();
  getAPIKeys().then(async (result) => {
    if (result == true) {
      const jvn_commit = `
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import json

jvn_update = StringIO()

with redirect_stdout(jvn_update):
  from jovian import commit

jvn_f_out = StringIO()
jvn_f_err = StringIO()

with redirect_stdout(jvn_f_out), redirect_stderr(jvn_f_err):
  jvn_msg = ${commit}

print(json.dumps({'msg': jvn_msg, 'err': jvn_f_err.getvalue(), 'update': jvn_update.getvalue()}))

del jvn_update, jvn_f_out, jvn_f_err, jvn_msg`;

      await NBKernel.execute(jvn_commit).then((result) => {
        committedWindow((result as string).trim());
      });
    } else {
      askAPIKeys();
    }
    lock = false;
  });
}

export function askAPIKeys(): void {
  /**
   * Uses to display a window with a input box, so
   * users can enter their API key to enable the
   * Jovian commit function
   */
  let header: HTMLElement = initialHeader();
  let div: HTMLElement = document.createElement("div");
  let span: HTMLElement = addText("Please enter your API key from Jovian");
  let err: HTMLElement = addErrorMsg("Invalid API key");
  let input: HTMLElement = addInput("Paste your API key", "password");
  let inError = (isError: boolean) => {
    let inp = input.getElementsByTagName("input")[0];
    if (isError) {
      err.hidden = false;
      (<any>inp.style)["border-color"] = "red";
      inp.onkeydown = () => {
        inError(false);
        inp.onkeydown = null;
      };
    } else {
      err.hidden = true;
      (<any>inp.style) = "";
    }
  };
  div.appendChild(span);
  div.appendChild(input);
  header.appendChild(div);
  header.appendChild(err);
  header.appendChild(
    addButtons("Save", () => {
      setAPIKeys(getInputText(input), inError);
    })
  );
  inError(false);
  openWindow();
}

function setAPIKeys(value: string, inError: any): void {
  /**
   * Sets the received API key to Jovian library, and
   * if the key is invalid, displays a error message
   */
  const api_key = value;
  const write_api =
    "from jovian.utils.credentials import write_api_key\n" +
    "write_api_key('" +
    api_key +
    "')\n";
  NBKernel.execute(write_api)
    .then(() => {
      getAPIKeys()
        .then((result) => {
          if (result == true) {
            closeWindow();
            alertWindow(
              'Success! API key saved. Use the "Commit" button to upload your notebook to Jovian.'
            );
          } else {
            inError(true);
          }
        })
        .catch(() => {
          console.log("Failed to validate API key");
        });
    })
    .catch(() => {
      console.log("Failed to write API key");
    });
}

function committedWindow(output: string): void {
  /**
   * Diaplays a window after committing to Jovian, and
   * this window will show whether the committing was
   * successful or not
   */
  const outputObj = JSON.parse(output);
  const msg = outputObj["msg"];
  const err = outputObj["err"];
  const update = outputObj["update"];

  let header: HTMLElement = initialHeader();
  let div: HTMLElement = document.createElement("div");

  if (msg) {
    const label = document.createElement("p");
    label.innerText = "Committed Successfully ";
    const icon = document.createElement("i");
    icon.innerHTML = '<i class="fa fa-check-circle" aria-hidden="true"></i>';
    icon.style.color = "green";
    const nbLink = addLink(msg, msg);

    div.appendChild(label).append(icon);
    div.appendChild(nbLink);
    div.appendChild(document.createElement("br"));

    if (err) {
      const label = document.createElement("p");
      label.innerText = "Warning ";
      const icon = document.createElement("i");
      icon.innerHTML =
        '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>';
      icon.style.color = "rgb(191, 191, 0)";
      div.appendChild(document.createElement("br"));
      div.appendChild(label).append(icon);

      const p = document.createElement("p");
      p.innerText = err;
      div.appendChild(p);
    }
  } else {
    const label = document.createElement("p");
    label.innerText = "Committed Failed ";
    const icon = document.createElement("i");
    icon.innerHTML = '<i class="fa fa-times" aria-hidden="true"></i>';
    icon.style.color = "red";
    div.appendChild(label).append(icon);

    if (err) {
      const p = document.createElement("p");
      p.innerText = err;
      div.appendChild(p);
    }
  }

  if (update) {
    const label = document.createElement("p");
    label.innerText = "Update available ";
    div.appendChild(label);
    const p = document.createElement("p");
    p.innerText = update;
    div.appendChild(p);
  }

  header.appendChild(div);
  header.appendChild(addButtons(null));
  openWindow();
}

export async function getAPIKeys() {
  /**
   * Gets a boolean value which can be used to see whether
   * the extension has a valid API key from Jovian
   */
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
    NBKernel.execute(validate_api).then((result) => {
      if ((result as string).trim() == "valid") {
        res(true);
      } else {
        res(false);
      }
    });
  });
}

/* *******************************************************
 *
 * Start here will all be helper functions:
 *
 * ******************************************************/

function addText(title: string): HTMLElement {
  /**
   * Creates a text message, which can be later added
   * into the commit window or other windows
   */
  let text: HTMLSpanElement = document.createElement("span");
  text.className = "p-Widget jp-Dialog-header";
  text.innerText = title;
  (<any>text.style)["margin-top"] = "0.5em";
  return text;
}

function addErrorMsg(msg: string): HTMLElement {
  /**
   * Creates a errors message, which can be later added
   * into the commit infos window
   */
  let err: HTMLSpanElement = document.createElement("p");
  err.className = "p-Widget";
  err.innerText = msg;
  (<any>err.style)["margin-top"] = "-0.8em";
  (<any>err.style)["color"] = "red";
  return err;
}

function addInput(
  placeHolder: string = "",
  type: string = "text"
): HTMLElement {
  /**
   * Creates a input box with a placeholder value, which
   * can be later added into the commit window
   */
  let div: HTMLElement = document.createElement("div");
  let div1: HTMLElement = document.createElement("div");
  let inp: HTMLInputElement = document.createElement("input");
  div.className = "p-Widget jp-Input-Dialog jp-Dialog-body";
  div1.className = "jp-select-wrapper";
  inp.className = "jp-mod-styled";
  inp.type = type;
  inp.placeholder = placeHolder;
  div.appendChild(div1);
  div1.appendChild(inp);
  return div;
}

function getInputText(input: HTMLElement): string {
  /**
   * Gets the value from a input box
   */
  let text: string = input.getElementsByTagName("input")[0].value;
  return text.trim();
}

function addLink(text: string, link: string): HTMLElement {
  /**
   * Creates a link HTMLElement with corresponding
   * text and link url
   */
  let a: HTMLElement = document.createElement("a");
  a.setAttribute("href", link);
  a.setAttribute("target", "_blank");
  a.style.color = "rgb(27, 87, 177)";
  a.innerText = text;
  return a;
}

function addButtons(name: string | null, callBack = () => {}): HTMLElement {
  /**
   * Create a footer for the window, and add necessary button(s)
   * with corresponding callback function(s)
   */
  let footer: HTMLElement = document.createElement("div");
  let icon1: HTMLElement = document.createElement("div");
  let icon2: HTMLElement = document.createElement("div");
  let cancel: HTMLElement = document.createElement("div");
  let ok: HTMLElement = document.createElement("div");
  let cancelBut: HTMLElement = document.createElement("button");
  let okBut: HTMLElement = document.createElement("button");
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
  (<any>cancelBut).onclick = () => {
    closeWindow();
  };
  if (name != null) {
    cancel.innerText = "Cancel";
    ok.innerText = name;
    okBut.appendChild(icon2);
    okBut.appendChild(ok);
    footer.appendChild(okBut);
    (<any>okBut).onclick = callBack;
  }
  return footer;
}

function initialHeader(): HTMLElement {
  /**
   * Use to create a modal, so we can add HTMLElements into this new modal
   */
  let header: HTMLElement = document.createElement("div");
  let subHeader: HTMLElement = document.createElement("div");
  header.className = "p-Widget jp-Dialog";
  subHeader.className = "p-Widget p-Panel jp-Dialog-content";
  header.appendChild(subHeader);
  body = header;
  return subHeader;
}

function alertWindow(msg: string): void {
  /**
   * alert Dialog inside Jupyter lab instead of a browser alert
   */
  const header: HTMLElement = initialHeader();
  let div: HTMLElement = document.createElement("div");
  div.appendChild(addText(msg));
  header.append(div);
  header.append(addButtons(null));
  openWindow();
}

function openWindow(): void {
  /**
   * When the modal is ready, this function will show the modal (window)
   */
  insertAfter(body, document.getElementById("main"));
}

function closeWindow(): void {
  /**
   * Close and clean the modal (window)
   */
  body.parentNode.removeChild(body);
}

function insertAfter(newNode: any, referenceNode: any): void {
  /**
   * Insert modal into the corresponding position of Document.body
   */
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

export { commit, alertWindow };
