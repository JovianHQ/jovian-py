from keras.backend import get_value
from keras.callbacks import Callback
import json
import numpy

from jovian.utils.records import log_metrics, log_hyperparams, reset
from jovian.utils.slack import notify


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:  # no-cover
            return super(Encoder, self).default(obj)


class JovianKerasCallback(Callback):
    """Keras Callback to log hyperparameters and metrics during model training.

    Args:
        reset_tracking (string, optional): Will clear previously tracked hyperparameters & metrics, and start a fresh recording. Defaults to True.
        arch_name (string, optional): A name for the model you’re training.
        every_epoch (bool, optional): Whether to record losses & metrics for every epoch or just the final loss & metric. Defaults to False.
        notify (bool, optional): Whether to send notification on slack when the training ends. Defaults to False.

    Example
        .. code-block::

            from jovian.callbacks.keras import JovianKerasCallback

            # To record logs of every epoch and to notify on slack
            jvn_cb = JovianKerasCallback(arch_name='resnet18', every_epoch=True, notify=True)
            model.fit(x_train, y_train, ...., callbacks=[jvn_cb])

    .. admonition:: Tutorial

        Visit `this`_ for a detailed example on using the fastai callback, also visit the *Records* tab
        to see all the logs of that notebook logged by the callback.
    .. _this: https://jovian.ai/PrajwalPrashanth/34fd4e72905e460db2d16aafab285537?utm_source=docs

    """

    def __init__(self, reset_tracking=True, arch_name='', every_epoch=False, notify=False):
        self.arch_name = arch_name
        self.every_epoch = every_epoch
        self.reset_tracking = reset_tracking
        self.notify_slack = notify

    def on_train_begin(self, logs=None):
        # Reset state if required
        if self.reset_tracking:
            reset('hyperparams', 'metrics')

        hyp_dict = {
            'epochs': self.params['epochs'],
            'batch_size': self.params['batch_size'],
            'loss_func': self.model.loss,
            'opt': str(self.model.optimizer.__class__).split("'")[1].split('.')[-1],
            'wt_decay': self.model.optimizer.initial_decay,
            'lr': str(get_value(self.model.optimizer.lr))
        }
        if self.arch_name:
            hyp_dict['arch'] = self.arch_name
        log_hyperparams(hyp_dict, verbose=False)
        self.hyperparams = hyp_dict

    def on_epoch_end(self, epoch, logs):
        if self.every_epoch:
            met_dict = {'epoch': epoch}
            for key, value in logs.items():
                logs[key] = round(value, 4)
            met_dict.update(logs)
            log_metrics(met_dict, verbose=False)

        elif epoch == self.params['epochs'] - 1:
            met_dict = {}
            for key, value in logs.items():
                logs[key] = round(value, 4)
            met_dict.update(logs)
            log_metrics(met_dict, verbose=False)

            if self.notify_slack:
                result = {
                    'message': 'Training complete after ' + str(self.params['epochs']) + ' epochs.',
                    'metrics': met_dict
                }
                if self.hyperparams:
                    result['hyperparams'] = self.hyperparams
                notify(json.dumps(result, indent=2, cls=Encoder), verbose=False, safe=True)
