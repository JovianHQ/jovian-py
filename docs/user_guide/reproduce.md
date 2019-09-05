## Reproducing uploaded notebooks

A uploaded notebook on Jovian can be reproduced in any other machine. Follow the below procedure to do so.

### Clone

1. Visit the uploaded notebook
2. Click on `Upload` button, which copies the clone command(along with the notebook_id) to the clipboard.
3. Paste it in the terminal in the directory where you want to clone the notebook project and run it.

**TODO-SB: GIF for clone button**

The copied command will be of the the following format.

```
$ jovian clone <notebook_id>
```

### Install

Jovian makes it easy for the user to run the notebook by capturing the environment while committing.
The following uses [conda](https://conda.io), make sure that is installed.

Once the notebook is cloned, it would have created a folder with the name of the notebook. Move to that directory.

```
$ cd jovian-demo
```

Then run

```
$ jovian install
```

It prompts for a virtual environment name where it will install all the required packages. By default it will have the original environment name in the square brackets, just click `enter` key to retain the name else specify the environment name.

**TODO-SB: GIF for Change directory after clone and then jovian install**

In this way, Jovian seamlessly ensures the end-to-end reproducibility of your Jupyter notebooks across different operating systems.

```eval_rst
.. note:: You have to own the notebook or have to be collaborator to commit changes to the same project notebook. If not you can commit any changes made to your profile as a new notebook.
```

### Pull

If changes are made after you have cloned the notebook by any of the collaborator.
You can use `pull` to get all those changes.

Move to the cloned directory and run

```
$ jovian pull
```

**TODO-SB: GIF to change directory to a cloned directory and use jovian pull**

```eval_rst
.. attention:: Beware any uncommitted changes will be lost during the process pull. When you pull the notebook it will be a duplicate of the latest version of the notebook on jovian.
```
