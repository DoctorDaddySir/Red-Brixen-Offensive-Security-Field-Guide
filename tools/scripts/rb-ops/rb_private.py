"""POSIX owner-only storage shared by every RB-OPS database opener."""
import os
from pathlib import Path
import sqlite3
import stat


def safe_parent(path):
    path = Path(path).absolute()
    # The final SQLite open uses a pathname, so protect every rename authority,
    # not only .redbrixen. /tmp is safe only through its sticky owner protection.
    trusted_owners = {os.getuid(), 0, Path('/').stat().st_uid}
    child = None
    for parent in (path, *path.parents):
        if parent.is_symlink():
            raise ValueError('Storage paths must not contain symbolic links.')
        info = parent.stat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid not in trusted_owners:
            raise ValueError('Storage ancestors must be directories owned by you or the system.')
        if parent == path and info.st_uid != os.getuid():
            raise ValueError('Storage parent must be owned by you.')
        if info.st_mode & 0o022:
            sticky_protects_child = (child is not None and info.st_mode & stat.S_ISVTX
                                    and child.stat().st_uid == os.getuid())
            if not sticky_protects_child:
                raise ValueError('Storage ancestors must not allow replacement by other users.')
        child = parent
    return path


def private_file(path, *, create=False, strict=False):
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    if create:
        flags = os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK
    fd = os.open(path, flags, 0o600)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_nlink != 1:
            raise ValueError('Storage must be a singly linked regular file owned by you.')
        if strict and stat.S_IMODE(info.st_mode) != 0o600:
            raise ValueError('Key and backup files must have mode 0600.')
        os.fchmod(fd, 0o600)
        return fd
    except BaseException:
        os.close(fd)
        raise


def prepare_database(path):
    path = Path(path)
    safe_parent(path.parent.parent)
    path.parent.mkdir(mode=0o700, exist_ok=True)
    safe_parent(path.parent)
    path.parent.chmod(0o700)
    # Also tighten any existing SQLite state before SQLite reads it.
    for suffix in ('', '-wal', '-shm', '-journal'):
        candidate = Path(str(path) + suffix)
        if candidate.exists() or candidate.is_symlink():
            os.close(private_file(candidate))
    return path


def connect_private(path):
    # These are command-line processes: subsequent SQLite/temp files stay private.
    os.umask(0o077)
    path = prepare_database(path)
    os.close(private_file(path, create=True))
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA secure_delete=ON')
    conn.execute('PRAGMA temp_store=MEMORY')
    return conn


def read_private(path):
    path = Path(path)
    safe_parent(path.parent)
    with os.fdopen(private_file(path, strict=True), 'rb') as stream:
        return stream.read()


def write_new_private(path, data):
    """Never replace an existing key, backup or restore destination."""
    path = Path(path)
    safe_parent(path.parent)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        with os.fdopen(fd, 'wb') as stream:
            os.fchmod(stream.fileno(), 0o600)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        path.unlink(missing_ok=True)
        raise
