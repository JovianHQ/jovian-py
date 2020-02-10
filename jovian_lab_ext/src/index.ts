import {
  IDisposable,  DisposableDelegate
} from '@phosphor/disposable';

import {
  JupyterFrontEndPlugin, JupyterFrontEnd
} from '@jupyterlab/application';

import {
  ToolbarButton,  //InputDialog
} from '@jupyterlab/apputils';

import {
  DocumentRegistry
} from '@jupyterlab/docregistry';

import {
  NotebookPanel, INotebookModel, //CellList
} from '@jupyterlab/notebook';

import '../style/index.css';

import askParameters from './module2';
  
let positionIndex:number = 9;

let commitButton:any, dropdownButton:any;

class JovainButtonExtension implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {

  readonly app: JupyterFrontEnd;

  constructor(app: JupyterFrontEnd) {
    this.app = app;
  }

  createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
    // Create the on-click callback for the toolbar button.
    let testFunc:any = () => {
      insertAfter(askParameters(), document.getElementById("main"));
    };

    // Create the toolbar button
    // this is the JOVIAN BUTTON
    let button = new ToolbarButton({
      className: 'jovian-lab-ext',
      iconClassName: 'fa fa-bookmark-o',
      onClick: testFunc,
      tooltip: 'commit to jovian'
    });

    // Add the toolbar button to the notebook
    panel.toolbar.insertItem(positionIndex, 'jovian', button);
    
