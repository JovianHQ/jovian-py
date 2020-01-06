## Reproducing uploaded notebooks

A uploaded notebook on Jovian can be reproduced in any other machine. Follow the below procedure to do reproduce the notebook in your machine.

### Clone

**1. Visit the link of the uploaded notebook.**

**2. Click on the `Clone` button, which copies the clone cli command (along with the notebook_id) to the clipboard.**

<img src="https://i.imgur.com/GPpjea5.gif" class="screenshot">

**3. Paste the mcomand in the terminal, in the directory where you want to clone the notebook project and then run the command.**

The copied command will be of the the following format

```
jovian clone <notebook_id>
```

<img src="https://i.imgur.com/9AmJ9hu.gif" class="screenshot">

### Install

Jovian captures the original python environment of the notebook, which make it easier to reproduce the notebook by installing all the required dependencies.
The following commands uses [conda](https://conda.io) to install all the required packages, make sure that conda is installed.

Once the notebook is cloned, it would have created a folder with the name of the notebook. Move to that directory.

```
cd jovian-demo
```

Then run

```
jovian install
```

The above command prompts for a virtual environment name where it will install all the required packages. By default it will have the original environment name in the square brackets, just click `enter` key to retain the name else specify the environment name.

<img src="https://i.imgur.com/ysEWR80.gif" class="screenshot">

In this way, Jovian seamlessly ensures the end-to-end reproducibility of your Jupyter notebooks across different operating systems.

```eval_rst
.. note:: You have to own the notebook or have to be a collaborator to commit changes to the same project notebook. If not you can commit any changes made to your profile as a new notebook.
```

### Pull

If changes are made after you have cloned the notebook by any of the collaborator.
You can use `pull` to get all those changes.

Move to the cloned directory and run

```
jovian pull
```

<img src="https://i.imgur.com/h5p4S07.gif" class="screenshot">

```eval_rst
.. attention:: Beware any uncommitted changes will be lost during the process of ``jovian.pull``. When you pull the notebook it will be a duplicate of the latest version of the notebook on Jovian.
```
