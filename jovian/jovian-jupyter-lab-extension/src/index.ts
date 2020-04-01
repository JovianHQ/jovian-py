import {
  IDisposable,  
  DisposableDelegate
} from '@lumino/disposable';

import {
  JupyterFrontEndPlugin, 
  JupyterFrontEnd,
  ILabShell
} from '@jupyterlab/application';

import {
  ToolbarButton
} from '@jupyterlab/apputils';

import {
  DocumentRegistry
} from '@jupyterlab/docregistry';

import {
  NotebookPanel, 
  INotebookModel
} from '@jupyterlab/notebook';

import {
  downloadIcon, 
  caretDownIcon
} from '@jupyterlab/ui-components';

import getDropdown from './module1';
import { 
  setApp,
  hasJovian 
} from './commands'

import {
  commit
} from './module2';

import NK from './NBKernel'

let positionIndex:number = 9; // The position will be used to add Jovian Icon

class JovainButtonExtension implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
  /**
   * This class uses to add the Jovian button into 
   * the jupyter lab toolbar
   */
  readonly app: JupyterFrontEnd;

  constructor(app: JupyterFrontEnd) {
    this.app = app;
    (<any>window).nb = NK;
  }

  createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
    // Create the on-click callback for the toolbar button.
    let callback:any = () => {
      hasJovian(commit);
    };

    // Create the toolbar button
    let button = new ToolbarButton({
      className: 'jovian-lab-ext',
      icon: downloadIcon,
      onClick: callback,
      tooltip: 'commit to jovian'
    });

    // Add the toolbar button to the notebook
    panel.toolbar.insertItem(positionIndex, 'jovian', button);
    
    button.node.addEventListener ("DOMNodeInserted", ()=>{
      let jovian_button:any = button.node.firstChild;
      jovian_button.style['border-radius'] = 0;
      jovian_button.style.background = setIcon("white");
      jovian_button.firstChild.innerText = "Commit";
      jovian_button.firstChild.style.color = "black";
      jovian_button.firstChild.style["padding-left"] = "17px";
    },{
      once: true,
      passive: true,
      capture: true
    });

    button.node.onmouseenter = ()=>{
      let jovian_button:any = button.node.firstChild;
      jovian_button.style.background = setIcon("rgb(209, 207, 207)");
    };

    button.node.onmouseleave = ()=>{
      let jovian_button:any = button.node.firstChild;
      jovian_button.style.background = setIcon("white");
    };

    return button;
  }
}

class dropdown implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
  /**
   * Creates a dropdown button into the toolbar, so
   * this class is needed
   */
   createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
    
    let callback = () => {
      // display the dropdown menu 
      hasJovian(getDropdown);
    };

    let button = new ToolbarButton({
      className: 'jovian-lab-dropdown',
      icon: caretDownIcon,
      onClick: callback,
      tooltip: 'Jovian Options'
    });

    panel.toolbar.insertItem(positionIndex+1, 'jovian dropdown', button);

    button.node.addEventListener ("DOMNodeInserted", ()=>{
      let jovian_dropdown:any = button.node.firstChild;
      jovian_dropdown.style['border-radius'] = 0;
      jovian_dropdown.style.background = "white";
      (button.node as any).style["margin-left"] = "-2px";
    },{
      once: true,
      passive: true,
      capture: true
    });

    button.node.onmouseenter = ()=>{
      let dropdown:any = button.node.firstChild;
      dropdown.style.background = "rgb(209, 207, 207)";
    };

    button.node.onmouseleave = ()=>{
      let dropdown:any = button.node.firstChild;
      dropdown.style.background = "white";
    };

    return new DisposableDelegate(() => {
      button.dispose();
    });
  }
}

