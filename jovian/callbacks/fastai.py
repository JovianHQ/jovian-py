from torch import Tensor
from fastai.basic_train import Learner
from fastai.callback import Callback

from jovian.utils.records import log_hyperparams, log_metrics, reset
from jovian.utils.logger import log


class JovianFastaiCallback(Callback):
    """Fastai callback to automatically log hyperparameters and metrics.

    Args:
        learn (Learner): A learner object reference of your current model.

        arch_name (string): A name for the model you're training. 

    Example
        .. code-block::

            from jovian.callbacks.fastai import JovianFastaiCallback

            jvn_cb = JovianFastaiCallback(learn, 'res18')
            learn.fit_one_cycle(5, callbacks = jvn_cb)

    .. admonition:: Tutorial

        Visit `this`_ for a detailed example on using the fastai callback, also visit the *Records* tab
        to see all the logs of that notebook logged by the callback.
    .. _this: https://jovian.ai/PrajwalPrashanth/7f16274fc3224d829941bc2553ef6061?utm_source=docs
    """

    def __init__(self, learn: Learner, arch_name=None, reset_tracking=True):
        self.learn = learn
        self.arch_name = arch_name
        self.met_names = ['epoch', 'train_loss']
        # existence of validation dataset
        self.valid_set = self.learn.data.valid_dl.items.size > 0
        self.reset_tracking = reset_tracking
        if self.valid_set:
            self.met_names.append('valid_loss')

    def on_train_begin(self, n_epochs: int, metrics_names: list, **ka):
        if self.reset_tracking:
            reset('hyperparams', 'metrics')
        hyp_dict = {
            'epochs': n_epochs,
            'batch_size': self.learn.data.batch_size,
            'loss_func': str(self.learn.loss_func.func),
            'opt_func': str(self.learn.opt_func.func).split("'")[1],
            'weight_decay': self.learn.wd,
            'learning_rate': str(self.learn.opt.lr)
        }
        if self.arch_name:
            hyp_dict['arch_name'] = self.arch_name
        log_hyperparams(hyp_dict)

        if self.valid_set:
            self.met_names.extend(metrics_names)

    def on_epoch_end(self, epoch: int, smooth_loss: Tensor, last_metrics: list, **ka):
        met_values = [epoch,
                      smooth_loss.item()]  # smoothened avg. train loss for the epoch

        if self.valid_set:
            # last_metrics is a list with first elem as valid_loss followed by all
            # the metrics of the learner
            met_values.extend([str(last_metrics[0])] + [i.item()
                                                        for i in last_metrics[1:]])
        log_metrics(dict(zip(self.met_names, met_values)))

    def on_train_end(self, **ka):  # no-cover
        if not self.valid_set:
            log('Metrics apart from train_loss are not calculated in fastai without a validation dataset')
