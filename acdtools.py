import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# TODO make public functions click commands

# TODO common click option -c, --config-path


# TODO make this run on the group
def _dependency_check():
    # TODO fill in
    pass

def _unmount(mountpoint: Path):
    """
    Unmount a mountpoint. Will not unmount if not already mounted.
    """
    # TODO: fusermount does not exist on OS X, make compatible.
    # TODO fill in
    pass

def unmount_all():
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


def sync_nodes():
    # TODO fill in
    pass

def sync_deletes():
    # TODO fill in
    pass

def mount():
    unmount_all()
    sync_nodes()
    # TODO the actual mount

def acd_cli_mount():
    # TODO fill in
    pass
