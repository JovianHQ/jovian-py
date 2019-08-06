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

- It saves and uploads the Jupyter notebook to your [Jovian](https://jvn.io) account.
- It captures and uploads the python virtual environment containing the list of libraries required to run your notebook.
- It returns a link that you can use to view and share your notebook with friends or colleagues.

**NOTE**: When you run `jovian.commit` for the first time, you'll be asked to provide an API, which you can find on [your Jovian account](https://jvn.io).
