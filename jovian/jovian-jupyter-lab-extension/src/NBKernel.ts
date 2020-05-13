import { Kernel, Session, KernelMessage } from "@jupyterlab/services";

class NBKernel {
  /**
   * This is a kernel helper class, which use to find the
   * current notebook name, and execute Python code in the
   * current notebook Kernel
   */
  async execute(pythonCode: string): Promise<string> {
    /**
     * Execute Python code and return a promise with the corresponding
     * result of that code
     */
    return new Promise(
      (
        resolve,
        reject = msg => {
          console.log("KERNEL_EXECUTE_ERROR:" + msg);
        }
      ) => {
        this.currentKernel().then(kernel => {
          let result = (kernel as Kernel.IKernelConnection).requestExecute({
            code: pythonCode,
            allow_stdin: true
          });
          let text: string = "";
          result.onIOPub = msg => {
            if (KernelMessage.isErrorMsg(msg)) {
              reject(msg.content);
            } else if (KernelMessage.isStreamMsg(msg)) {
              text += msg.content.text + "\n";
            } else if (KernelMessage.isStatusMsg(msg)) {
              if (msg.content.execution_state.toLowerCase() == "idle") {
                resolve(text);
              }
            }
          };
        });
      }
    );
  }

  async currentKernel() {
    /**
     * Retrieve the current Kernel and return in a promise
     */
    return new Promise(resolve => {
      Session.listRunning().then(allSessions => {
        for (let i = 0; i < allSessions.length; i++) {
          let session = allSessions[i];
          if (session.type.toLowerCase() == "notebook") {
            let NBnameFromSession = session.name;
            if (
              NBnameFromSession.toLowerCase() ==
              this.currentNotebookName().toLowerCase()
            ) {
              resolve(Kernel.connectTo(session.kernel) as Kernel.IKernel);
            }
          }
        }
      });
    });
  }

  currentNotebookName(): string {
    /**
     * Return the name of current Notebook
     * note:
     *   (document.getElementsByClassName("jp-mod-current")
     *   might have zero length, which means JupyterLab did not activate yet
     */
    if (document.getElementsByClassName("jp-mod-current").length !== 0) {
      return (document.getElementsByClassName("jp-mod-current")[0]
        .childNodes[1] as any).innerText;
    } else {
      console.log("JupyterLab not activated yet!");
    }
  }
}

export default new NBKernel();
