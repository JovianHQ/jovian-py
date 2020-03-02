# Jupyter Notebook Extension

Now you can commit your Jupyter Notebook with to [Jovian](https://jovian.ml?utm_source=docs) just **One Click**.
Make sure you’ve completed the [Installation](https://jovian-py.readthedocs.io/en/latest/user-guide/01-install.html) before reading further.

## Using Jovian Jupyter Extension

<img src="https://i.imgur.com/44QTHP6.png" class="screenshot" alt="jupyter extension toolbar button">

Once you have successfully installed jovian, a new button `Commit` will appear on the tool bar. When using `Commit` button for first time you'll be asked to provide an API key.

<img src="https://i.imgur.com/oNSowtY.png" class="screenshot" alt="jovian api key prompt">

You can get the API key at [Jovian](https://jovian.ml?utm_source=docs). Once you log in, just click on `API key` button, and the key will be copied to the clipboard.

<img src="https://i.imgur.com/taLLUVd.png" class="screenshot" alt="jovian api key copy button">

#### Valid API key

If the key is valid you will be notified with the following alert.

<img src="https://i.imgur.com/UHvSihx.png" class="screenshot" alt="valid api key prompt">

#### Error with API key

If the entered API key is invalid you will get following error.

<img src="https://i.imgur.com/9WaVkTR.png" class="screenshot" alt="api key error prompt">

#### Successful Commit

Once the API key has been validated, you can start committing to [Jovian](https://jovian.ml?utm_source=docs) by clicking `Commit` button. Once the Notebook has been committed successfully you will get the confirmation message with the link where the Jupyter Notebook has been uploaded to, you can use the copy button to get the link to the share the notebook.

<img src="https://i.imgur.com/4GoqzER.png" class="screenshot" alt="jovian commit success prompt">

## Commit with more options

This makes use of [jovian.commit's](https://jovian-py.readthedocs.io/en/latest/jvn/commit.html) parameters to enable the user to commit with preferences like private notebook, new notebook project, to add outputs and files .....

Firstly, click the dropdown menu

<img src="https://i.imgur.com/C4trCHn.png" class="screenshot" alt="jovian dropdown menu">

Then, choose **commit with options**

<img src="https://i.imgur.com/MAbD0aB.png" class="screenshot" alt="jovian commit options jupyter extension">

By default the parameters are derived from [jovian.commit](https://jovian-py.readthedocs.io/en/latest/jvn/commit.html), once the user changes a certain parameter they are retained.

<img src="https://i.imgur.com/3C7dokb.png" class="screenshot" alt="jupyter extension commit options prompt">

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
