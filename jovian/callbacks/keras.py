from keras.backend import get_value
from keras.callbacks import Callback

from jovian import log_hyperparams, log_metrics


class JovianKerasCallback(Callback):
    """Keras Callback to log hyperparameters and metrics during model training.

    Args:
        arch_name (string, optional): A name for the model you’re training.
        every_epoch (bool, optional): Whether to record losses & metrics for every epoch. Defaults to False.

    Example
        .. code-block::

            from jovian.callbacks.keras import JovianKerasCallback

            jvn_cb = JovianKerasCallback(arch_name='resnet18', every)
            model.fit(x_train, y_train, ...., callbacks=[jvn_cb])

    .. admonition:: Tutorial

        Visit `this`_ for a detailed example on using the fastai callback, also visit the *Records* tab
        to see all the logs of that notebook logged by the callback.
    .. _this: https://jvn.io/PrajwalPrashanth/34fd4e72905e460db2d16aafab285537

    """

    def __init__(self, arch_name='', every_epoch=False):
        self.arch_name = arch_name
        self.every_epoch = every_epoch

    def on_train_begin(self, logs=None):
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
