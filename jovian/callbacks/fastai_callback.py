from torch import Tensor
from fastai.basic_train import Learner
from fastai.callback import Callback

from jovian import log_hyperparams, log_metrics
from jovian.utils.logger import log


class FastaiCallback(Callback):
    """FastAI callback to log hyperparameters and metrics during model training.

    Arguments:
        learn (Learner): A learner object with which you're fitting your model

        arch_name (string): A name for the architecture that you're using 
    """

    def __init__(self, learn: Learner, arch_name: str):
        self.learn = learn
        self.arch_name = arch_name
        self.met_names = ['epoch', 'train_loss']
        # existence of validation dataset
        self.valid_set = self.learn.data.valid_dl.items.any()
        if self.valid_set:
            self.met_names.append('valid_loss')

    def on_train_begin(self, n_epochs: int, metrics_names: list, **ka):
        hyp_dict = {
            'arch_name': self.arch_name,
            'epochs': n_epochs,
            'batch_size': self.learn.data.batch_size,
            'loss_func': str(self.learn.loss_func.func),
            'opt_func': str(self.learn.opt_func.func).split("'")[1],
            'weight_decay': self.learn.wd,
            'learning_rate': str(self.learn.opt.lr)
        }
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

    def on_train_end(self, **ka):
        if not self.valid_set:
            log('Metrics apart from train_loss are not calculated in fastai without a validation dataset')
