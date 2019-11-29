import {
    Kernel,
    Session,
    KernelMessage
  } from '@jupyterlab/services';

class NBKernel {

    async execute(pythonCode:string) {
        return new Promise((resolve, reject = (msg)=>{console.log(msg)}) => {
            this.currentKernel().then(
                (kernel) => {
                    let result = (kernel as Kernel.IKernel).requestExecute({code:pythonCode, allow_stdin:true});
                    let text:string = "";
                    result.onIOPub = (msg) => {
                        if (KernelMessage.isErrorMsg(msg)){
                            reject(msg.content);
                        } else if (KernelMessage.isStreamMsg(msg)) {
                            text += msg.content.text + "\n";
                        }
                        if (KernelMessage.isStatusMsg(msg)){
                            if (msg.content.execution_state.toLowerCase() == "idle"){
                                resolve(text);
                            }
                        }
                    }
                }
            )
        });
    }

    async currentKernel() {
        return new Promise(resolve => {
            Session.listRunning().then(
                (allSessions)=>{
                    for (let i = 0; i < allSessions.length; i++){
                        let session = allSessions[i];
                        if (session.type.toLowerCase() == "notebook"){
                            let NBnameFromSession = session.name;
                            if (NBnameFromSession.toLowerCase() == this.currentNotebookName().toLowerCase()){
                                resolve(Kernel.connectTo(session.kernel) as Kernel.IKernel);
                            }
                        }
                    }
                }
            )
        });
    }
    
    currentNotebookName():string{
        //return (document.getElementsByClassName("jp-mod-selected jp-mod-running")[0].childNodes[1] as any).innerText;
        return (document.getElementsByClassName("jp-mod-current")[0].childNodes[1] as any).innerText;
    }

}

export default (new NBKernel());