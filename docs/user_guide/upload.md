## Uploading Jupyter Notebooks to Jovian

Once you're done with the [installation](install.md).
The following steps will help you upload the notebook to Jovian. If you're not signed up yet, you should do it at [Jovian](https://www.jvn.io) to use the following.

### Upload

#### Step 1: Import the library

```
import jovian
```

#### Step 2: Commit

Once you done with writing code and running some experiment, you can upload a version to Jovian.
When doing this for the first you'll be asked for the API key, can get it from [Jovian](https://jvn.io).

**TODO-SB: Add gif to copy API key from webapp**

```
jovian.commit()
```

- Saves the checkpoint of your notebook.
- Captures source code, python environment.
- Uploads it to [Jovian](https://jvn.io) and returns a link to your notebook.

**TODO-SB: Add gif for committing**

For more features of commit and API reference visit [Commit](../jvn/commit.md).

```eval_rst
.. attention::
        Pass notebook's name to nb_filename argument, in certain environments like Jupyter Lab and password protected notebooks sometimes it may fail to detect notebook automatically.
```

### What are the benefits of uploading to Jovian?

**TODO-AA: Add more points ideally things of webapp**

#### Share the notebooks with ease

Uploaded notebooks can be public/secret. You can get stars from the people who benefit from your notebook.

Secret Notebooks(Private) won't be on your public profile but anyone with the link can access it.

**TODO-SB: GIF for Sharing notebooks, making them secret/public**

#### Collaborate with teammates/colleagues

Team up and add collaborators.
Even they can add their version of notebook to the same project.

**TODO-SB: GIF for adding Collaborators**

#### Comment on individual code cells

Users can comment on any code cells individually and maintain that thread to have specific discussion about a part of the source code with context.

**TODO-SB: GIF for commenting on notebook cells**

There are many more benefits follow the pages in this section to know more. You can click `Next ->` button or use the side bar `GETTING STARTED` section.
