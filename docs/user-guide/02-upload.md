## Uploading Jupyter Notebooks to Jovian

Jovian allows you to upload and share [Jupyter notebooks](https://jupyter.org/) instantly with a single command, directly within Jupyter notebook. Make sure you've completed the [installation](01-install.md) before reading further.

### Uploading a Notebook

**Step 1**: Import `jovian` by running the following command within a Jupyter notebook.

```
import jovian
```

**Step 2**: After writing some code, running some experiments, training some models and plotting some charts, you can save and commit your Jupyter notebook.

```
jovian.commit()
```

When you run `jovian.commit` for the first time you'll be asked to provide an API key, which you can get from your [Jovian](https://jvn.io) (or Jovian Pro) account.

<img src="https://i.imgur.com/taLLUVd.png" class="screenshot">

Here's what `jovian.commit` does:

- It saves and uploads the Jupyter notebook to your Jovian (or Jovian Pro) account.
- It captures and uploads the python virtual environment containing the list of libraries required to run your notebook.
- It returns a link that you can use to view and share your notebook with friends or colleagues.

![](https://i.imgur.com/JUMvVMd.gif)

<!-- TODO: Redo the GIF -->

For more features of `jovian.commit` and API reference visit [Commit](../jvn/commit.md).

```eval_rst
.. attention::
        In certain environments like JupyterLab and password protected notebooks, ``jovian`` may not be able to detect the notebook filename automatically. In such cases, pass the notebook's name as the ``nb_filename`` argument to ``jovian.commit``.
```

### What are the benefits of uploading to Jovian?

#### Share the notebooks with ease

Uploaded notebooks can be public/secret. You can get stars from the people who benefit from your notebook.

Secret Notebooks(Private) won't be on your public profile but anyone with the link can access it.

<!-- TODO-SB: GIF for Sharing notebooks, making them secret/public -->

#### Collaborate with teammates/colleagues

Team up and add collaborators.
Even they can add their version of notebook to the same project.

<!-- **TODO-SB: GIF for adding Collaborators** -->

#### Comment on individual code cells

Users can comment on any code cells individually and maintain that thread to have specific discussion about a part of the source code with context.

<!-- **TODO-SB: GIF for commenting on notebook cells** -->

There are many more benefits follow the pages in this section to know more. You can click `Next ->` button or use the side bar `GETTING STARTED` section.