    button.node.className += " jovian-lab-ext-box jovian-lab-ext-commit";
    button.node.addEventListener ("DOMNodeInserted", ()=>{
      let jovian_button:any = button.node.firstChild;
      jovian_button.style.background = 
        // jovian logo, encoded to base64
        "white url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAjCAIAAAAMti2GAAABTGlDQ1BpY2MAACjPY2BgUkksKMhhYWBgyM0rKQpyd1KIiIxSYH/IwA6EvAxiDAqJycUFjgEBPkAlDDAaFXy7xsAIoi/rgsw6JTW1SbVewNdipvDVi69EmxjwA66U1OJkIP0HiFOTC4pKGBgYU4Bs5fKSAhC7A8gWKQI6CsieA2KnQ9gbQOwkCPsIWE1IkDOQfQPIVkjOSASawfgDyNZJQhJPR2JD7QUBbpfM4oKcxEqFAGMGqoOS1IoSEO2cX1BZlJmeUaLgCAylVAXPvGQ9HQUjA0NzBgZQmENUfw4EhyWj2BmEWPN9Bgbb/f///9+NEPPaz8CwEaiTaydCTMOCgUGQm4HhxM6CxKJEsBAzEDOlpTEwfFrOwMAbycAgfAGoJ7o4zdgILM/I48TAwHrv///PagwM7JMZGP5O+P//96L///8uBmq+w8BwIA8AFSFl7ghfNBMAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAZiS0dEAP8A/wD/oL2nkwAAAAd0SU1FB+MIBgkzIxDC+FwAAANlSURBVEjHtZZNTxtHGMf/M+O3uA5OttgG27UxSmrSppEhRJzKxTckc6nEuQeOfAOuPcIFiS/ByQcUwQfgVGMhgtI3NTah1KwJccB2bNaeeXpYt8QvyGvTzGm1+9+fnvnNPrPDiAifZ9j6JhoShyeyek0AOMOToPjSw/4fdP6dWntZ//CRAGge9tMP9yyied/EwbEsVQmAVHgcEKGHPV6RUg6Mrhm0n28qAgAbx4uYcLTPs1wur62tLS0tbW5u1mq1AYTk36k/i4pzEGF0hD2LiI5AOp1eXV01DGN3dzcSiaRSKatVZ/OyXCMGKMKTcTHu7czrum4YBoB6vV4qlawKqVxT9lia36ZdYHZS2DqLRiqVSiaTPp9vcXExmUxaFfKmqPLnijEQweflT8OiOxOPx7e2tnRdDwaDXq/XKno/LyvXxBkk4dsQD4z0nqKmaZqmdd+/FX1Vo4PjpnntsOFFzCZ6kYnIMAwi4pzb7XbGbj75W13/oau3F4oxKMKYl38TEj1jxWJxeXl5YWFhZWWlUqlYqno/1/xogDMowndh4bvfuwPr9fre3l4ulzs/P280Gp8+6l11qUoHb1sN5rJjdlIwS73dNnqjfzuTp++VWXLwAZ8aFwNib0ETIZOTNXNyhGcRoVnbj/qjLyp0eCJNAy4HZmNiGHBP9C8FWfjQsvGVxr8eG8ZGD7QiZN7I63+XOhEVD9zDFd2FLl6pV39JxkCA28GeT/T/V1hFvz5V+pXiDESIjvJHgf7/CktoqfBzrtlotTdmouK+a0gbneizS/X6VHIGAjwuNjMx5AL2QL86kedlYgykMOnjMd/wNtrQDYlMTjYlADCGmQnxhXN4G23ov0vq14I0F3DkHpuJ3slGG/rwRF5UyNxFHwV4dPRONm7QRhOZnJQKADjH85jNZb+TjRv0yXv1+1nLxkM3S0Ss2pBSmucbIQRr33lb6Gy+eVEhApoKj8dEWLNqI5/Pm2cEv9/vdDo/fWQDQEBY4z9+7zC3pKdh4by9vS8vL9PpdCKRCAQChUJhfX29XC4DmJubc7vdbVEacGxvb3s8Hr/fH4/H/X6/KSEejx8dHXUkB0ZvbGx4PJ7/KhNCTE9P7+zsdCfZoEf3arWayWSy2ayu606nc2pqan5+PhQKdScHRlsf/wCBmeWmRK6m9QAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxOS0wOC0wNlQwOTo1MTozNS0wNDowMBKu+PQAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTktMDgtMDZUMDk6NTE6MzUtMDQ6MDBj80BIAAAAAElFTkSuQmCC') no-repeat 5px / 15px 17px";
        //"white url('data:image/png;base64,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') no-repeat 5px / 15px 17px";

        jovian_button.firstChild.innerText = "Share Dialogue"; //MODIFY
      jovian_button.firstChild.style.color = "black";
      jovian_button.firstChild.style["padding-left"] = "17px";
    },{
      once: true,
      passive: true,
      capture: true
    });

