import os
import sys
from unittest import mock
from unittest.mock import ANY
from pathlib import PosixPath
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
    data = (ImageList.from_folder(PosixPath("./jovian/tests/resources/mnist_tiny"))
            .split_by_folder()
            .label_from_folder()
            .databunch()
            .normalize(imagenet_stats))
    data.batch_size = 2

    learn = cnn_learner(data, models.resnet18, metrics=accuracy)
    return learn


@pytest.mark.skipif(True, reason="requires python3.6 or higher")
@mock.patch("jovian.callbacks.fastai.log_hyperparams")
@mock.patch("jovian.callbacks.fastai.log_metrics")
def test_on_train_begin_and_on_epoch_end(mock_log_metrics, mock_log_hyperparams, learn):
    jvn_cb = JovianFastaiCallback(learn, 'res18')
    learn.fit_one_cycle(2, callbacks=jvn_cb)

    mock_log_hyperparams.assert_called_with(
        {'epochs': 2, 'batch_size': 2, 'loss_func': 'CrossEntropyLoss()', 'opt_func': 'torch.optim.adam.Adam',
         'weight_decay': 0.01, 'learning_rate': '0.003', 'arch_name': 'res18'})

    mock_log_metrics.assert_called_with({'epoch': 1, 'train_loss': ANY, 'valid_loss': ANY, 'accuracy': ANY})
