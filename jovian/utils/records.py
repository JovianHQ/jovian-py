from jovian.utils import api
from jovian.utils.logger import log

_data_blocks = []


def get_records(slug_only=False):
    """Get the list of slugs recorded so far"""
    global _data_blocks
    if slug_only:
        return [slug for slug, _, _ in _data_blocks]
    else:
        return _data_blocks


def reset(*record_types):
    """Reset the tracked hyperparameters, metrics or dataset (for a fresh experiment)

    Args:
        *record_types(strings, optional): By default, resets all type of records. 
            To reset specific type of records, pass arguments `metrics`, 
            `hyperparams`, `dataset`
    Example
        .. code-block::

            import jovian
            jovian.reset('hyperparams', 'metrics')
    """
    global _data_blocks

    if len(record_types) == 0:
        _data_blocks = []
    else:
        _data_blocks = [(slug, rec_type, data) for (slug, rec_type, data) in _data_blocks
                        if rec_type not in record_types]


def _parse_data(data, data_args):
    """Parse different types of arguments"""
    data = data or {}
    if isinstance(data, dict):
        for k in data_args:
            data[k] = data_args[k]
    elif isinstance(data, list) and len(data_args.keys()) > 0:
        data.append(data_args)
    return data if len(data) > 0 else None


def log_record(record_type, data=None, verbose=True, **data_args):
    """Create records with the given data & type"""
    global _data_blocks
    # Create the combined data dictionary
    data = _parse_data(data, data_args)
    if data is None and verbose:
        log('Nothing to record. Skipping..', error=True)
        return
    # Send to API endpoint
    res = api.post_block(data, record_type)
    tracking_slug = res['tracking']['trackingSlug']
    # Save to data block
    _data_blocks.append((tracking_slug, record_type, data))
    if verbose:
        log(record_type.capitalize() + ' logged.')


def log_hyperparams(data_dict=None, verbose=True, **data_args):
    """Record hyperparameters for the current experiment

    Args:
        data_dict(dict, optional): A python dict to be recorded as hyperparmeters.

        verbose(bool, optional): By default it prints the acknowledgement, you can remove 
            this by setting the argument to False.

        **data_args(optional): Instead of passing a dictionary, you can also pass each 
            individual key-value pair as a argument (see example below)

    Example
        .. code-block::

            import jovian
            jovian.log_hyperparams(arch='cnn', lr=0.001)
            # or
            jovian.log_hyperparams({ 'arch': 'cnn', 'lr': 0.001 })
    """
    log_record('hyperparams', data_dict, verbose, **data_args)


def log_metrics(data_dict=None, verbose=True, **data_args):
    """Record metrics for the current experiment

    Args:
        data_dict(dict, optional): A python dict to be recorded as metrics.

        verbose(bool, optional): By default it prints the acknowledgement, you can remove 
            this by setting the argument to False.

        **data_args(any, optional): Instead of passing a dictionary, you can also pass each 
            individual key-value pair as a argument (see example below)

    Example
        .. code-block::

            import jovian
            jovian.log_metrics(epochs=1, train_loss=0.5, 
                               val_loss=0.3, val_accuracy=0.9)
            # or
            jovian.log_metrics({ 'epochs': 1, 'train_loss': 0.5 })
    """
    log_record('metrics', data_dict, verbose, **data_args)


def log_dataset(data_dict=None, verbose=True, **data_args):
    """Record dataset details for the current experiment

    Args:
        data_dict(dict, optional): A python dict to be recorded as dataset.

        verbose(bool, optional): By default it prints the acknowledgement, you can remove 
            this by setting the argument to False.

        **data_args(optional): Instead of passing a dictionary, you can also pass each 
            individual key-value pair as a argument (see example below)

    Example
        .. code-block::

            import jovian

            path = 'data/mnist'
            description = '28x28 images of handwritten digits (in grayscale)'

            jovian.log_dataset(path=path, description=description)
            # or 
            jovian.log_dataset({ 'path': path, 'description': description })
    """
    log_record('dataset', data_dict, verbose, **data_args)


def log_git(data_dict=None, verbose=True, **data_args):
    """Record the git-related information.

    Args:
        data(dict): A python dict or a array of dicts to be recorded as a git related block.

        verbose(bool, optional): By default it prints the acknowledgement, you can 
            remove this by setting the argument to False.
    """
    log_record('git', data_dict, verbose, **data_args)
