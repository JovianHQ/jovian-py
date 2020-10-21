## CLI Commands

CLI - Command line interface, is a text-based interface to interact with your system. On Mac/Linux based OS you'll have terminal application where these commands can be executed, on windows it'll be named as command prompt or conda prompt can be used if Anaconda has been installed.

These commands requires [installation](/user-guide/install.md) of jovian library, if you're working with pip/conda virtual environments make sure you activate the environment where the jovian library is installed.

These commands ensure that you can directly interact with [Jovian](https://jovian.ai) from CLI.

```eval_rst
.. meta::
   :description: Use Jovian from the command line.
.. click:: jovian.cli:main
    :prog: jovian
    :show-nested:
    :commands: clone, install, activate, pull, configure, set-project, commit, reset, add-slack, enable-extension, disable-extension, version, help
    :flat-toctree:
    :hide-options:
    :options-suffix:
    :skip-main-command:
```
