# Contributing Guide

## Development Setup

This guide will help you setup and contribute to jovian.

**Step 1: Clone the repository**

```
git clone https://github.com/JovianML/jovian-py.git
```

Move into the `jovian-py` folder:

```
cd jovian-py
```

**Step 2: Setup the Python environment for development**

Create a new Python environment using [conda](https://docs.conda.io/en/latest/).

_Make sure you have [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) setup on your pc_

```
conda create -n jovian-py-dev python=3.6 -y
```

Activate the environment:

```
conda activate jovian-py-dev
```

Install the dependencies by running:

```
pip install -r requirements.txt
```

To ensure that [VSCode](https://code.visualstudio.com/) and other code editors use the correct conda environment, run the following command to add the path of the `jovian-py-dev` env to your `.bashrc` file:

_Ensure that you have activated `jovian-py-dev` environment before running the following command_

```
echo -e "\n\nexport JOVIAN_PY_DEV_PYTHONPATH=$CONDA_PREFIX/bin/python" >> ~/.bashrc

source ~/.bashrc
```

The installation of dependencies is now complete.

When working on Jovian, please ensure that you activate the `jovian-py-dev` environment inside the `jovian-py` folder.

You can deactivate the environment using:

```
conda deactivate
```

**Step 3: Install CMake:**

Make sure you have `CMake` [installed](https://cmake.org/install/)

To test the installation, run the following command:

```
make help
```

This should print out:

![](https://i.imgur.com/9yFX3oh.png)

**Step 4: Setup Code Editor:**

We recommend using [VSCode](https://code.visualstudio.com/),
_Make sure VSCode can be [launched from the command line](https://code.visualstudio.com/docs/setup/mac#_launching-from-the-command-line)_.

We recommend using the following extensions in VSCode:

_Read more about VSCode Extensions [here](https://code.visualstudio.com/docs/editor/extension-gallery)_

- [Prettier - Code formatter](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) `Important` (To make the formatting consistent and avoid unwanted whitespace changes)
- [Python Extension](https://code.visualstudio.com/docs/languages/python)
- [autoDocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
- [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)
- [reStructured Text](https://marketplace.visualstudio.com/items?itemName=lextudio.restructuredtext)

Launch VSCode inside the folder type:

```
code .
```

## Contributing to Docs

The documentation website of Jovian is hosted at [jovian.com/docs](https://jovian.com/docs/)

To run the docs server locally, run:

```
make run-docs
```

Once this command has run, you can view the docs here: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

The documentation is present in the `docs` folder.

### Structure of the docs

- **`index.rst`**: is the home page of the docs website and it holds the structure for all content. If you'd like to add docs for a new function, please add docstring to that function and make the necessary changes here.
- **Structure**: Each section in the docs consists of a folder and each sub-section is formed by a Markdown file inside of the folder.
- **Docstring Style**: We follow [Google Style Docstring](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).

### Adding Documentation

- **Adding/Linking Docstring**: If the new function is of a existing file, you can add the same to the existing doc structure. Incase, if you'd like to create a new section, you can add the folder structure and link them in the `index.rst` file.
- **Autodoc**: We are using [Sphinx's autodoc](http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html) extension to import documentation to the docs website directly from the docstrings.
- **Adding Autodoc**:Visit the Markdown file where you want to import the docstring and add [`rst` autodoc directives](http://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html).
- **Embedding `rst` directives in `.md`**:
  Embed the directives with three backticks (`) followed by`eval_rst` below that please add all the directives that you'd like and close with three backticks in a new line.
  ````
  ```eval_rst
  .. autofunction:: jovian.commit
  ```
  ````
- **Embedding rst directives in Docstring**: You'd want to add [rst admonition](https://runawayhorse001.github.io/SphinxGithub/rtxt.html?highlight=admonition#admonitions) for attention, caution, note. reminder, etc.

  ```
  .. attention::
      Pass notebook's name to nb_filename argument, in certain environments like Jupyter Lab and password protected notebooks sometimes it may fail to detect notebook automatically.
  ```

- **Adding Examples in the Docstring**: Please add examples to the functions wherever possible.
  ```
  Example
      .. code-block::
          from jovian.callbacks.fastai_callback import FastaiCallback
          jvn_cb = FastaiCallback(learn, 'res18')
          learn.fit_one_cycle(5, callbacks = jvn_cb)
  ```
  \*Note that the `code-block` directive should be in the line after the `Example` along with a `tab` indentation, the code should be in the line after the `code-block` with a further tab indentation.

Check out these cheetsheets of [rst](https://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html) and [this for markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).

### Creating your docs preview

- Sign up for a [readthedocs account](https://readthedocs.org/).
- Connect the account with your GitHub account.
- Visit a project's admin settings
- Set the `Repository URL` as `https://github.com/JovianML/jovian-py`
- Goto Versions Tab
- Select the particular branch
- Set it to active
- Once the project is built, goto the versions tab, click on the branch under active versions.
- Include this link for a preview in your PR.

**Optional: Adding a git prompt**

To add a simple git prompt, add the following code to your bashrc:

```
# Bash git-branch
force_color_prompt=yes
color_prompt=yes
parse_git_branch() {
 git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}
if [ "$color_prompt" = yes ]; then
 PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[01;31m\]$(parse_git_branch)\[\033[00m\]\$ '
else
 PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w$(parse_git_branch)\$ '
fi
unset color_prompt force_color_prompt
```

This should give you a prompt that looks like this:

![](https://i.imgur.com/XRjzHEC.png)

For alternatives, We'd recommend checking out [bash-git-prompt](https://github.com/magicmonty/bash-git-prompt) but feel free to use one that you might like.
