import json
from time import sleep


from IPython import get_ipython
from jovian.utils.logger import log
from jovian.utils.api import get_current_user
from jovian.utils.credentials import read_cred, WEBAPP_URL_KEY
from jovian.utils.constants import DEFAULT_WEBAPP_URL


# 0. Detect Kaggle notebook
# 1. Get API key
# 2. Get user profile
# 3. Validate project title
# 4. Construct URL jovian.ml/username/project-title and print it
# 5. Call perform_kaggle_commit (gets the JSON and commits from JS)
# 6. Get result of commit in JS, and show an alert (success/failure)

def perform_kaggle_commit(project):
    """ Retreive all cells and writes it to a file called project-name.ipynb, then returns the filename"""
    # Get user profile
    user = get_current_user()['username']

    # Construct and print URL
    url = read_cred(WEBAPP_URL_KEY, DEFAULT_WEBAPP_URL) + user + "/" + project
    log("Uploading notebook to " + url)

    # Construct filename
    filename = project + ".ipynb"

    # Consturct javascript code
    js_code = '''
    require(["base/js/namespace"],function(Jupyter) {
        var nbJson = JSON.stringify(Jupyter.notebook.toJSON());

        console.log("[jovian] Extracted notebook JSON:");
        console.log(nbJson);

        function jvnLog (data) {
          console.log("Result from jovian.commit:");
          if (data.content.text) {
              var result = JSON.parse(data.content.text.trim());
              var msg = result['msg'];
              var err = result['err'];
              if (msg) {
                  alert("Notebook committed successfully! Visit " + msg);
              } else {
                  alert("Notebook commit failed. Error: " + (err || "Unknown"))
              }
          }
          
        };
        
        var pythonCode = `
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import json
 
with open("'''+filename+'''", 'w') as f:
    f.write(r"""${nbJson}""")

jvn_update = StringIO()
jvn_update_err = StringIO()
with redirect_stdout(jvn_update), redirect_stderr(jvn_update_err):
    from jovian import commit

jvn_f_out = StringIO()
jvn_f_err = StringIO()
with redirect_stdout(jvn_f_out), redirect_stderr(jvn_f_err):
    jvn_msg = jovian.commit(project="'''+project+'''", filename="'''+filename+'''", environment=None)

print(json.dumps({'msg': jvn_msg, 'err': jvn_f_err.getvalue(), 'update': jvn_update.getvalue()}))
        `;

        console.log("Invoking jovian.commit")
        // console.log(pythonCode)

        Jupyter.notebook.kernel.execute(pythonCode, { iopub: { output: jvnLog }});
    });'''

    get_ipython().run_cell_magic('javascript', '', js_code)
