# Use Extension to Commit

Inorder to use `jovian` extention you will need to first install Jovian on your system. Please visit [Installation](../user-guide/01-install.md) page before reading further.


#### Using Jovian Extention

Once you have sucessfully installed Jovian a new button `/j Commit` will appear on the tool bar. 

When using `/j Commit` button for first time you'll be prompted to provide an API key, which you can get from your [Jovian](https://jvn.io) (or Jovian Pro) account. By clicking on `API key` button, key will be copied to the clipboard.

<img src="https://i.imgur.com/taLLUVd.png" class="screenshot">


By default, the jovian jupyter extension is enabled, but you may not be able to see `/j Commit` button due to diffrence in versions. You can simply run the following command in the terminal.

```
$ jovian enable-ext
```
You can also disable the button by running the following command. 

```
$ jovian disable-ext
```

The changes are observed when the webpage of the notebook is refreshed.


#### Here's what `/j Commit` button does:

It saves the current state of the notebook. It captures and uploads the required dependencies from the python environment and python environment itself. Capturing the python environment and dependencies ensures that the notebook can be reproduced and executed easily. Once the process has been completed a link will be displayed in a pop up, which you can use to view and share your notebook with friends or colleagues.




