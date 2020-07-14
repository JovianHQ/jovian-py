# Github Integration

```eval_rst
.. meta::
   :description: Jovian.ml integration with github.com
```

[jovian.commit](../api-reference/commit) automatically performs [git commit](https://git-scm.com/docs/git-commit) if the current notebook/script is in a git repository, as `git_commit` is `True` by default and works only inside a git repository.

Use `git_message` parameter to give a different commit message to git, else it will take jovian's commit message by default.

```
jovian.commit(message="jovian version commit message",
              git_message="git commit message")
```

<img src="https://imgur.com/D1Dy17f.png" class="screenshot" alt="git commit from notebook">

Jovian also generates a link to the `git commit` associated to each `jovian commit` versions and is accessible with a button on the notebook linking to github/gitlab.

<img src="https://imgur.com/Stbaigk.png" class="screenshot" alt="git button on jovian">

```eval_rst
.. important::
        Jovian does not perform ``git push``, so if the asscociated link is not available then you'll have push your repo.
```
