# Reproducing uploaded notebooks

Once a notebook is uploaded to Jovian, anyone (including you) can download the notebook and it's Python dependencies by running `jovian clone <notebook_id>` command on the Linux/Mac terminal or Windows Command Prompt. Try clicking the 'Clone' button at the top of this page to copy the command (including notebook ID) to clipboard.

```
pip install jovian --upgrade
jovian clone 903a04b17036436b843d70443ef5d7ad
```

Once cloned, you can enter the directly and setup the virtual environment using `jovian install`.

```
cd jovian-demo
jovian install
```

Jovian uses [conda](https://conda.io) internally, so make sure you have it installed before running the above commands. Once the libraries are installed, you can activate the environment and start Jupyter in the usual way:

```
conda activate jovian-demo
jupyter notebook
```

In this way, Jovian seamlessly ensures the end-to-end reproducibility of your Jupyter notebooks.

## Updating existing notebooks

Updating existing notebooks is really easy too! Just run `jovian.commit` once again, and Jovian will automatically identify and update the current notebook on your Jovian account.

```
# Updating the notebook
jovian.commit()
```

Jovian keeps track of existing notebooks using a `.jovianrc` file next to your notebook. If you don't want to update the current notebook, but create a new notebook instead, simply delete the `.jovianrc` file. Note that if you rename your notebook, Jovian will upload a new notebooko when you commit, instead of updating the old one.

If you run into issues with updating a notebook, or want to replace a notebook in your account using a new/renamed notebook, you can provide the `notebook_id` argument to `jovian.commit`.

```
jovian.commit(notebook_id="903a04b17036436b843d70443ef5d7ad")
```

## Getting new changes on cloned notebooks

Once a notebook has been updated, the new changes can be retrieved at any cloned location using the `jovian pull` command.

```
cd jovian-demo # Enter cloned directory
jovian pull    # Pull the latest changes
```
