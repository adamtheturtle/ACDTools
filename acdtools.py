import logging
import os
import shutil
import subprocess
import time
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
        'data_dir',
        'days_to_keep_local',
        'encfs6_config',
        'encfs_pass',
        'mount_base',
        'path_on_cloud_drive',
        'plexdrive',
        'rclone',
        'rclone_remote',
    ])
    optional_keys = set(['http_proxy', 'https_proxy'])

    allowed_keys = required_keys + optional_keys

    config = yaml.load(value)

    missing_required_keys = required_keys - config.keys()
    extra_keys = config.keys() - allowed_keys

    if missing_required_keys:
        message = ('Using configuration file at "{config_file_path}". '
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


def config_option(command: Callable[..., None]) -> Callable[..., None]:
    """
    """
    default_config_path = Path(__file__) / 'vars'

    function = click.option(
        '--config',
        '-c',
        type=click.Path(exists=True),
        callback=_validate_config,
        default=default_config_path,
        help='The path to a file including configuration YAML.',
    )(command)  # type: Callable[..., None]
    return function


def _local_cleanup() -> None:
    """
    Delete local data older than "days_to_keep_local" from the configuration
    file.
    """
    days_to_keep_local = float(config['days_to_keep_local'])
    mount_base = Path(config['mount_base'])
    local_decrypted = mount_base / 'local-decrypted'

    message = (
        'Deleting local files older than "{days_to_keep_local}" days old'
    ).format(
        days_to_keep_local=days_to_keep_local,
    )

    logger.info(message)

    seconds_to_keep_local = days_to_keep_local * 24 * 60 * 60

    file_paths = local_decrypted.rglob('*')

    now_timestamp = datetime.datetime.now().timestamp()
    oldest_acceptable_time = now_timestamp - seconds_to_keep_local

    for path in file_paths:
        ctime = path.stat().st_ctime
        if path.is_file() and ctime < oldest_acceptable_time:
            path.unlink()


# TODO make this run on the group
def _dependency_check(rclone_binary: Path, plexdrive_binary: Path) -> None:
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
                dependency=dependency,
            )

            click.fail(message=message)


def _unmount(mountpoint: Path) -> None:
    """
    Unmount a mountpoint. Will not unmount if not already mounted.

    This does not work on macOS as ``fusermount`` does not exist.
    """
    is_mountpoint = os.path.ismount(path=str(mountpoint))
    if not is_mountpoint:
        message = 'Cannot unmount "{mountpoint}" - it is not mounted'.format(
            mountpoint=str(mountpoint),
        )
        logger.warn(message=message)
        return

    message = 'Unmounting "{mountpoint}"'.format(mountpoint=str(mountpoint))
    logger.info(message=message)
    unmount_args = ['fusermount', '-u', str(mountpoint)]
    subprocess.run(args=unmount_args, check=True)


@config_option
def unmount_all(config: Dict[str, str]) -> None:
    """
    Unmount all mountpoints associated with ACDTools.
    """
    message = 'Unmounting all ACDTools mountpoints'
    logger.info(message)

    data_dir = Path(config['data_dir'])
    mount_base = Path(config['mount_base'])
    remote_encrypted = mount_base / 'acd-encrypted'
    remote_decrypted = mount_base / 'acd-decrypted'
    local_encrypted = mount_base / 'local-encrypted'
    unmount_lock_file = Path(__file__) / 'unmount.acd'

    _unmount(mountpoint=data_dir)
    unmount_lock_file.touch()
    _unmount(mountpoint=remote_encrypted)
    time.sleep(6)
    unmount_lock_file.unlink()
    _unmount(mountpoint=remote_decrypted)
    _unmount(mountpoint=local_encrypted)


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


def acd_cli_mount(config: Dict[str, str]) -> None:
    """
    Foreground mount which will keep remounting until unmount file exists.
    """
    unmount_lock_file = Path(__file__) / 'unmount.acd'
    mount_base = Path(config['mount_base'])
    remote_encrypted = mount_base / 'acd-encrypted'
    chunks_dir = mount_base / 'chunks'
    chunks_dir.mkdir(exist_ok=True)

    while not unmount_lock_file.exists():
        message = 'Running cloud storage mount in the foreground'
        logger.info(message)
        _unmount(mountpoint=remote_encrypted)
        # TODO these args, and run these
        plexdrive_args = [
            plexdrive_binary,
            '-o',
            'allow-other,read_only',
            '-v',
            '2',
            '-t',
            str(chunks_dir),
            '--clear-chunk-max-size=32G',
            str(remote_encrypted),
        ]

        subprocess.run(args=plexdrive_args, check=True)

        message = (
            'Cloud storage mount exited - checking if to remount in a couple '
            'of seconds'
        )
        logger.info(message)
        time.sleep(2)

    message = 'The acdcli mount exited cleanly'
    unmount_lock_file.unlink()
