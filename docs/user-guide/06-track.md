## Tracking Datasets, Hyperparameters and Metrics

Spreadsheets is one of the ways to track information & results of multiple ML experiments. However, using spreadsheets can be tiresome and non-intuitive without the context of the code.

Jovian makes its easy for anyone to track information about datasets, hyperparameters and metrics which are associated with each version of the your experiment in notebooks. Its also displays these information version-by-version of your notebook under single UI.

These information of a notebook are all added to `Records` Tab where you can toggle and view each version's log.

<!-- TODO: Add Pic.  -->

```
import jovian
```

### Dataset

```
data = {
    'path': '/datasets/mnist',
    'description': '28x28 gray-scale images of handwritten digits'
}
jovian.log_dataset(data)
```

### Hyperparameters

```
hyperparams = {
    'arch_name': 'cnn_1',
    'lr': .001
}
jovian.log_hyperparams(hyperparams)
```

### Metrics

```
metrics = {
    'epoch': 1,
    'train_loss': .5,
    'val_loss': .3,
    'acc': .94
}
jovian.log_metrics(metrics)
```

### Reset

If you're not satisfied with some experiment and want to discard the previously recorded parameters to start a fresh experiment. Use

```
jovian.reset()
```

The input to any of these can be a [python dict](https://docs.python.org/3/tutorial/datastructures.html#dictionaries). You can add custom parameters that are related to your experiment and have it record values manually, or automate it to record the values of a variable in a loop.
Visit [this](../jvn/logger.md) page for these logging API reference.

We have callbacks for [keras](../callbacks/keras.md) and [fastai](../callbacks/fastai.md) to automatically record hyperparams and metrics check it out.

Click `Next` to look at how to compare all of these information of all the versions.
