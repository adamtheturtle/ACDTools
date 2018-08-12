import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def acdtools_unmount(mountpoint: Path):
    pass

def acdtools_unmount():
    message = 'Unmounting all ACDTools moundpoints'
    logger.info(message)

    mountpoints = (
        data_dir,
        mountbase / 'acd-encrypted',
        mountbase / 'acd-decrypted',
        mountbase / 'local-encrypted',
    )

    for mountpoint in mountpoints:
    pass