    //this is the JOVIAN BUTTON
    let jovian_button:any = button.node.firstChild;
      button.node.onmouseenter = ()=>{
      jovian_button.style.background = 
        "rgb(231, 229, 229) url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAjCAIAAAAMti2GAAABTGlDQ1BpY2MAACjPY2BgUkksKMhhYWBgyM0rKQpyd1KIiIxSYH/IwA6EvAxiDAqJycUFjgEBPkAlDDAaFXy7xsAIoi/rgsw6JTW1SbVewNdipvDVi69EmxjwA66U1OJkIP0HiFOTC4pKGBgYU4Bs5fKSAhC7A8gWKQI6CsieA2KnQ9gbQOwkCPsIWE1IkDOQfQPIVkjOSASawfgDyNZJQhJPR2JD7QUBbpfM4oKcxEqFAGMGqoOS1IoSEO2cX1BZlJmeUaLgCAylVAXPvGQ9HQUjA0NzBgZQmENUfw4EhyWj2BmEWPN9Bgbb/f///9+NEPPaz8CwEaiTaydCTMOCgUGQm4HhxM6CxKJEsBAzEDOlpTEwfFrOwMAbycAgfAGoJ7o4zdgILM/I48TAwHrv///PagwM7JMZGP5O+P//96L///8uBmq+w8BwIA8AFSFl7ghfNBMAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAZiS0dEAP8A/wD/oL2nkwAAAAd0SU1FB+MIBgkzIxDC+FwAAANlSURBVEjHtZZNTxtHGMf/M+O3uA5OttgG27UxSmrSppEhRJzKxTckc6nEuQeOfAOuPcIFiS/ByQcUwQfgVGMhgtI3NTah1KwJccB2bNaeeXpYt8QvyGvTzGm1+9+fnvnNPrPDiAifZ9j6JhoShyeyek0AOMOToPjSw/4fdP6dWntZ//CRAGge9tMP9yyied/EwbEsVQmAVHgcEKGHPV6RUg6Mrhm0n28qAgAbx4uYcLTPs1wur62tLS0tbW5u1mq1AYTk36k/i4pzEGF0hD2LiI5AOp1eXV01DGN3dzcSiaRSKatVZ/OyXCMGKMKTcTHu7czrum4YBoB6vV4qlawKqVxT9lia36ZdYHZS2DqLRiqVSiaTPp9vcXExmUxaFfKmqPLnijEQweflT8OiOxOPx7e2tnRdDwaDXq/XKno/LyvXxBkk4dsQD4z0nqKmaZqmdd+/FX1Vo4PjpnntsOFFzCZ6kYnIMAwi4pzb7XbGbj75W13/oau3F4oxKMKYl38TEj1jxWJxeXl5YWFhZWWlUqlYqno/1/xogDMowndh4bvfuwPr9fre3l4ulzs/P280Gp8+6l11qUoHb1sN5rJjdlIwS73dNnqjfzuTp++VWXLwAZ8aFwNib0ETIZOTNXNyhGcRoVnbj/qjLyp0eCJNAy4HZmNiGHBP9C8FWfjQsvGVxr8eG8ZGD7QiZN7I63+XOhEVD9zDFd2FLl6pV39JxkCA28GeT/T/V1hFvz5V+pXiDESIjvJHgf7/CktoqfBzrtlotTdmouK+a0gbneizS/X6VHIGAjwuNjMx5AL2QL86kedlYgykMOnjMd/wNtrQDYlMTjYlADCGmQnxhXN4G23ov0vq14I0F3DkHpuJ3slGG/rwRF5UyNxFHwV4dPRONm7QRhOZnJQKADjH85jNZb+TjRv0yXv1+1nLxkM3S0Ss2pBSmucbIQRr33lb6Gy+eVEhApoKj8dEWLNqI5/Pm2cEv9/vdDo/fWQDQEBY4z9+7zC3pKdh4by9vS8vL9PpdCKRCAQChUJhfX29XC4DmJubc7vdbVEacGxvb3s8Hr/fH4/H/X6/KSEejx8dHXUkB0ZvbGx4PJ7/KhNCTE9P7+zsdCfZoEf3arWayWSy2ayu606nc2pqan5+PhQKdScHRlsf/wCBmeWmRK6m9QAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxOS0wOC0wNlQwOTo1MTozNS0wNDowMBKu+PQAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTktMDgtMDZUMDk6NTE6MzUtMDQ6MDBj80BIAAAAAElFTkSuQmCC') no-repeat 5px / 15px 17px";
      let dropdown:any = dropdownButton.node.firstChild;
      dropdown.style.background = "rgb(209, 207, 207)";
    };