function setIcon(color:string):string {
  /**
   * Helper function, which uses to set the icon for Jovian
   */
  let icon:string = color + " url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAjCAIAAAAMti2GAAABTGlDQ1BpY2MAACjPY2BgUkksKMhhYWBgyM0rKQpyd1KIiIxSYH/IwA6EvAxiDAqJycUFjgEBPkAlDDAaFXy7xsAIoi/rgsw6JTW1SbVewNdipvDVi69EmxjwA66U1OJkIP0HiFOTC4pKGBgYU4Bs5fKSAhC7A8gWKQI6CsieA2KnQ9gbQOwkCPsIWE1IkDOQfQPIVkjOSASawfgDyNZJQhJPR2JD7QUBbpfM4oKcxEqFAGMGqoOS1IoSEO2cX1BZlJmeUaLgCAylVAXPvGQ9HQUjA0NzBgZQmENUfw4EhyWj2BmEWPN9Bgbb/f///9+NEPPaz8CwEaiTaydCTMOCgUGQm4HhxM6CxKJEsBAzEDOlpTEwfFrOwMAbycAgfAGoJ7o4zdgILM/I48TAwHrv///PagwM7JMZGP5O+P//96L///8uBmq+w8BwIA8AFSFl7ghfNBMAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAZiS0dEAP8A/wD/oL2nkwAAAAd0SU1FB+MIBgkzIxDC+FwAAANlSURBVEjHtZZNTxtHGMf/M+O3uA5OttgG27UxSmrSppEhRJzKxTckc6nEuQeOfAOuPcIFiS/ByQcUwQfgVGMhgtI3NTah1KwJccB2bNaeeXpYt8QvyGvTzGm1+9+fnvnNPrPDiAifZ9j6JhoShyeyek0AOMOToPjSw/4fdP6dWntZ//CRAGge9tMP9yyied/EwbEsVQmAVHgcEKGHPV6RUg6Mrhm0n28qAgAbx4uYcLTPs1wur62tLS0tbW5u1mq1AYTk36k/i4pzEGF0hD2LiI5AOp1eXV01DGN3dzcSiaRSKatVZ/OyXCMGKMKTcTHu7czrum4YBoB6vV4qlawKqVxT9lia36ZdYHZS2DqLRiqVSiaTPp9vcXExmUxaFfKmqPLnijEQweflT8OiOxOPx7e2tnRdDwaDXq/XKno/LyvXxBkk4dsQD4z0nqKmaZqmdd+/FX1Vo4PjpnntsOFFzCZ6kYnIMAwi4pzb7XbGbj75W13/oau3F4oxKMKYl38TEj1jxWJxeXl5YWFhZWWlUqlYqno/1/xogDMowndh4bvfuwPr9fre3l4ulzs/P280Gp8+6l11qUoHb1sN5rJjdlIwS73dNnqjfzuTp++VWXLwAZ8aFwNib0ETIZOTNXNyhGcRoVnbj/qjLyp0eCJNAy4HZmNiGHBP9C8FWfjQsvGVxr8eG8ZGD7QiZN7I63+XOhEVD9zDFd2FLl6pV39JxkCA28GeT/T/V1hFvz5V+pXiDESIjvJHgf7/CktoqfBzrtlotTdmouK+a0gbneizS/X6VHIGAjwuNjMx5AL2QL86kedlYgykMOnjMd/wNtrQDYlMTjYlADCGmQnxhXN4G23ov0vq14I0F3DkHpuJ3slGG/rwRF5UyNxFHwV4dPRONm7QRhOZnJQKADjH85jNZb+TjRv0yXv1+1nLxkM3S0Ss2pBSmucbIQRr33lb6Gy+eVEhApoKj8dEWLNqI5/Pm2cEv9/vdDo/fWQDQEBY4z9+7zC3pKdh4by9vS8vL9PpdCKRCAQChUJhfX29XC4DmJubc7vdbVEacGxvb3s8Hr/fH4/H/X6/KSEejx8dHXUkB0ZvbGx4PJ7/KhNCTE9P7+zsdCfZoEf3arWayWSy2ayu606nc2pqan5+PhQKdScHRlsf/wCBmeWmRK6m9QAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxOS0wOC0wNlQwOTo1MTozNS0wNDowMBKu+PQAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTktMDgtMDZUMDk6NTE6MzUtMDQ6MDBj80BIAAAAAElFTkSuQmCC') no-repeat 5px / 15px 17px";
  return icon;
}
  
async function activate (app: JupyterFrontEnd, labShell: ILabShell) {
  /**
   * Registers two buttons into JupyterLab toolbar
   *  - button1: Jovian button
   *  - button2: Dropdown button
   */
  app.docRegistry.addWidgetExtension('Notebook', new JovainButtonExtension(app));
  app.docRegistry.addWidgetExtension('Notebook', new dropdown());
  setApp(app, labShell);
}

const extension: JupyterFrontEndPlugin<void> = {
  /**
   * settings of this plugin
   */
  id: 'jovian_lab_extension',
  autoStart: true,
  requires: [
    ILabShell
  ],
  activate
};

export default extension;