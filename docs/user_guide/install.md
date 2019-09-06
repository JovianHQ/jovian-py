## Installation

### Jovian

Jovian can be installed using `pip` package manager.

To install via terminal

```
$ pip install jovian --upgrade
```

To install via Jupyter Notebook, you can run the following command in a cell.

```
!pip install jovian --upgrade
```

```eval_rst
.. caution::
    If you come across ``Permission denied`` error, install with sudo permission.

    .. code-block::

        $ sudo pip install jovian --upgrade

```

**TODO-SB: Add gif of Installation.**

### Jovian-pro

The following command is only for a Jovian-pro user, to configure credentials after the installation of Jovian from the previous section.

Find out more about [Jovian-pro](pro.md).

#### Step 1: Import the library

```
import jovian
```

#### Step 2: Configure

```
jovian.configure()
```

The above commands prompts for

1.  Organization ID: Your organization id provided for authentication.
2.  API key: You'll get the API key when you're logged on in website. By clicking on the API key button key will be copied to clipboard.

**TODO-SB: Add gif of configure**
