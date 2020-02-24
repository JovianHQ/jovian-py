## Tracking Datasets, Hyperparameters and Metrics

Spreadsheets is one of the ways to track information & results of multiple ML experiments. However, using spreadsheets can be tiresome and non-intuitive without the context of the code.

<a href="https://jovian.ml?utm_source=docs" target=_blank> Jovian.ml </a> makes its easy for anyone to track information about datasets, hyperparameters and metrics which are associated with each version of the your experiment in notebooks. Its also displays these information version-by-version of your notebook under single UI.

These information of a notebook are all added to `Records` Tab where you can toggle and view each version's log.

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

<img src="https://i.imgur.com/57BxYjH.gif" class="screenshot" alt="jovian track datasets, hyperparameters and metrics" >

The input to any of these can be a <a href="https://docs.python.org/3/tutorial/datastructures.html#dictionaries" target="_blank"> python dict </a>. You can add custom parameters that are related to your experiment and have it record values manually, or automate it to record the values of a variable in a loop.
Visit [this](../jvn/logger.md) page for these logging API reference.

We have callbacks for [keras](../callbacks/keras.md) and [fastai](../callbacks/fastai.md) to automatically record hyperparams and metrics check it out.

### Reset

If you're not satisfied with some experiment and want to discard the current recorded logs before a commit. Use

```
jovian.reset()
```

Click `Next` to look at how to compare all of these information of all the versions.
