## Attaching files and model outputs

As seen in the previous section by committing, source code and environment files are uploaded.
More files can be attached to the notebook like files with helper code, output files that the notebook is generating.

### How to attach these files?

```
jovian.commit(files=[], artifacts=[])
```

**TODO-SB: Committing with files and artifacts argument**

### What files to include in files argument?

The type of files which is required to run the notebook.

- Helper code (.py)
- Some input CSVs
- ....

### What files to include in artifacts argument?

Any type of outputs that the notebook is generating.

- Saved model or weights (.h5, .pkl, .pth)
- Outputs, Submission CSVs
- Images outputs
- ...

### Where to search for the files after committing?

All the attached files are listed under `Files` Tab.

**Files can be:**

1. Renamed
2. Downloaded
3. Deleted
4. View Raw
5. Uploaded

**TODO-SB: Visiting, opening, renaming, downloading those files in webapp**
