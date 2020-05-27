const getVersionListUrl = () => {
  /**
   * promise function: to get
   * the list of urls, for every
   * version of the current
   * notebook.
   */

  return new Promise(resolve => {
    const valStatus = data => {
      resolve(data.content.text.trim());
    };

    const gvlu = `
from jovian.utils.jupyter import get_notebook_name
import jovian.utils.api as api
import json

with open('.jovianrc') as f:
    jovianrc = json.load(f)

lib = jovianrc['notebooks']
book = get_notebook_name()
slug = lib[book]
slug_number = slug['slug']
net1 = api.get_gist(slug_number)
net2 = net1['currentUser']
username = net2['username']
step1 = api.get_gist(slug_number)
book = step1['title']
count = api.get_gist(slug_number)
total = count['version']
list_link = []
for x in range(0+1, total+1):
    a = 'https://jovian.ml/'+username+'/'+book+'/v/'+str(x)+''
    list_link.append(a)
print(list_link)`;

    Jupyter.notebook.kernel.execute(gvlu, {
      iopub: { output: valStatus }
    });
  });
};
