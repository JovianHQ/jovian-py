# Fastai Integration

**Step 1** Import

```
import jovian
from jovian.callbacks.fastai import JovianFastaiCallback
```

**Step 2** Pass the callback to the fit method.

```
learn = cnn_learner(data, resnet34)
jvn_cb = JovianFastaiCallback(learn, 'res18')
learn.fit_one_cycle(5, callbacks = jvn_cb)
```

For more details visit [Fastai callback API reference](../callbacks/fastai)

**Step 3** Perform jovian commit

```
jovian.commit(message="fastai callback")
```

**Step 4** View and compare experiment logs

View all the log of a certain version is the `Records Tab`

<img src="https://imgur.com/FJenNc1.png" class="screenshot" alt="keras records tab">

Compare the results of many expriments that you have performed.For more usage of compare details visit [Compare](../user-guide/compare)

<img src="https://i.imgur.com/m9zlfTJ.gif" class="screenshot" alt="compare records">
