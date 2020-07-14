## Installation

```eval_rst
.. meta::
   :description: Install Jovian python library to collaborate, track versions of online jupyter notebooks
```

The `jovian` python library can be installed using the `pip` package manager. To install `jovian` via terminal or command line, run:

```
pip install jovian --upgrade
```

You can also install the `jovian` library directly within a <a href="https://jupyter.org/" target=_blank> Jupyter Notebook</a>, by running the following command in a code cell:

```
!pip install jovian --upgrade
```

```eval_rst
.. caution::
    If you get a ``Permission denied`` error, try installing with sudo permission (on Linux/Mac).

    .. code-block::

        $ sudo pip install jovian --upgrade

    Another alternative is to try installing with the ``--user`` flag, but you'll need to ensure that the target directory is added to your system ``PATH``.

    .. code-block::

        $ pip install jovian --upgrade --user
```

Once the installation is complete, you can start [uploading Jupyter notebooks to Jovian](upload.md).

**Configuration (for Jovian Pro users only)**

If you are a [Jovian Pro](pro.md) user, run the following commands on the terminal (or command line) to connect the `jovian` library with your company's internal Jovian Pro site:

```
jovian configure
```

You can also do this directly within a Jupyter notebook, by executing the following inside a code cell:

```
import jovian
jovian.configure()
```

The above command prompts for the following information:

1.  **Organization ID**: The Organization ID provided by your company for authentication. E.g. if you are accessing Jovian Pro at [https://mycompany.jovian.ml](https://mycompany.jovian.ml?utm_source=docs) , your organization ID is `mycompany`.

2.  **API key**: You'll get the API key when you're logged in to your organization's Jovian Pro site. By clicking on the _API key_ button, the key will be copied to clipboard.

<img src="https://i.imgur.com/taLLUVd.png" class="screenshot" alt="jovian api key button" >

```eval_rst
.. note::
    You need to run ``jovian configure`` or ``jovian.configure()`` only once after installation. Your credentials are cached in the ``~/.jovian`` directory on your computer. You can run ``jovian reset`` to clear this configuration.

```

You can learn more about Jovian Pro [here](pro.md), or start [uploading Jupyter notebooks to Jovian](upload.md) in the next section.