    //this button is POINTING DROPDOWN
    button.node.onmouseleave = ()=>{
      let jovian_button:any = button.node.firstChild;
      jovian_button.style.background = 
        "white url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAjCAIAAAAMti2GAAABTGlDQ1BpY2MAACjPY2BgUkksKMhhYWBgyM0rKQpyd1KIiIxSYH/IwA6EvAxiDAqJycUFjgEBPkAlDDAaFXy7xsAIoi/rgsw6JTW1SbVewNdipvDVi69EmxjwA66U1OJkIP0HiFOTC4pKGBgYU4Bs5fKSAhC7A8gWKQI6CsieA2KnQ9gbQOwkCPsIWE1IkDOQfQPIVkjOSASawfgDyNZJQhJPR2JD7QUBbpfM4oKcxEqFAGMGqoOS1IoSEO2cX1BZlJmeUaLgCAylVAXPvGQ9HQUjA0NzBgZQmENUfw4EhyWj2BmEWPN9Bgbb/f///9+NEPPaz8CwEaiTaydCTMOCgUGQm4HhxM6CxKJEsBAzEDOlpTEwfFrOwMAbycAgfAGoJ7o4zdgILM/I48TAwHrv///PagwM7JMZGP5O+P//96L///8uBmq+w8BwIA8AFSFl7ghfNBMAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAZiS0dEAP8A/wD/oL2nkwAAAAd0SU1FB+MIBgkzIxDC+FwAAANlSURBVEjHtZZNTxtHGMf/M+O3uA5OttgG27UxSmrSppEhRJzKxTckc6nEuQeOfAOuPcIFiS/ByQcUwQfgVGMhgtI3NTah1KwJccB2bNaeeXpYt8QvyGvTzGm1+9+fnvnNPrPDiAifZ9j6JhoShyeyek0AOMOToPjSw/4fdP6dWntZ//CRAGge9tMP9yyied/EwbEsVQmAVHgcEKGHPV6RUg6Mrhm0n28qAgAbx4uYcLTPs1wur62tLS0tbW5u1mq1AYTk36k/i4pzEGF0hD2LiI5AOp1eXV01DGN3dzcSiaRSKatVZ/OyXCMGKMKTcTHu7czrum4YBoB6vV4qlawKqVxT9lia36ZdYHZS2DqLRiqVSiaTPp9vcXExmUxaFfKmqPLnijEQweflT8OiOxOPx7e2tnRdDwaDXq/XKno/LyvXxBkk4dsQD4z0nqKmaZqmdd+/FX1Vo4PjpnntsOFFzCZ6kYnIMAwi4pzb7XbGbj75W13/oau3F4oxKMKYl38TEj1jxWJxeXl5YWFhZWWlUqlYqno/1/xogDMowndh4bvfuwPr9fre3l4ulzs/P280Gp8+6l11qUoHb1sN5rJjdlIwS73dNnqjfzuTp++VWXLwAZ8aFwNib0ETIZOTNXNyhGcRoVnbj/qjLyp0eCJNAy4HZmNiGHBP9C8FWfjQsvGVxr8eG8ZGD7QiZN7I63+XOhEVD9zDFd2FLl6pV39JxkCA28GeT/T/V1hFvz5V+pXiDESIjvJHgf7/CktoqfBzrtlotTdmouK+a0gbneizS/X6VHIGAjwuNjMx5AL2QL86kedlYgykMOnjMd/wNtrQDYlMTjYlADCGmQnxhXN4G23ov0vq14I0F3DkHpuJ3slGG/rwRF5UyNxFHwV4dPRONm7QRhOZnJQKADjH85jNZb+TjRv0yXv1+1nLxkM3S0Ss2pBSmucbIQRr33lb6Gy+eVEhApoKj8dEWLNqI5/Pm2cEv9/vdDo/fWQDQEBY4z9+7zC3pKdh4by9vS8vL9PpdCKRCAQChUJhfX29XC4DmJubc7vdbVEacGxvb3s8Hr/fH4/H/X6/KSEejx8dHXUkB0ZvbGx4PJ7/KhNCTE9P7+zsdCfZoEf3arWayWSy2ayu606nc2pqan5+PhQKdScHRlsf/wCBmeWmRK6m9QAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxOS0wOC0wNlQwOTo1MTozNS0wNDowMBKu+PQAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTktMDgtMDZUMDk6NTE6MzUtMDQ6MDBj80BIAAAAAElFTkSuQmCC') no-repeat 5px / 15px 17px";
      let dropdown:any = dropdownButton.node.firstChild;
      dropdown.style.background = "white";
    };

