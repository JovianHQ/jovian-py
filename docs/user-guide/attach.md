## Attaching files and model outputs

As seen in the [previous section](04-version.md) by committing, source code and environment files are captured & uploaded.
More files can be attached to the notebook such as files with helper code, output files/model checkpoints that the notebook is generating.

### How to attach files?

```
jovian.commit(files=[], outputs=[])
```

<img src="https://i.imgur.com/giVFiKw.gif" class="screenshot" alt="attach csv, images to notebook versions" >

### What to include in the `files` argument?

The type of files which is required to run the notebook.

- Helper code (.py)
- Some input CSVs

### What to include in the artifacts argument?

Any type of outputs that the notebook is generating.

- Saved model or weights (.h5, .pkl, .pth)
- Outputs, Submission CSVs
- Images outputs

### Where to search for the files after committing?

All the attached files are listed under `Files` Tab.

**Files can be:**

1. Renamed
2. Downloaded
3. Deleted
4. View Raw
5. Uploaded
