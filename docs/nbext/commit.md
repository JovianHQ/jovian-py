# Use Extension to Commit

Inorder to use `jovian` extension you will need to first install Jovian on your system. Please visit [Installation](../user-guide/01-install.md) page before reading further.


#### Using Jovian Extension

Once you have sucessfully installed Jovian a new button `/j Commit` will appear on the tool bar. 

When using `/j Commit` button for first time you'll be asked to provide an API key.

                          
<img src="https://i.imgur.com/oNSowtY.png" class="screenshot">

 You can get the API key at [Jovian](https://jvn.io). You will need to sign in using your github or google account. If you dont not either of this accounts you will need to sign up. Once you log in, just click on `API key` button, and the key will be copied to the clipboard.

<img src="https://i.imgur.com/taLLUVd.png" class="screenshot">

#### Valid API key
If the key is valid you will be notified with the following alert.

<img src="https://i.imgur.com/UHvSihx.png" class="screenshot">

#### Error with API key
IF the entered API key is invalid you will get follwwoing error.

<img src="https://i.imgur.com/9WaVkTR.png" class="screenshot">

#### Sucessful Commit
Once the API key has been validated, you can start commiting to Jovian by pressing `/j Commit` button. Once the document has been commited sucessfully you will be prompted with the following message. 
                            
<img src="https://i.imgur.com/4GoqzER.png" class="screenshot">


#### Enable or Disable Extension
By default, the jovian jupyter extension is enabled, but you may not be able to see `/j Commit` button due to diffrence in versions. You can simply run the following command in the terminal.

```
jupyter nbextension enable jovian_nb_ext/main
```
You can also disable the button by running the following command. 

```
jupyter nbextension disable jovian_nb_ext/main
```

The changes are observed when the webpage of the notebook is reloaded.


#### Here's what `/j Commit` button does:

It saves the current state of the notebook. It captures and uploads the required dependencies from the python environment and python environment itself. Capturing the python environment and dependencies ensures that the notebook can be reproduced and executed easily. Once the process has been completed a link will be displayed in a pop up, which you can use to view and share your notebook with friends or colleagues.




