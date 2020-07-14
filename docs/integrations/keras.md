# Keras Integration

```eval_rst
.. meta::
   :description: Jovian.ml integration with keras.io
```

**Step 1** Import

```
import jovian
from jovian.callbacks.keras import JovianKerasCallback
```

**Step 2** Pass the callback to the fit method.

```
# To record logs of every epoch and to notify on slack
jvn_cb = JovianKerasCallback(arch_name='resnet18', every_epoch=True, notify=True)
model.fit(x_train, y_train, ...., callbacks=[jvn_cb])
```

For more details visit [Keras callback API reference](../callbacks/keras)

<img src="https://imgur.com/nXqaHH6.png" class="screenshot" alt="keras callback log">

**Step 3** Perform jovian commit

```
jovian.commit(message="keras callback")
```

**Step 4** View and compare experiment logs

View all the log of a certain version is the `Records Tab`

<img src="https://imgur.com/FJenNc1.png" class="screenshot" alt="keras records tab">

Compare the results of many expriments that you have performed. For more usage of compare details visit [Compare](../user-guide/compare)

<img src="https://i.imgur.com/m9zlfTJ.gif" class="screenshot" alt="compare records">
