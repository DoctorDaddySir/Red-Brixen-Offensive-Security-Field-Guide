# Portable Python SFTP Server

A lightweight, field-friendly SFTP server built with Python and Paramiko.

This tool is designed for **quick file transfers in the field**:

* serves the **current working directory**
* uses **username/password** authentication
* defaults to **port 22**
* allows an optional custom port via CLI
* restricts access to the directory where it was launched
* supports basic SFTP browsing, upload, and download

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the server from the directory you want to share.

Example using the default SFTP port:

```bash
sudo python sftp_server.py --username operator --password secret
```

Example using a custom port:

```bash
python sftp_server.py --username operator --password secret --port 2222
```

## Notes on Port 22

Port `22` usually requires elevated privileges on Linux. If you do not want to run with `sudo`, use a higher port such as `2222`.

## What It Serves

The server always serves the **current working directory**.

Example:

```bash
cd /tmp/drop
python sftp_server.py --username operator --password secret --port 2222
```

In this case, remote clients will only be able to access files under:

```text
/tmp/drop
```

## Security Model

This is a **simple field-transfer tool**, not a hardened enterprise file server.

Current design choices:

* plaintext password provided at runtime
* local SSH host key stored as `host_key.pem`
* path traversal blocked so clients cannot escape the served directory
* intended for short-term, operator-controlled use

## Current Feature Set

Implemented:

* username/password authentication
* host key creation and reuse
* privileged-port check for ports below `1024`
* SFTP subsystem support
* directory listing
* file metadata lookups
* file upload and download
* path restriction to the launch directory

Not included by design:

* delete
* rename
* mkdir
* rmdir
* multi-user support
* key-based authentication
* daemon/service packaging

## Files

Typical project layout:

```text
portable-sftp-server/
├── sftp_server.py
├── requirements.txt
├── README.md
└── host_key.pem
```

`host_key.pem` will be created automatically on first run.

## Quick Test Plan

### 1. Start the server

From the folder you want to share:

```bash
python sftp_server.py --username operator --password secret --port 2222
```

### 2. Connect from a client

From another machine or terminal:

```bash
sftp -P 2222 operator@127.0.0.1
```

Enter the password when prompted.

### 3. Verify basic operations

Inside the SFTP client:

```text
ls
pwd
get somefile.txt
put test_upload.txt
```

### 4. Verify auth failure

Try the wrong password and confirm login fails.

### 5. Verify privileged-port behavior

Try running on port `22` without `sudo` and confirm the script exits with a clear error.

### 6. Verify path restriction

Confirm clients cannot access files outside the served directory.

## Operational Notes

* The script currently handles a **single connection** and then exits.
* That behavior is acceptable for quick, controlled field transfers.
* If you need repeated use, just relaunch it.

## Recommended Next Step

Run the script locally first and test it with:

```bash
sftp -P 2222 operator@127.0.0.1
```

Then validate:

* listing files
* downloading files
* uploading files
* overwriting an existing file

## Disclaimer

This tool is meant for controlled, temporary use by an operator who understands the tradeoffs. It is intentionally minimal.
