# Submit assignments directly from jovian library

[Commit](upload.md) and submit assignments for <a href="https://jovian.com/learn" target=_blank>Courses hosted on Jovian</a> directly from Jupyter notebook. All you need is an `assignment` code (available in the respective assignment pages) that you need pass to `jovian.submit`.

**Example:**

```
import jovian

jovian.submit(assignment="zero-to-pandas-a1")
```

Incase you just need to submit a notebook already uploaded to Jovian, you can pass the `notebook_url` to just make the submission without committing the current notebook.

**Example:**

```
import jovian

jovian.submit(assignment="zero-to-pandas-a1",
              notebook_url="https://jovian.com/PrajwalPrashanth/assignment")
```

### Submit from Kaggle Kernels

`jovian.submit` works well for Local Jupyter notebooks/Colab/Binder, but it is not completely supported for Kaggle Kernels. Where you would have to do `jovian.commit` to commit and then do `jovian.submit` with the URL from `jovian.commit`.

**Example:**

```
import jovian

jovian.commit(....) # returns and prints the URL of the committed notebook
```

```
jovian.submit(assignment="zero-to-pandas-a1",
              notebook_url=<notebook_url_taken_from_commit>)
```
