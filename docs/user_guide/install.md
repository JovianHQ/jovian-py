## Installation

### Jovian

Jovian can be installed using `pip` package manager.

To install Jovian via terminal or command line, run:

```
pip install jovian --upgrade
```

You can also install Jovian directly within a [Jupyter Notebook](https://jupyter.org/), by running the following command in a code cell:

```
!pip install jovian --upgrade
```

```eval_rst
.. caution::
    If you get a ``Permission denied`` error, try installing with sudo permission (on Linux/Mac).

    .. code-block::

        $ sudo pip install jovian --upgrade

```

### Jovian Pro Configuration

If you are a [Jovian Pro](pro.md) user, run the following commands inside a Jupyter notebook to configure credentials after the installation:

**Step 1**: Import the library

```
import jovian
```

**Step 2**: Configure the library

```
jovian.configure()
```

The above commands prompt for the following information:

1.  **Organization ID**: The Organization ID provided by your company for authentication. E.g. if you are accessing Jovian Pro at [https://mycompany.jvn.io](https://mycompany.jvn.io) , your organization ID is `mycompany`.

2.  **API key**: You'll get the API key when you're logged in to your organization's Jovian pro site. By clicking on the _API key_ button, the key will be copied to clipboard.

![](https://i.imgur.com/aI99Qmh.png)

To find out more, visit the [Jovian Pro](pro.md) section.
