# Jovian

[Jovian](www.jvn.io) is a platform that helps data scientists and ML engineers 

* track & reproduce data science projects
* collaborate easily with friends/colleagues, and
* automate repetitive tasks in their day-to-day workflow.


## Uploading your work to Jovian

It's really easy to get started with Jovian! 

### Step 1: Install the `jovian` python library

You can do this from the terminal, or directly within a Jupyter notebook.

```
!pip install jovian -q
```

### Step 2: Import the library

```
import jovian
```

### Step 3: Run jovian.commit

After writing some code, running some experiments, training some models and plotting some charts, you can save and commit your Jupyter notebook.

```
jovian.commit()
```

Here's what `jovian.commit` does:

* It saves and uploads the Jupyter notebook to your [Jovian](https://jvn.io) account.
* It captures and uploads the python virtual environment containing the list of libraries required to run your notebook.
* It returns a link that you can use to view and share your notebook with friends or colleagues.

**NOTE**: When you run `jovian.commit` for the first time, you'll be asked to provide an API, which you can find on [your Jovian account](https://jvn.io).


## Reproducing uploaded notebooks

Once a notebook is uploaded to Jovian, anyone (including you) can download the notebook and it's Python dependencies by running `jovian clone <notebook_id>` command on the Linux/Mac terminal or Windows Command Prompt. Try clicking the 'Clone' button at the top of this page to copy the command (including notebook ID) to clipboard. 

```
pip install jovian --upgrade
jovian clone 903a04b17036436b843d70443ef5d7ad
```

Once cloned, you can enter the directly and setup the virtual environment using `jovian install`.

```
cd jovian-demo
jovian install
```

Jovian uses [conda](https://conda.io) internally, so make sure you have it installed before running the above commands. Once the libraries are installed, you can activate the environment and start Jupyter in the usual way:

```
conda activate jovian-demo
jupyter notebook
```

In this way, Jovian seamlessly ensures the end-to-end reproducibility of your Jupyter notebooks.

## Updating existing notebooks

Updating existing notebooks is really easy too! Just run `jovian.commit` once again, and Jovian will automatically identify and update the current notebook on your Jovian account.

```
# Updating the notebook
jovian.commit()
```

Jovian keeps track of existing notebooks using a `.jovianrc` file next to your notebook. If you don't want to update the current notebook, but create a new notebook instead, simply delete the `.jovianrc` file. Note that if you rename your notebook, Jovian will upload a new notebooko when you commit, instead of updating the old one.

If you run into issues with updating a notebook, or want to replace a notebook in your account using a new/renamed notebook, you can provide the `notebook_id` argument to `jovian.commit`.

```
jovian.commit(notebook_id="903a04b17036436b843d70443ef5d7ad")
```

## Getting new changes on cloned notebooks

Once a notebook has been updated, the new changes can be retrieved at any cloned location using the `jovian pull` command.

```
cd jovian-demo # Enter cloned directory
jovian pull    # Pull the latest changes
```


## Coming Soon

- Callbacks for Tensorflow, Keras, PyTorch and FastAI to record hyperparameters and metrics automatically
- Full support for Windows, Python 2.7+, non-Anaconda environments and `.py` script files
- Real time monitoring and email/Slack notifications for long running training jobs
- Check out and reproduce tracked experiments on any machine with a single command

For feedback, suggestions and feature requests, drop us a line at hello@jvn.io or create a ticket in the [issues tab](https://github.com/jvn-io/jovian-py/issues) .


## Development and Testing   
To run the tests, run the following command in the project directory    
`python -m unittest discover`     [`-v` for verbose]

