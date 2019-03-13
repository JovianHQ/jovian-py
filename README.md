# Jovian

Share jupyter notebooks instantly with a single command directly within Jupyter. Learn more on https://www.jvn.io .

## Getting Started

Install the `jovian` python library.

```bash
  pip install jovian --upgrade
```

Import the library into a Jupyter notebook.

```py
  import jovian
```

Use the `commit` command to capture and upload the Jupyter notebook and Python environment (Anaconda or pip).

```py
  jovian.commit()
```

You’ll be prompted for an API key, which you can generate by logging in here: https://jvn.io/login .

Once the notebook is uploaded successfully, you will get a shareable link to it. Other users can comment on parts of the notebook, and you'll get email notifications when they comment.

## Limitations

Since this is a beta release, the `jovian` library has some limitations:

- The library requires Python 3.6 or above
- The library must be used inside a Jupyter notebook
- Commits might fail if you use the "Run All" feature in Jupyter

## Coming Soon

- Callbacks for Tensorflow, Keras, PyTorch and FastAI to record hyperparameters and metrics automatically
- Full support for Windows, Python 2.7+, non-Anaconda environments and `.py` script files
- Real time monitoring and email/Slack notifications for long running training jobs
- Check out and reproduce tracked experiments on any machine with a single command

For feedback, suggestions and feature requests, drop us a line at hello@swiftace.ai .
