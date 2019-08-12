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

    def __init__(self, learn: Learner, arch_name):
        self.learn = learn
        self.arch_name = arch_name
        self.met_names = ['epoch', 'train_loss']
        # existence of validation dataset
        self.valid_set = self.learn.data.valid_dl.items.any()
        if(self.valid_set):
            self.met_names.append('valid_loss')

    def on_train_begin(self, **ka):

        hyp_dict = {
            'arch_name': self.arch_name,
            'epochs': ka['n_epochs'],
            'batch_size': self.learn.data.batch_size,
            'loss_func': str(self.learn.loss_func.func),
            'opt_func': str(self.learn.opt_func.func).split("'")[1],
            'weight_decay': self.learn.wd,
            'learning_rate': str(self.learn.opt.lr)
        }
        log_hyperparams(hyp_dict, verbose=False)

        if(self.valid_set):
            self.met_names.extend(ka['metrics_names'])

    def on_epoch_end(self, **ka):
        met_values = [ka['epoch'],
                      ka['smooth_loss'].item()]  # smooth_loss is the key for avg. train_loss value(tensor) for the epoch
        if(self.valid_set):
            # last_metrics is a key for a list with first element as val_loss(type float)
            # followed by all the metrics(tensors) calculated
            met_values.extend([str(ka['last_metrics'][0])] + [i.item()
                                                              for i in ka['last_metrics'][1:]])
        log_metrics(dict(zip(self.met_names, met_values)), verbose=False)

    def on_train_end(self, **ka):
        if not(self.valid_set):
            log('Metrics are not calculatd in fastai without a validation dataset')
