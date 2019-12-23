
from jovian._version import __version__
from jovian.utils.jupyter import set_notebook_name
from jovian.utils.latest import check_update
from jovian.utils.commit import commit
from jovian.utils.records import log_hyperparams, log_metrics, log_dataset, log_git, reset_records
from jovian.utils.slack import notify


set_notebook_name()
check_update()