    commitButton = button;
    return button;
  }
}

function insertAfter (newNode:any, referenceNode:any):void {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

class dropdown implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
  /**
   * Create a new extension object.
   */
  //***************************BUTTON POINTING DROPDOWN**************************///////////
  createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
    
    let callback = () =>{
      // display the dropdown menu 

      let jovian_button:any = button.node.firstChild;
      button.node.onmouseenter = ()=>{
      jovian_button.style.background = 
        "rgb(231, 229, 229) url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAjCAIAAAAMti2GAAABTGlDQ1BpY2MAACjPY2BgUkksKMhhYWBgyM0rKQpyd1KIiIxSYH/IwA6EvAxiDAqJycUFjgEBPkAlDDAaFXy7xsAIoi/rgsw6JTW1SbVewNdipvDVi69EmxjwA66U1OJkIP0HiFOTC4pKGBgYU4Bs5fKSAhC7A8gWKQI6CsieA2KnQ9gbQOwkCPsIWE1IkDOQfQPIVkjOSASawfgDyNZJQhJPR2JD7QUBbpfM4oKcxEqFAGMGqoOS1IoSEO2cX1BZlJmeUaLgCAylVAXPvGQ9HQUjA0NzBgZQmENUfw4EhyWj2BmEWPN9Bgbb/f///9+NEPPaz8CwEaiTaydCTMOCgUGQm4HhxM6CxKJEsBAzEDOlpTEwfFrOwMAbycAgfAGoJ7o4zdgILM/I48TAwHrv///PagwM7JMZGP5O+P//96L///8uBmq+w8BwIA8AFSFl7ghfNBMAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAZiS0dEAP8A/wD/oL2nkwAAAAd0SU1FB+MIBgkzIxDC+FwAAANlSURBVEjHtZZNTxtHGMf/M+O3uA5OttgG27UxSmrSppEhRJzKxTckc6nEuQeOfAOuPcIFiS/ByQcUwQfgVGMhgtI3NTah1KwJccB2bNaeeXpYt8QvyGvTzGm1+9+fnvnNPrPDiAifZ9j6JhoShyeyek0AOMOToPjSw/4fdP6dWntZ//CRAGge9tMP9yyied/EwbEsVQmAVHgcEKGHPV6RUg6Mrhm0n28qAgAbx4uYcLTPs1wur62tLS0tbW5u1mq1AYTk36k/i4pzEGF0hD2LiI5AOp1eXV01DGN3dzcSiaRSKatVZ/OyXCMGKMKTcTHu7czrum4YBoB6vV4qlawKqVxT9lia36ZdYHZS2DqLRiqVSiaTPp9vcXExmUxaFfKmqPLnijEQweflT8OiOxOPx7e2tnRdDwaDXq/XKno/LyvXxBkk4dsQD4z0nqKmaZqmdd+/FX1Vo4PjpnntsOFFzCZ6kYnIMAwi4pzb7XbGbj75W13/oau3F4oxKMKYl38TEj1jxWJxeXl5YWFhZWWlUqlYqno/1/xogDMowndh4bvfuwPr9fre3l4ulzs/P280Gp8+6l11qUoHb1sN5rJjdlIwS73dNnqjfzuTp++VWXLwAZ8aFwNib0ETIZOTNXNyhGcRoVnbj/qjLyp0eCJNAy4HZmNiGHBP9C8FWfjQsvGVxr8eG8ZGD7QiZN7I63+XOhEVD9zDFd2FLl6pV39JxkCA28GeT/T/V1hFvz5V+pXiDESIjvJHgf7/CktoqfBzrtlotTdmouK+a0gbneizS/X6VHIGAjwuNjMx5AL2QL86kedlYgykMOnjMd/wNtrQDYlMTjYlADCGmQnxhXN4G23ov0vq14I0F3DkHpuJ3slGG/rwRF5UyNxFHwV4dPRONm7QRhOZnJQKADjH85jNZb+TjRv0yXv1+1nLxkM3S0Ss2pBSmucbIQRr33lb6Gy+eVEhApoKj8dEWLNqI5/Pm2cEv9/vdDo/fWQDQEBY4z9+7zC3pKdh4by9vS8vL9PpdCKRCAQChUJhfX29XC4DmJubc7vdbVEacGxvb3s8Hr/fH4/H/X6/KSEejx8dHXUkB0ZvbGx4PJ7/KhNCTE9P7+zsdCfZoEf3arWayWSy2ayu606nc2pqan5+PhQKdScHRlsf/wCBmeWmRK6m9QAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxOS0wOC0wNlQwOTo1MTozNS0wNDowMBKu+PQAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTktMDgtMDZUMDk6NTE6MzUtMDQ6MDBj80BIAAAAAElFTkSuQmCC') no-repeat 5px / 15px 17px";
      let dropdown:any = dropdownButton.node.firstChild;
      dropdown.style.background = "rgb(209, 207, 207)";
    };
      
      alert("I always get what I want!");

    };

    let button = new ToolbarButton({
      className: 'jovian-lab-dropdown',
      iconClassName: 'fa fa-caret-down',
      onClick: callback,
      tooltip: 'Jovian Options'
    });

    //*************************************************************************//////////////////

    panel.toolbar.insertItem(positionIndex+1, 'jovian dropdown', button);

    button.node.className += " jovian-lab-ext-box jovian-lab-ext-dropdown";
    button.node.addEventListener ("DOMNodeInserted", ()=>{
      let jovian_dropdown:any = button.node.firstChild;
      jovian_dropdown.style.background = "white";
      (button.node as any).style["margin-left"] = "-2px";
    },{
      once: true,
      passive: true,
      capture: true
    });

    button.node.onmouseenter = ()=>{
      let jovian_button:any = commitButton.node.firstChild;
      jovian_button.style.background = 
        "rgb(209, 207, 207) url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAjCAIAAAAMti2GAAABTGlDQ1BpY2MAACjPY2BgUkksKMhhYWBgyM0rKQpyd1KIiIxSYH/IwA6EvAxiDAqJycUFjgEBPkAlDDAaFXy7xsAIoi/rgsw6JTW1SbVewNdipvDVi69EmxjwA66U1OJkIP0HiFOTC4pKGBgYU4Bs5fKSAhC7A8gWKQI6CsieA2KnQ9gbQOwkCPsIWE1IkDOQfQPIVkjOSASawfgDyNZJQhJPR2JD7QUBbpfM4oKcxEqFAGMGqoOS1IoSEO2cX1BZlJmeUaLgCAylVAXPvGQ9HQUjA0NzBgZQmENUfw4EhyWj2BmEWPN9Bgbb/f///9+NEPPaz8CwEaiTaydCTMOCgUGQm4HhxM6CxKJEsBAzEDOlpTEwfFrOwMAbycAgfAGoJ7o4zdgILM/I48TAwHrv///PagwM7JMZGP5O+P//96L///8uBmq+w8BwIA8AFSFl7ghfNBMAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAZiS0dEAP8A/wD/oL2nkwAAAAd0SU1FB+MIBgkzIxDC+FwAAANlSURBVEjHtZZNTxtHGMf/M+O3uA5OttgG27UxSmrSppEhRJzKxTckc6nEuQeOfAOuPcIFiS/ByQcUwQfgVGMhgtI3NTah1KwJccB2bNaeeXpYt8QvyGvTzGm1+9+fnvnNPrPDiAifZ9j6JhoShyeyek0AOMOToPjSw/4fdP6dWntZ//CRAGge9tMP9yyied/EwbEsVQmAVHgcEKGHPV6RUg6Mrhm0n28qAgAbx4uYcLTPs1wur62tLS0tbW5u1mq1AYTk36k/i4pzEGF0hD2LiI5AOp1eXV01DGN3dzcSiaRSKatVZ/OyXCMGKMKTcTHu7czrum4YBoB6vV4qlawKqVxT9lia36ZdYHZS2DqLRiqVSiaTPp9vcXExmUxaFfKmqPLnijEQweflT8OiOxOPx7e2tnRdDwaDXq/XKno/LyvXxBkk4dsQD4z0nqKmaZqmdd+/FX1Vo4PjpnntsOFFzCZ6kYnIMAwi4pzb7XbGbj75W13/oau3F4oxKMKYl38TEj1jxWJxeXl5YWFhZWWlUqlYqno/1/xogDMowndh4bvfuwPr9fre3l4ulzs/P280Gp8+6l11qUoHb1sN5rJjdlIwS73dNnqjfzuTp++VWXLwAZ8aFwNib0ETIZOTNXNyhGcRoVnbj/qjLyp0eCJNAy4HZmNiGHBP9C8FWfjQsvGVxr8eG8ZGD7QiZN7I63+XOhEVD9zDFd2FLl6pV39JxkCA28GeT/T/V1hFvz5V+pXiDESIjvJHgf7/CktoqfBzrtlotTdmouK+a0gbneizS/X6VHIGAjwuNjMx5AL2QL86kedlYgykMOnjMd/wNtrQDYlMTjYlADCGmQnxhXN4G23ov0vq14I0F3DkHpuJ3slGG/rwRF5UyNxFHwV4dPRONm7QRhOZnJQKADjH85jNZb+TjRv0yXv1+1nLxkM3S0Ss2pBSmucbIQRr33lb6Gy+eVEhApoKj8dEWLNqI5/Pm2cEv9/vdDo/fWQDQEBY4z9+7zC3pKdh4by9vS8vL9PpdCKRCAQChUJhfX29XC4DmJubc7vdbVEacGxvb3s8Hr/fH4/H/X6/KSEejx8dHXUkB0ZvbGx4PJ7/KhNCTE9P7+zsdCfZoEf3arWayWSy2ayu606nc2pqan5+PhQKdScHRlsf/wCBmeWmRK6m9QAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxOS0wOC0wNlQwOTo1MTozNS0wNDowMBKu+PQAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTktMDgtMDZUMDk6NTE6MzUtMDQ6MDBj80BIAAAAAElFTkSuQmCC') no-repeat 5px / 15px 17px";
      let dropdown:any = button.node.firstChild;
      dropdown.style.background = "rgb(231, 229, 229)";
    };

    button.node.onmouseleave = ()=>{
      let jovian_button:any = commitButton.node.firstChild;
      jovian_button.style.background = 
        "white url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB4AAAAjCAIAAAAMti2GAAABTGlDQ1BpY2MAACjPY2BgUkksKMhhYWBgyM0rKQpyd1KIiIxSYH/IwA6EvAxiDAqJycUFjgEBPkAlDDAaFXy7xsAIoi/rgsw6JTW1SbVewNdipvDVi69EmxjwA66U1OJkIP0HiFOTC4pKGBgYU4Bs5fKSAhC7A8gWKQI6CsieA2KnQ9gbQOwkCPsIWE1IkDOQfQPIVkjOSASawfgDyNZJQhJPR2JD7QUBbpfM4oKcxEqFAGMGqoOS1IoSEO2cX1BZlJmeUaLgCAylVAXPvGQ9HQUjA0NzBgZQmENUfw4EhyWj2BmEWPN9Bgbb/f///9+NEPPaz8CwEaiTaydCTMOCgUGQm4HhxM6CxKJEsBAzEDOlpTEwfFrOwMAbycAgfAGoJ7o4zdgILM/I48TAwHrv///PagwM7JMZGP5O+P//96L///8uBmq+w8BwIA8AFSFl7ghfNBMAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdwnLpRPAAAAAZiS0dEAP8A/wD/oL2nkwAAAAd0SU1FB+MIBgkzIxDC+FwAAANlSURBVEjHtZZNTxtHGMf/M+O3uA5OttgG27UxSmrSppEhRJzKxTckc6nEuQeOfAOuPcIFiS/ByQcUwQfgVGMhgtI3NTah1KwJccB2bNaeeXpYt8QvyGvTzGm1+9+fnvnNPrPDiAifZ9j6JhoShyeyek0AOMOToPjSw/4fdP6dWntZ//CRAGge9tMP9yyied/EwbEsVQmAVHgcEKGHPV6RUg6Mrhm0n28qAgAbx4uYcLTPs1wur62tLS0tbW5u1mq1AYTk36k/i4pzEGF0hD2LiI5AOp1eXV01DGN3dzcSiaRSKatVZ/OyXCMGKMKTcTHu7czrum4YBoB6vV4qlawKqVxT9lia36ZdYHZS2DqLRiqVSiaTPp9vcXExmUxaFfKmqPLnijEQweflT8OiOxOPx7e2tnRdDwaDXq/XKno/LyvXxBkk4dsQD4z0nqKmaZqmdd+/FX1Vo4PjpnntsOFFzCZ6kYnIMAwi4pzb7XbGbj75W13/oau3F4oxKMKYl38TEj1jxWJxeXl5YWFhZWWlUqlYqno/1/xogDMowndh4bvfuwPr9fre3l4ulzs/P280Gp8+6l11qUoHb1sN5rJjdlIwS73dNnqjfzuTp++VWXLwAZ8aFwNib0ETIZOTNXNyhGcRoVnbj/qjLyp0eCJNAy4HZmNiGHBP9C8FWfjQsvGVxr8eG8ZGD7QiZN7I63+XOhEVD9zDFd2FLl6pV39JxkCA28GeT/T/V1hFvz5V+pXiDESIjvJHgf7/CktoqfBzrtlotTdmouK+a0gbneizS/X6VHIGAjwuNjMx5AL2QL86kedlYgykMOnjMd/wNtrQDYlMTjYlADCGmQnxhXN4G23ov0vq14I0F3DkHpuJ3slGG/rwRF5UyNxFHwV4dPRONm7QRhOZnJQKADjH85jNZb+TjRv0yXv1+1nLxkM3S0Ss2pBSmucbIQRr33lb6Gy+eVEhApoKj8dEWLNqI5/Pm2cEv9/vdDo/fWQDQEBY4z9+7zC3pKdh4by9vS8vL9PpdCKRCAQChUJhfX29XC4DmJubc7vdbVEacGxvb3s8Hr/fH4/H/X6/KSEejx8dHXUkB0ZvbGx4PJ7/KhNCTE9P7+zsdCfZoEf3arWayWSy2ayu606nc2pqan5+PhQKdScHRlsf/wCBmeWmRK6m9QAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAxOS0wOC0wNlQwOTo1MTozNS0wNDowMBKu+PQAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMTktMDgtMDZUMDk6NTE6MzUtMDQ6MDBj80BIAAAAAElFTkSuQmCC') no-repeat 5px / 15px 17px";
      let dropdown:any = button.node.firstChild;
      dropdown.style.background = "white";
    };

    dropdownButton = button;
    return new DisposableDelegate(() => {
      button.dispose();
    });
  }
}
  
async function activate (app: JupyterFrontEnd) {
  app.docRegistry.addWidgetExtension('Notebook', new JovainButtonExtension(app));
  app.docRegistry.addWidgetExtension('Notebook', new dropdown());
}

const extension: JupyterFrontEndPlugin<void> = {
  id: 'jovian-extension',
  autoStart: true,
  activate
};

export default extension;