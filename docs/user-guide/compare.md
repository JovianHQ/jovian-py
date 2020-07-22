## Comparing and Analyzing experiments

```eval_rst
.. meta::
   :description: Compare and analyze different versions of ML experiments with Jovian.
```

Once you have more than one [versions](version.md) of a notebook, you will be able to use `Compare Versions` present in the `Version` dropdown on the top right corner.

Here you can observe all types of information about all of your versions.

- Title
- Time of Creation
- Author
- All the parameters logged under dataset.
- All the parameters logged under hyperparameters.
- All the parameters logged under metrics.
- Notes (for author and collaborators add extra notes)

<img src="https://i.imgur.com/pkLzNum.png" class="screenshot" alt="notebooks compare versions" >

### Sort

You can sort any column or a sub-column (For ex: accuracy or any other metric, date of creation etc.) by clicking on the column header.

<img src="https://i.imgur.com/BblhF2n.gif" class="screenshot" alt="sort tracked metrics" >

### Show, Hide and Reorder columns

You can create a custom view to analyse & compare your choice of parameters.
Click on `Configure` button and then tick on the checkboxes to create a customized view. Click and drag the elements to reorder them based on your preference.

<img src="https://i.imgur.com/cVZU2Oe.gif" class="screenshot" alt="reorder results" >

### Add notes

You can add notes to summarize the experiment for reference
or for collaborators to refer to.

<img src="https://i.imgur.com/m9zlfTJ.gif" class="screenshot" alt="add notes to notebooks versions" >

### View Diff between specific versions

Select any of the 2 versions by ticking the checkbox next to each version-row of the compare table which can be seen when you hover over any row. Click on `View Diff` button to view the additions and deletion made.

<img src="https://i.imgur.com/bCSoyL4.gif" class="screenshot" alt="notebook version diffs" >

### Archive/Delete versions

Select version/versions by ticking the checkbox of the row/rows. This enables both `Archive` and `Delete` ready for the respective actions.

<img src="https://i.imgur.com/K9CEWGh.gif" class="screenshot" alt="archive and delete notebook versions" >

### Filter

By default all the archived versions are hidden, you can display them by enabling `Show Archived` in `Filter` dropdown.

<img src="https://i.imgur.com/eGarr8z.gif" class="screenshot" alt="Filter results" >
