# Jupyter Notebook Extension

Now you can commit your Jupyter Notebook with to [Jovian](https://jovian.ml?utm_source=docs) just **One Click**.
Make sure you’ve completed the [Installation](../user-guide/01-install.md) before reading further.

## Using Jovian Jupyter Extension

<img src="https://i.imgur.com/RdBnJYy.png" class="screenshot">

Once you have successfully installed jovian, a new button `Commit` will appear on the tool bar. When using `Commit` button for first time you'll be asked to provide an API key.
  
<img src="https://i.imgur.com/oNSowtY.png" class="screenshot">

You can get the API key at [Jovian](https://jovian.ml?utm_source=docs). Once you log in, just click on `API key` button, and the key will be copied to the clipboard.

<img src="https://i.imgur.com/taLLUVd.png" class="screenshot">

#### Valid API key

If the key is valid you will be notified with the following alert.

<img src="https://i.imgur.com/UHvSihx.png" class="screenshot">

#### Error with API key

If the entered API key is invalid you will get following error.

<img src="https://i.imgur.com/9WaVkTR.png" class="screenshot">

#### Successful Commit

Once the API key has been validated, you can start committing to [Jovian](https://jovian.ml?utm_source=docs) by clicking `Commit` button. Once the Notebook has been committed successfully you will get the confirmation message with the link where the Jupyter Notebook has been uploaded to, you can use the copy button to get the link to the share the notebook.
  
<img src="https://i.imgur.com/4GoqzER.png" class="screenshot">

## Commit Dropdown to commit with more options

This makes use of [jovian.commit's](../jvn/commit) parameters to enable the user to commit with preferences like secret notebook, new notebook project, to add output and artifact files .....

<img src="https://i.imgur.com/maHhYY2.png" class="screenshot">

By default the parameters are derived from [jovian.commit](../jvn/commit), once the user changes a certain parameter they are retained.

<img src="https://i.imgur.com/2NKfNGB.png" class="screenshot">

Once the parameters are set to the need click `Commit` to the commit the notebook with these parameters set.

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
## Jovian Settings

Jovian settings are accessed in in the dropdown
<img src="https://i.imgur.com/dnu5qkY.png" class="screenshot">

<img src="https://i.imgur.com/iDFrZsd.png" class="screenshot">

### Set Default Commit Parameters

Sets the Parameters for Commit without Commiting to Jovian.
<img src="https://i.imgur.com/al3f6gU.png" class="screenshot">

### Clear Api Key

Clears the API key.
<img src="https://i.imgur.com/DPAR6rh.png" class="screenshot">

### Change Api Key

Allows the API key to be changed.
<img src="https://i.imgur.com/kfAtxFE.png" class="screenshot">

### Disable Jovian Extension

Disables the jovian Extension
<img src="https://i.imgur.com/n98LRMW.png" class="screenshot">

Can be reversed by running `!jovian enable` in the notebook
