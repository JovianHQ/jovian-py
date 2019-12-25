from jovian.utils import api
from jovian.utils.logger import log

_data_blocks = []


def get_record_slugs(with_type=False):
    """Get the list of slugs recorded so far"""
    global _data_blocks
    if with_type:
        return _data_blocks
    else:
        return [slug for slug, _ in _data_blocks]


def reset_records(*args):
    """Reset the tracked hyperparameters, metrics or dataset (for a fresh experiment)

    Args:
        *args(strings, optional): By default resets all type of records. For specific filter
                            add keywords `metrics`, `hyperparams`, `dataset` individually
                            or in combinations to reset those type of records.  
    Example
        .. code-block::

            import jovian

            jovian.reset_records('hyperparams', 'metrics')
    """
    global _data_blocks

    if len(args) == 0:
        _data_blocks = []
    else:
        _data_blocks = [(slug, rec_type) for (slug, rec_type) in _data_blocks if rec_type not in args]


def log_hyperparams(data, verbose=True):
    """Record hyperparameters for the current experiment

    Args:
        data(dict): A python dict or a array of dicts to be recorded as hyperparmeters.

        verbose(bool, optional): By default it prints the acknowledgement, you can remove 
            this by setting the argument to False.

    Example
        .. code-block::

            import jovian

            hyperparams = {
                'arch_name': 'cnn_1',
                'lr': .001
            }
            jovian.log_hyperparams(hyperparams)
    """
    global _data_blocks
    record_type = 'hyperparams'

    res = api.post_block(data, record_type)
    _data_blocks.append((res['tracking']['trackingSlug'], record_type))

    if verbose:
        log('Hyperparameters logged.')


def log_metrics(data, verbose=True):
    """Record metrics for the current experiment

    Args:
        data(dict): A python dict or a array of dicts to be recorded as metrics.

        verbose(bool, optional): By default it prints the acknowledgement, you can remove 
            this by setting the argument to False.

    Example
        .. code-block::

            import jovian

            metrics = {
                'epoch': 1,
                'train_loss': .5,
                'val_loss': .3,
                'acc': .94
            }
            jovian.log_metrics(metrics)
    """
    global _data_blocks
    record_type = 'metrics'

    res = api.post_block(data, record_type)
    _data_blocks.append((res['tracking']['trackingSlug'], record_type))

    if verbose:
        log('Metrics logged.')


def log_dataset(data, verbose=True):
    """Record dataset details for the current experiment

    Args:
        data(dict): A python dict or a array of dicts to be recorded as Dataset.

        verbose(bool, optional): By default it prints the acknowledgement, you can 
            remove this by setting the argument to False.

    Example
        .. code-block::

            import jovian

            data = {
                'path': '/datasets/mnist',
                'description': '28x28 images of handwritten digits (in grayscale)'
            }
            jovian.log_dataset(data)
    """
    global _data_blocks
    record_type = 'dataset'

    res = api.post_block(data, record_type)
    _data_blocks.append((res['tracking']['trackingSlug'], record_type))

    if verbose:
        log('Dataset logged.')


def log_git(data, verbose=True):
    """Record the git-related information.

    Args:
        data(dict): A python dict or a array of dicts to be recorded as a git related block.

        verbose(bool, optional): By default it prints the acknowledgement, you can 
            remove this by setting the argument to False.
    """
    global _data_blocks
    record_type = 'git'

    res = api.post_block(data, record_type)
    _data_blocks.append((res['tracking']['trackingSlug'], record_type))

    if verbose:
        log('Git information logged.')
