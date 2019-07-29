from fastai.callback import Callback
from fastai.basic_train import Learner
from jovian import log_hyperparams, log_metrics


class JovianFastaiCallback(Callback):
    """FastAI callback to log hyperparameters and metrics during model training.

    Arguments:
        learn (Learner): A learner object with which you're fitting your model

        arch_name (string): A name for the architecture that you're using 
    """

    def __init__(self, learn: Learner, arch_name):
        self.learn = learn
        self.arch_name = arch_name
        self.hyp_names = ['arch_name', 'epochs', 'batch_size',
                          'loss_func', 'opt_func', 'weight_decay', 'learning_rate']
        self.met_names = ['epoch', 'train_loss']
        # existance of validation dataset
        self.valid_set = self.learn.data.valid_dl.items.any()
        if(self.valid_set):
            self.met_names.append('valid_loss')

    def on_train_begin(self, **ka):

        hyp_values = [self.arch_name,
                      ka['n_epochs'],
                      self.learn.data.batch_size,
                      str(self.learn.loss_func.func),
                      str(self.learn.opt_func.func).split("'")[1],
                      self.learn.wd,
                      str(self.learn.opt.lr)]
        log_hyperparams(dict(zip(self.hyp_names, hyp_values)), verbose=False)

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
            log_metrics({
                'val_loss, metrics': "won't be calculated in fastai without valid dataset"
            })
