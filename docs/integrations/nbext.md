# Jupyter Notebook Extension

```eval_rst
.. meta::
   :description: Jovian integration with Jupyter Notebook.
```

Now you can commit your Jupyter Notebook to [Jovian](https://jovian.ai?utm_source=docs) with just **One Click**.
Make sure you’ve completed the [Installation](../user-guide/install.md) before reading further.

## Using Jovian Jupyter Extension

<img src="https://i.imgur.com/6ZcKly7.png" class="screenshot" alt="jupyter extension toolbar button">

Once you have successfully installed jovian, a new button `Commit` will appear on the tool bar. When using `Commit` button for first time you'll be asked to provide an API key.

<img src="https://i.imgur.com/oNSowtY.png" class="screenshot" alt="jovian api key prompt">

You can get the API key at [Jovian](https://jovian.ai?utm_source=docs). Once you log in, just click on `API key` button, and the key will be copied to the clipboard.

<img src="https://i.imgur.com/taLLUVd.png" class="screenshot" alt="jovian api key copy button">

#### Valid API key

If the key is valid you will be notified with the following alert.

<img src="https://i.imgur.com/UHvSihx.png" class="screenshot" alt="valid api key prompt">

#### Error with API key

If the entered API key is invalid you will get following error.

<img src="https://i.imgur.com/9WaVkTR.png" class="screenshot" alt="api key error prompt">

#### Successful Commit

Once the API key has been validated, you can start committing to [Jovian](https://jovian.ai?utm_source=docs) by clicking `Commit` button. Once the Notebook has been committed successfully you will get the confirmation message with the link where the Jupyter Notebook has been uploaded to, you can use the copy button to get the link to the share the notebook.

<img src="https://i.imgur.com/4GoqzER.png" class="screenshot" alt="jovian commit success prompt">

## Commit with more options

This makes use of [jovian.commit's](../api-reference/commit) parameters to enable the user to commit with preferences like private notebook, new notebook project, to add outputs and files .....

**Step 1:** click the dropdown menu

<img src="https://i.imgur.com/svBbgsT.png" class="screenshot" alt="jovian dropdown menu">

**Step 2:** choose `commit with options`

<img src="https://i.imgur.com/jZEpIjl.png" class="screenshot" alt="jovian commit options jupyter extension">

**Note:** By default the parameters are derived from [jovian.commit](../api-reference/commit), changes to any parameter persists after commit.

**Step 3:** Click on `Commit` to commit the notebook with following options.

<img src="https://i.imgur.com/Fgkvk5b.png" class="screenshot" alt="jupyter extension commit options prompt">

## Enable or Disable the extension

By default, the Jovian Jupyter Notebook Extension is enabled to the environment where jovian is installed.

You can also disable the extension by running the following command.

```
$ jovian disable-extension
```

To Enable the Notebook Extension, when you have manually disabled it.

```
$ jovian enable-extension
```

<!-- ## Commit with Share Dialog

After you have succesfully commited your notebook to [Jovian](https://jovian.ai?utm_source=docs), you can share your notebook to social media.

The following window will appear, providing the user with the options to share the notebook to facebook, twitter, or linkedin.

<img src="https://i.imgur.com/FUUk82w.png" class="screenshot" alt="Share Dialog Window" >

Once the facebook button is click. A share post will appear, providing the choice to add a description to the share notebook.

<img src="https://i.imgur.com/4EfyHbn.png" class="screenshot" alt="Facebook post" >

If the Linkedin buttton is click. A share post will appear, providing the choice to add a description to the share notebook.

<img src="https://i.imgur.com/uwZxy1Y.png" class="screenshot" alt="Linked post" >

If the twitter button is click. A share post will appear, also providing the choice to add description text to the tweet.

<img src="https://i.imgur.com/HVP6t4M.png" class="screenshot" alt="Twitter post" >

Finally you will see your tweet display.

<img src="https://i.imgur.com/Qg0TUU3.png" class="screenshot" alt="Twitter post" > -->

<!-- ## Jovian Settings

Jovian settings are accessed in in the dropdown
<img src="https://i.imgur.com/dnu5qkY.png" class="screenshot">

<img src="https://i.imgur.com/iDFrZsd.png" class="screenshot">

### Set Default Commit Parameters

Sets the Parameters for Commit without Committing to Jovian.
<img src="https://i.imgur.com/al3f6gU.png" class="screenshot">

### Clear Api Key

Clears the API key.
<img src="https://i.imgur.com/DPAR6rh.png" class="screenshot">

### Change Api Key

Allows the API key to be changed.
<img src="https://i.imgur.com/kfAtxFE.png" class="screenshot"> -->
