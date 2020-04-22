# Jovian: The platform for all your Data Science projects

![](/docs/jovian_horizontal_logo.svg)

jovian is an open-source Python package integrated with [Jovian](https://jovian.ml/?utm_source=github) to provide the tools necessary for Data Scientists and ML/DL Engineers to **Track**, **Collaborate** and **Automate** projects where even Students and Enthusiasts can leverage the same and also use [Jovian](https://jovian.ml/?utm_source=github) **Share** and **Showcase** their projects.

- [Upload and share Jupyter Notebooks](https://jovian-py.readthedocs.io/en/latest/user-guide/02-upload.html)
- [Reproduce Notebooks from Jovian](https://jovian-py.readthedocs.io/en/latest/user-guide/03-reproduce.html)
- [Notebooks as version, view Diffs between versions](https://jovian-py.readthedocs.io/en/latest/user-guide/04-version.html)
- [Attaching utility files and model outputs with the Notebook](https://jovian-py.readthedocs.io/en/latest/user-guide/05-attach.html)
- [Tracking Datasets, Hyperparameters and Metrics](https://jovian-py.readthedocs.io/en/latest/user-guide/06-track.html)
- [Comparing and Analyzing all the experiments](https://jovian-py.readthedocs.io/en/latest/user-guide/07-compare.html)
- [Collaborate with teammates/colleagues](https://jovian-py.readthedocs.io/en/latest/user-guide/08-collaborate.html)
- [Stay connected with your model training, live updates with Slack Notifications](https://jovian-py.readthedocs.io/en/latest/jvn/notif.html)

[![Documentation Status](https://readthedocs.org/projects/jovian-py/badge/?version=latest)](https://jovian-py.readthedocs.io/en/latest/?badge=latest)

## Installation

```
pip install jovian --upgrade
```

> **Caution**:
>
> If you get a `Permission denied` error, try installing with sudo permission (on Linux/Mac).
>
> ```
> sudo pip install jovian --upgrade
> ```
>
> Another alternative is to try installing with the `--user` flag, but you’ll need to ensure that the target directory is added to your system `PATH`.
>
> ```
> pip install jovian --upgrade --user
> ```

Visit [Docs](https://jovian-py.readthedocs.io) for more.

## Contact

Mail : hello@jovian.ml
<br>
Twitter : [@JovianML](https://twitter.com/JovianML)
<br>
Slack : [Slack Invite](https://bit.ly/jovian-users)

## Requirements

- JupyterLab >= 0.30.0
- Jovian >= 0.1.89
- nodejs >= 10.20.0

# Jupyter Lab Extension

Now you can commit your Jupyter Notebook to [Jovian](https://jovian.ml?utm_source=docs) with just **One Click**.
Make sure you’ve completed the [Installation](../user-guide/01-install.md) before reading further.

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

## _Comming Soon!_
## Commit with more options

This makes use of [jovian.commit's](../jvn/commit) parameters to enable the user to commit with preferences like private notebook, new notebook project, to add outputs and files .....

**Step 1:** click the dropdown menu

<img src="https://i.imgur.com/GUgZGcS.png" class="screenshot" alt="jovian dropdown menu">

**Step 2:** choose `commit with options`

<img src="https://i.imgur.com/NzRMRH8.png" class="screenshot" alt="jovian commit options jupyter extension">

**Note:** By default the parameters are derived from [jovian.commit](https://jovian-py.readthedocs.io/en/latest/jvn/commit.html), changes to any parameter persists after commit.

**Step 3:** Click on `Commit` to commit the notebook with following options.

<img src="https://i.imgur.com/XdVkMPZ.png" class="screenshot" alt="jupyter extension commit options prompt">

## Install Jovian Juputer Lab Extension

You can install the extension by running the following command.

```shell
$ jupyter labextension install jovian-lab-ext-test
```

## Enable or Disable the extension

You can also disable the extension by running the following command.

```
$ jupyter labextension disable jovian-lab-ext-test
```

To Enable the Notebook Extension, when you have manually disabled it.

```
$ jupyter labextension enable jovian-lab-ext-test
```

## Contributing

### Install

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Move to jovian-lab-ext-test directory
# Install dependencies
jlpm
# Build Typescript source
jlpm build
# Link your development version of the extension with JupyterLab
jupyter labextension link .
# Rebuild Typescript source after making changes
jlpm build
# Rebuild JupyterLab after making any changes
jupyter lab build
```

You can watch the source directory and run JupyterLab in watch mode to watch for changes in the extension's source and automatically rebuild the extension and application.

```bash
# Watch the source directory in another terminal tab
jlpm watch
# Run jupyterlab in watch mode in one terminal tab
jupyter lab --watch
```

### Uninstall

```bash
jupyter labextension uninstall jovian-lab-ext-test
```
