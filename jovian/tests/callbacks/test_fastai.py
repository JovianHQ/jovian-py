import sys
from unittest import mock
from unittest.mock import ANY

import pytest
try:
    from fastai import *
    from fastai.vision import *
    from jovian.callbacks.fastai import JovianFastaiCallback
except ImportError:
    print('fastai needs Python 3.6 or higher')
    pass


@pytest.fixture
def learn():
    mnist = untar_data(URLs.MNIST_TINY)
    tfms = get_transforms(do_flip=False)

    data = (ImageList.from_folder(mnist)
            .split_by_folder()
            .label_from_folder()
            .transform(tfms, size=32)
            .databunch()
            .normalize(imagenet_stats))

    learn = cnn_learner(data, models.resnet18, metrics=accuracy)
    return learn


@pytest.mark.skip(reason="need to deal with latest version of torch and torchvision")
@mock.patch("jovian.callbacks.fastai.log_hyperparams")
@mock.patch("jovian.callbacks.fastai.log_metrics")
def test_on_train_begin_and_on_epoch_end(mock_log_metrics, mock_log_hyperparams, learn):
    jvn_cb = JovianFastaiCallback(learn, 'res18')
    learn.fit_one_cycle(1, callbacks=jvn_cb)

    mock_log_hyperparams.assert_called_with({
        'epochs': 1,
        'batch_size': 64,
        'loss_func': 'CrossEntropyLoss()',
        'opt_func': 'torch.optim.adam.Adam',
        'weight_decay': 0.01,
        'learning_rate': '0.003',
        'arch_name': 'res18'})

    mock_log_metrics.assert_called_with({
        'epoch': 0,
        'train_loss': ANY,
        'valid_loss': ANY,
        'accuracy': ANY})
