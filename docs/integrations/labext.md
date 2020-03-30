# Jupyter Lab Extension

Now you can commit your Jupyter Notebook to [Jovian](https://jovian.ml?utm_source=docs) with just **One Click**.
Make sure you’ve completed the [Installation](../user-guide/install.md) before reading further.

## Using Jovian Jupyter Lab Extension

<img src="https://i.imgur.com/uezsdYX.png" class="screenshot" alt="jupyter extension toolbar button">

Once you have successfully installed jovian, a new button `Commit` will appear on the tool bar. When using `Commit` button for first time you'll be asked to provide an API key.

<img src="https://i.imgur.com/jTvA0De.png" class="screenshot" alt="jovian api key prompt">

You can get the API key at [Jovian](https://jovian.ml?utm_source=docs). Once you log in, just click on `API key` button, and the key will be copied to the clipboard.

<img src="https://i.imgur.com/taLLUVd.png" class="screenshot" alt="jovian api key copy button">

#### Valid API key

If the key is valid you will be notified with the following alert.

<img src="https://i.imgur.com/lNKQO3G.png" class="screenshot" alt="valid api key prompt">

#### Error with API key

If the entered API key is invalid you will get following error.

<img src="https://i.imgur.com/PsMgrGI.png" class="screenshot" alt="api key error prompt">

#### Successful Commit

Once the API key has been validated, you can start committing to [Jovian](https://jovian.ml?utm_source=docs) by clicking `Commit` button. Once the Notebook has been committed successfully you will get the confirmation message with the link where the Jupyter Notebook has been uploaded to, you can click the link to your Notebook in Jovian.

<img src="https://i.imgur.com/BBesRzu.png" class="screenshot" alt="jovian commit success prompt">

## Commit with more options

This makes use of [jovian.commit's](../api-reference/commit) parameters to enable the user to commit with preferences like private notebook, new notebook project, to add outputs and files .....

**Step 1:** click the dropdown menu

<img src="https://i.imgur.com/GUgZGcS.png" class="screenshot" alt="jovian dropdown menu">

**Step 2:** choose `commit with options`

<img src="https://i.imgur.com/NzRMRH8.png" class="screenshot" alt="jovian commit options jupyter extension">

**Note:** By default the parameters are derived from [jovian.commit](https://jovian-py.readthedocs.io/en/latest/api-reference/commit.html), changes to any parameter persists after commit.

**Step 3:** Click on `Commit` to commit the notebook with following options.

<img src="https://i.imgur.com/XdVkMPZ.png" class="screenshot" alt="jupyter extension commit options prompt">

## Install Jovian Juputer Lab Extension

You can use NPM to install the extension by running the following command.

```
$ Coming soon
```

## Enable or Disable the extension

You can also disable the extension by running the following command.

```
$ jupyter labextension disable Jovian
```

To Enable the Notebook Extension, when you have manually disabled it.

```
$ jupyter labextension enable Jovian
```
