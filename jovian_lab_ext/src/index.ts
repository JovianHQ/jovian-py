import { IDisposable } from "@phosphor/disposable";

import {
  JupyterFrontEndPlugin,
  JupyterFrontEnd
} from "@jupyterlab/application";

import {
  ToolbarButton //InputDialog
} from "@jupyterlab/apputils";

import { DocumentRegistry } from "@jupyterlab/docregistry";

import { NotebookPanel, INotebookModel } from "@jupyterlab/notebook";

import "../style/index.css";

import "./window";
import askParameters from "./window";

class JovainButtonExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
  readonly app: JupyterFrontEnd;

  constructor(app: JupyterFrontEnd) {
    this.app = app;
  }

  createNew(
    panel: NotebookPanel,
    context: DocumentRegistry.IContext<INotebookModel>
  ): IDisposable {
    // Create the on-click callback for the toolbar button.
    let testFunc: any = () => {
      insertAfter(askParameters(), document.getElementById("main"));
    };

    // Create the toolbar button
    let button = new ToolbarButton({
      className: "jovian-lab-ext",
      iconClassName: "logo",
      onClick: testFunc,
      tooltip: "commit to jovian"
    });

    // Add the toolbar button to the notebook
    panel.toolbar.insertItem(9, "jovian", button);
    // The ToolbarButton class implements `IDisposable`, so the
    // button *is* the extension for the purposes of this method.

    button.node.className += " jovian-lab-ext-box";
    button.node.addEventListener(
      "DOMNodeInserted",
      () => {
        let jovian_button: any = button.node.firstChild;
        jovian_button.style.background =
          // jovian logo, encoded to base64
          "white url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAjCAIAAAAMti2GAAABTGlDQ1BpY2MAACjPY2BgUkksKMhhYWBgyM0rKQpyd1KIiIxSYH/IwA6EvAxiDAqJycUFjgEBPkAlDDAaFXy7xsAIoi/rgsw6JTW1SbVewNdipvDVi69EmxjwA66U1OJkIP0HiFOTC4pKGBgYU4Bs5fKSAhC7A8gWKQI6CsieA2KnQ9gbQOwkCPsIWE1IkDOQfQPIVkjOSASawfgDyNZJQhJPR2JD7QUBbpfM4oKcxEqFAGMGqoOS1IoSEO2cX1BZlJmeUaLgCAylVAXPvGQ9HQUjA0NzBgZQmENUfw4EhyWj2BmEWPN9Bgbb/f///9+NEPPaz8CwEaiTaydCTMOCgUGQm4HhxM6CxKJEsBAzEDOlpTEwfFrOwMAbycAgfAGoJ7o4zdgILM/I48TAwHrv///PagwM7JMZGP5O+P//96L///8uBmq+w8BwIA8AFSFl7ghfNBMAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAZiS0dEAP8A/wD/oL2nkwAAAAd0SU1FB+MIBgkzIxDC+FwAAANlSURBVEjHtZZNTxtHGMf/M+O3uA5OttgG27UxSmrSppEhRJzKxTckc6nEuQeOfAOuPcIFiS/ByQcUwQfgVGMhgtI3NTah1KwJccB2bNaeeXpYt8QvyGvTzGm1+9+fnvnNPrPDiAifZ9j6JhoShyeyek0AOMOToPjSw/4fdP6dWntZ//CRAGge9tMP9yyied/EwbEsVQmAVHgcEKGHPV6RUg6Mrhm0n28qAgAbx4uYcLTPs1wur62tLS0tbW5u1mq1AYTk36k/i4pzEGF0hD2LiI5AOp1eXV01DGN3dzcSiaRSKatVZ/OyXCMGKMKTcTHu7czrum4YBoB6vV4qlawKqVxT9lia36ZdYHZS2DqLRiqVSiaTPp9vcXExmUxaFfKmqPLnijEQweflT8OiOxOPx7e2tnRdDwaDXq/XKno/LyvXxBkk4dsQD4z0nqKmaZqmdd+/FX1Vo4PjpnntsOFFzCZ6kYnIMAwi4pzb7XbGbj75W13/oau3F4oxKMKYl38TEj1jxWJxeXl5YWFhZWWlUqlYqno/1/xogDMowndh4bvfuwPr9fre3l4ulzs/P280Gp8+6l11qUoHb1sN5rJjdlIwS73dNnqjfzuTp++VWXLwAZ8aFwNib0ETIZOTNXNyhGcRoVnbj/qjLyp0eCJNAy4HZmNiGHBP9C8FWfjQsvGVxr8eG8ZGD7QiZN7I63+XOhEVD9zDFd2FLl6pV39JxkCA28GeT/T/V1hFvz5V+pXiDESIjvJHgf7/CktoqfBzrtlotTdmouK+a0gbneizS/X6VHIGAjwuNjMx5AL2QL86kedlYgykMOnjMd/wNtrQDYlMTjYlADCGmQnxhXN4G23ov0vq14I0F3DkHpuJ3slGG/rwRF5UyNxFHwV4dPRONm7QRhOZnJQKADjH85jNZb+TjRv0yXv1+1nLxkM3S0Ss2pBSmucbIQRr33lb6Gy+eVEhApoKj8dEWLNqI5/Pm2cEv9/vdDo/fWQDQEBY4z9+7zC3pKdh4by9vS8vL9PpdCKRCAQChUJhfX29XC4DmJubc7vdbVEacGxvb3s8Hr/fH4/H/X6/KSEejx8dHXUkB0ZvbGx4PJ7/KhNCTE9P7+zsdCfZoEf3arWayWSy2ayu606nc2pqan5+PhQKdScHRlsf/wCBmeWmRK6m9QAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxOS0wOC0wNlQwOTo1MTozNS0wNDowMBKu+PQAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTktMDgtMDZUMDk6NTE6MzUtMDQ6MDBj80BIAAAAAElFTkSuQmCC') no-repeat 5px / 15px 17px";
        jovian_button.firstChild.innerText = "Commit";
        jovian_button.firstChild.style.color = "black";
        jovian_button.firstChild.style["padding-left"] = "17px";
      },
      {
        once: true,
        passive: true,
        capture: true
      }
    );

    return button;
  }
}

function insertAfter(newNode: any, referenceNode: any): void {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

async function activate(app: JupyterFrontEnd) {
  let buttonExtension = new JovainButtonExtension(app);
  app.docRegistry.addWidgetExtension("Notebook", buttonExtension);
  app.contextMenu.addItem({
    selector: ".jp-Notebook",
    command: "notebook:run-all-cells",
    rank: -0.5
  });
}

const extension: JupyterFrontEndPlugin<void> = {
  id: "jovian-extension",
  autoStart: true,
  activate
};

export default extension;
