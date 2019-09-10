## Contributing Guide

### Getting Started

This guide will help you setup and contribute to jovian.

**Step 1: Clone the repo:**

```
git clone git clone https://github.com/jvn-io/jovian-py.git
```

`cd` into the `jovian-py` folder:

```
cd jovian-py
```

**Step 2: Setup the Python environment for devolopment:**

Create a new Python environment using [conda](conda.io).

_Make sure you have [conda](https://docs.conda.io/en/latest/) setup on your pc_

```
conda create -n jovian-py-dev python=3.5 -y
```

Activate the environment:

```
conda activate jovian-py-dev
```

Install the dependencies by running:

```
pip install -r requirements.txt
```

To ensure that VSCode and other code editors use the correct conda environment, run the following command to add the path of the `jovian-py-dev` env to your `.bashrc` file:

```
echo -e "\n\nexport JOVIAN_PY_DEV_PYTHONPATH=$CONDA_PREFIX/bin/python" >> ~/.bashrc

source ~/.bashrc
```

The installation of dependencies is complete.
When working on jovian, please ensure that you activate the `jovian-py-dev` environment inside the `jovian-py` folder. You can deactivate the environment using:

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

_Make sure VSCode can be [launched from the command line](https://code.visualstudio.com/docs/setup/mac#_launching-from-the-command-line)_

We recommend using the following extensions in VSCode:

- [Python Extension](https://code.visualstudio.com/docs/languages/python)
- [autoDocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
- [Code Spell Checker](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker)
- [reStructured Text](https://marketplace.visualstudio.com/items?itemName=lextudio.restructuredtext)

Launch VSCode inside the folder type:

```
code .
```

### Contributing to Docs

The documentation website of Jovian is hosted at [jovian-py.readthedocs.io](https://jovian-py.readthedocs.io/en/latest/)

To run the docs server locally, run:

```
make run-docs
```

Once this command has run, you can view the docs here: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

The documentation is present in the `docs` folder.

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
