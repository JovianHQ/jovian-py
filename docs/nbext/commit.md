# Use Extension to Commit

Inorder to use `jovian` extention you will need to first install Jovian on your system. Please visit [Installation](../user-guide/01-install.md) page before reading further.


#### Importing and Using Jovian Extention

**Step 1**: To import `jovian` type following command within a Jupyter notebook and run it.

```
import jovian
```

**Step 2**: After writing some code, you can save and commit your Jupyter notebook by running follwoing code. 

```
jovian.commit()
```

When running `jovian.commit` for first time you'll be prompted to provide an API key, which you can get from your [Jovian](https://jvn.io) (or Jovian Pro) account. By clicking on `API key` button, key will be copied to the clipboard.

<img src="https://i.imgur.com/taLLUVd.png" class="screenshot">

#### Here's what `jovian.commit` does:

It saves the current state of the notebook. It captures and uploads the required dependencies from the python environment and python environment itself. Capturing the python environment and dependencies ensures that the notebook can be reproduced and executed easily. Once the process has been completed a link will be displayed in a pop up, which you can use to view and share your notebook with friends or colleagues.


<img src="https://i.imgur.com/1cFeiC7.gif" class="screenshot">

