## Uploading Jupyter Notebooks to Jovian

Jovian allows you to upload and share [Jupyter notebooks](https://jupyter.org/) instantly with a single command, directly within Jupyter. Make sure you've completed the [installation](01-install.md) before reading further.

#### Uploading Notebooks

**Step 1**: Import `jovian` by running the following command within a Jupyter notebook.

```
import jovian
```

**Step 2**: After writing some code, running some experiments, training some models and plotting some charts, you can save and commit your Jupyter notebook.

```
jovian.commit()
```

When you run `jovian.commit` for the first time you'll be asked to provide an API key, which you can get from your [Jovian](https://jovian.ml?utm_source=docs) (or Jovian Pro) account.

<img src="https://i.imgur.com/taLLUVd.png" class="screenshot">

Here's what `jovian.commit` does:

- It saves and uploads the Jupyter notebook to your Jovian (or Jovian Pro) account.
- It captures and uploads the python virtual environment containing the list of libraries required to run your notebook.
- It returns a link that you can use to view and share your notebook with friends or colleagues.

<img src="https://i.imgur.com/1cFeiC7.gif" class="screenshot">

<!-- TODO: Redo the GIF -->

For more features of `jovian.commit` and API reference visit [Commit](../jvn/commit.md).

```eval_rst
.. attention::
        In certain environments like JupyterLab and password protected notebooks, ``jovian`` may not be able to detect the notebook filename automatically. In such cases, pass the notebook's name as the ``nb_filename`` argument to ``jovian.commit``.
```

#### Benefits of Jovian

**Easy sharing and collaboration**: Just copy the link to share an uploaded notebook with your friends or colleages. Your notebooks are also visible on your profile page, unless you mark them _Secret_. You can also add collaborators and let others contribute to your project ([learn more](08-collaborate.md)).

<img src="https://i.imgur.com/D6JU35G.gif" class="screenshot">

**Cell-level comments and discussions**: Jovian's powerful commenting interface allows your team to discuss specific parts of a notebook with cell-level comment threads. Just hover over a cell and click the _Comment_ button. You'll receive an email when someone comments on your notebook, or replies to your comment.

<img src="https://i.imgur.com/15vj2qv.png" class="screenshot">

**End-to-end reproducibility**:
Jovian automatically captures Python libraries used in your notebook, so anyone (including you) can reproduce your work on any computer with a single command: `jovian clone`. You can also use the 'Run' dropdown on the Jovian notebook page to run your notebooks on free cloud GPU platforms like Google Colab, Kaggle Kernels and BinderHub.

<img src="https://i.imgur.com/kGPlFCp.png" class="screenshot">

This is just a small selection of features that Jovian offers. Continue reading by clicking the `Next ->` button to learn more, or use the sidebar to jump to a specific section.
