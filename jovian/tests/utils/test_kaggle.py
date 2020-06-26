from unittest import mock
import pytest
from textwrap import dedent
from jovian.utils.kaggle import perform_kaggle_commit
from jovian.tests.resources.shared import fake_creds


@pytest.mark.parametrize("args, expected_jovian_commit",
                         [
                             # default commit params w/ full project name
                             ({'message': None,
                               'files': [],
                               'outputs': [],
                               'environment': 'auto',
                               'privacy': 'auto',
                               'project': 'PrajwalPrasahanth/sample-notebook',
                               'new_project': None},
                              """jovian.commit(message=None, files=[], outputs=[], environment='auto', privacy='auto', filename='sample-notebook.ipynb', project='PrajwalPrasahanth/sample-notebook', new_project=None)"""),
                             # default commit params w/ just project title
                             ({'message': None,
                               'files': [],
                               'outputs': [],
                               'environment': 'auto',
                               'privacy': 'auto',
                               'project': 'sample-notebook',
                               'new_project': None},
                              """jovian.commit(message=None, files=[], outputs=[], environment='auto', privacy='auto', filename='sample-notebook.ipynb', project='sample-notebook', new_project=None)"""),
                             # message is string, environment in None, new_project is bool
                             ({'message': "test commit",
                               'files': [],
                               'outputs': [],
                               'environment': None,
                               'privacy': 'auto',
                               'project': 'sample-notebook',
                               'new_project': True},
                              """jovian.commit(message='test commit', files=[], outputs=[], environment=None, privacy='auto', filename='sample-notebook.ipynb', project='sample-notebook', new_project=True)""")
                         ])
@ mock.patch('jovian.utils.kaggle.get_ipython')
@ mock.patch("jovian.utils.kaggle.get_current_user", return_value={'username': 'PrajwalPrashanth'})
def test_perform_kaggle_commit(mock_get_current_user, mock_get_ipython, args, expected_jovian_commit):

    perform_kaggle_commit(**args)

    # expected
    filename = "sample-notebook.ipynb"  # expected filename remains constant for all tests
    jovian_commit = expected_jovian_commit

    # js_code from jovian.utils.kaggle
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
                  element.text("Committed successfully: " + msg)
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
    jvn_msg = '''+jovian_commit+'''

print(json.dumps({'msg': jvn_msg, 'err': jvn_f_err.getvalue(), 'update': jvn_update.getvalue()}))
        `;

        console.log("Invoking jovian.commit")
        // console.log(pythonCode)

        Jupyter.notebook.kernel.execute(pythonCode, { iopub: { output: jvnLog }});
    });'''

    mock_get_ipython().run_cell_magic.assert_called_with('javascript', '', js_code)
