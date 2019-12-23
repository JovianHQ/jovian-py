
from jovian._version import __version__

from jovian.utils.initialize import _initialize_jovian
from jovian.utils.commit import commit
from jovian.utils.records import log_hyperparams, log_metrics, log_dataset, log_git, reset_records
from jovian.utils.slack import notify


_initialize_jovian()
