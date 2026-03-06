# Unquoted Service Path

## Detection

wmic service get name,displayname,pathname,startmode

Look for paths like:

C:\Program Files\Service Folder\service.exe

without quotes.

## Exploitation

Place malicious executable earlier:

C:\Program.exe

Restart service.
