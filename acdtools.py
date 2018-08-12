import logging
import os
import shutil
import subprocess
import yaml
from pathlib import Path
from typing import Callable, Dict, Optional, Union

import click

logger = logging.getLogger(__name__)

# TODO make public functions click commands


def _validate_config(
    ctx: click.core.Context,
    param: Union[click.core.Option, click.core.Parameter],
    value: Optional[Union[int, bool, str]],
) -> Dict[str, str]:
    required_keys = set([
        'mount_base',
        'data_dir',
        'encfs_pass',
        'path_on_cloud_drive',
        'days_to_keep_local',
        'encfs6_config',
    ])
    optional_keys = set(['http_proxy', 'https_proxy'])

    allowed_keys = required_keys + optional_keys

    config = yaml.load(value)

    keys = config.keys()

    missing_required_keys = required_keys - config.keys()
    extra_keys = config.keys() - allowed_keys

    if missing_required_keys:
        message = (
            'Using configuration file at "{config_file_path}". '
            'Missing the following configuration keys: {missing_keys}.'
        ).format(
            config_file_path=str(value),
            missing_keys=', '.join(missing_required_keys),
        )
        raise click.BadParameter(message)

    if extra_keys:
        message = (
            'Using configuration file at "{config_file_path}". '
            'The following keys were given but are not valid: {extra_keys}.'
        ).format(
            config_file_path=str(value),
            extra_keys=', '.join(extra_keys),
        )
        raise click.BadParameter(message)

    return config



def config_path_option(command: Callable[..., None]) -> Callable[..., None]:
    """
    """
    # TODO common click option -c, --config-path
    # default to pwd/vars
    # TODO validator validates config


# TODO make this run on the group
def _dependency_check() -> None:
    # TODO binaries from config
    dependencies = (
        rclone_binary,
        plexdrive_binary,
        'unionfs-fuse',
        'encfs',
        'fusermount',
        'screen',
    )
    for dependency in dependencies:
        if shutil.which(dependency) is None:
            message = '"{dependency}" is not available on the PATH.'.format(
                dependency=dependency, )

            click.fail(message=message)


def _unmount(mountpoint: Path) -> None:
    """
    Unmount a mountpoint. Will not unmount if not already mounted.

    This does not work on macOS as ``fusermount`` does not exist.
    """
    is_mountpoint = os.path.ismount(path=str(mountpoint))
    if not is_mountpoint:
        message = 'Cannot unmount "{mountpoint}" - it is not mounted'.format(
            mountpoint=str(mountpoint), )
        logger.warn(message=message)
        return

    message = 'Unmounting "{mountpoint}"'.format(mountpoint=str(mountpoint))
    logger.info(message=message)
    unmount_args = ['fusermount', '-u', str(mountpoint)]
    subprocess.run(args=unmount_args, check=True)


@config_path_option
def unmount_all(config: Dict[str, str]) -> None:
    message = 'Unmounting all ACDTools moundpoints'
    logger.info(message)

    # mountpoints = (
    #     data_dir,
    #     mountbase / 'acd-encrypted',
    #     mountbase / 'acd-decrypted',
    #     mountbase / 'local-encrypted',
    # )
    #
    # for mountpoint in mountpoints:
    #     _unmount(mountpoint)


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
