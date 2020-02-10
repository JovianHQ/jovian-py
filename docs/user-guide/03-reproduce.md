## Reproducing uploaded notebooks

An uploaded notebook on <a href="https://jovian.ml?utm_source=docs" target=_blank> Jovian.ml </a> can be reproduced in any other machine. Following are the steps involved to reproduce a notebook.

### Clone

1. Visit the link of the uploaded notebook.
2. Click on the `Clone` button, to copy the notebook's clone command to the clipboard.
3. Paste the command in the terminal, in the directory where you want to clone the notebook project and then run the command.

<img src="https://i.imgur.com/GPpjea5.gif" class="screenshot">

The copied command will be of the the following format

```
jovian clone <username/project-title>
```

<img src="https://i.imgur.com/9AmJ9hu.gif" class="screenshot">

### Install

<a href="https://jovian.ml?utm_source=docs" target=_blank> Jovian.ml </a> captures the original python environment of the notebook, which make it easier to reproduce the notebook by installing all the required dependencies.
The following commands uses <a href="https://conda.io" target=_blank> Anaconda </a> to install all the required packages, make sure that conda is installed.

Once the notebook is cloned, it would have created a folder with the name of the notebook project.

Move into that directory.

```
cd jovian-demo
```

Then run

```
jovian install
```

The above command prompts for a virtual environment name where it will install all the required packages. By default it will have the original environment name in the square brackets, just click `enter` key to retain the name else specify the environment name.

<img src="https://i.imgur.com/ysEWR80.gif" class="screenshot">

In this way, <a href="https://jovian.ml?utm_source=docs" target=_blank> Jovian.ml </a> seamlessly ensures the end-to-end reproducibility of your Jupyter notebooks across different operating systems.

```eval_rst
.. note:: You have to own the notebook or have to be a collaborator to commit changes to the same notebook project. If not you can commit the cloned notebook with any changes to your Jovian profile as a new notebook project.
```

### Pull

If there are any new versions uploaded after you have cloned the notebook by any of the collaborator.
You can use `pull` to get all those changes.

Move to the cloned directory and run

```
jovian pull
```

<img src="https://i.imgur.com/h5p4S07.gif" class="screenshot">

```eval_rst
.. attention:: Beware any uncommitted changes will be lost during the process of ``jovian pull``. When you pull the notebook it will be a duplicate of the latest version of the notebook on Jovian.
```
