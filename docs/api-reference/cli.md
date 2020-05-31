## Command Line Commands

```eval_rst
.. click:: jovian.cli:main
    :prog: jovian
    :show-nested:
```

<!-- #### Initialize

Requests for a API Key for a new user, can find the key at [Jovian](https://jnv.io). By clicking on `API key` button, key will be copied to the clipboard.

```
$ jovian init
```

#### Clone a Notebook

Clone a notebook form Jovian, by clicking on the `Clone` button of a notebook repo the whole clone command will be copied to the clipboard.

```
$ jovian clone {notebook_id}
```

#### Pull the latest Notebook

Pull the latest version of the notebook, use the command in a cloned repository or from a repository where you have committed to jovian.

```
$ jovian pull
```

```eval_rst
.. caution::
    Make sure the changes are committed if needed, pull overwrites the current notebook.
```

#### Install the required dependencies

Install all the dependencies required to the the cloned notebook, use the command in a cloned repository.

```
$ jovian install
```

```eval_rst
.. important:: The above command prompts
    `
    Please provide a name for the conda environment [{env_name}]:
    `

    Press enter to install the dependencies to `env_name` (base env if the content of the square brackets is empty) else provide the env name in the prompt.
```

#### Version

Displays the current installed version of jovian library.

```
$ jovian version
```

#### Enable or Disable Jupyter Notebook Extension

By default, the jovian jupyter extension is enabled.

```
$ jovian enable-extension
```

```
$ jovian disable-extension
```

```eval_rst
.. note::
    The changes are observed when the webpage of the notebook is refreshed.
``` -->
