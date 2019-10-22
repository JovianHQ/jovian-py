# Use Extension to Commit

Inorder to use `jovian` extension you will need to first install jovian on your system. Please visit [Installation](../user-guide/01-install.md) page before reading further.


#### Using Jovian Extension

Once you have sucessfully installed jovian, a new button `/j Commit` will appear on the tool bar. When using `/j Commit` button for first time you'll be asked to provide an API key.

                          
<img src="https://i.imgur.com/oNSowtY.png" class="screenshot">

 You can get the API key at [Jovian](jovian.ml). Once you log in, just click on `API key` button, and the key will be copied to the clipboard.

<img src="https://i.imgur.com/taLLUVd.png" class="screenshot">

#### Valid API key
If the key is valid you will be notified with the following alert.

<img src="https://i.imgur.com/UHvSihx.png" class="screenshot">

#### Error with API key
If the entered API key is invalid you will get follwwoing error.

<img src="https://i.imgur.com/9WaVkTR.png" class="screenshot">

#### Sucessful Commit
Once the API key has been validated, you can start commiting to Jovian by clicking `/j Commit` button. Once the document has been commited sucessfully you will be prompted with the following message. 
                            
<img src="https://i.imgur.com/4GoqzER.png" class="screenshot">

You can visit the link to view your notebook on Jovian. You can also copy the link with that copy button in the modal and share your notebook.


#### Here's what `/j Commit` button does:

It saves the current state of the notebook. It captures and uploads the required dependencies from the python environment and python environment itself. Capturing the python environment and dependencies ensures that the notebook can be reproduced and executed easily. Once the process has been completed a link will be displayed in a pop up, which you can use to view and share your notebook with friends or colleagues.




