import logging
import shutil
from pathlib import Path
from typing import Callable

import click

logger = logging.getLogger(__name__)

# TODO make public functions click commands


def config_path_option(command: Callable[..., None]) -> Callable[..., None]:
    """
    """
    # TODO common click option -c, --config-path
    # default to pwd/vars


# TODO make this run on the group
def _dependency_check() -> None:
    # TODO binary from ACDCLI binary config
    dependencies = (
        acd_cli_binary,
        'unionfs-fuse',
        'encfs',
        'screen',
    )
    for dependency in dependencies:
        if shutil.which(dependency) is None:
            message = '"{dependency}" is not available on the PATH.'.format(
                dependency=dependency,
            )

            click.fail(message=message)


def _unmount(mountpoint: Path) -> None:
    """
    Unmount a mountpoint. Will not unmount if not already mounted.
    """
    # TODO: fusermount does not exist on OS X, make compatible.
    # TODO fill in
    pass


def unmount_all() -> None:
    message = 'Unmounting all ACDTools moundpoints'
    logger.info(message)

    mountpoints = (
        data_dir,
        mountbase / 'acd-encrypted',
        mountbase / 'acd-decrypted',
        mountbase / 'local-encrypted',
    )

    for mountpoint in mountpoints:
        _unmount(mountpoint)


def upload() -> None:
    # TODO fill in
    pass


def sync_nodes() -> None:
    """
    Sync node cache.
    """
    # TODO fill in
    pass


def sync_deletes() -> None:
    # TODO fill in
    pass

def _mount() -> None:
    # TODO fill in
    pass


def mount() -> None:
    unmount_all()
    sync_nodes()
    _mount()


def acd_cli_mount() -> None:
    # TODO fill in
    pass
