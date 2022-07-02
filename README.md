
## Description
The program synchronizes the contents of the destination directory (slave) with the contents of the source directory (master).

Synchronization includes operations:
- deletion
- creation
- modification
- change of file metadata

## Usage

Run synchronization
```bash
$ sudo ./sync.py [--interval INTERVAL] [--log-file LOG_FILE] master slave
```

Stop syncronization
`Ctrl`+`C`


#### Example
```bash
user@ubuntu:~/sync$ sudo ./sync.py -i 1.5 --log-file sync.log /etc/ /tmp/etc-copy/
```
Log file snippet example:
```bash
2022-02-18 02:46:25 : ./sync.py PID 191 : INFO : Start syncronization /etc ----> /tmp/etc-copy
2022-02-18 02:46:25 : ./sync.py PID 191 : INFO : copied: dir /tmp/etc-copy/alternatives
...
2022-02-18 02:46:26 : ./sync.py PID 191 : INFO : copied: dir /tmp/etc-copy/xdg
...
2022-02-18 02:46:26 : ./sync.py PID 191 : INFO : copied: file /tmp/etc-copy/zsh_command_not_found
...
2022-02-18 02:46:28 : ./sync.py PID 191 : INFO : changed GID: /tmp/etc-copy/gshadow-
...
2022-02-18 02:46:28 : ./sync.py PID 191 : INFO : updated: /tmp/etc-copy/mtab
...
2022-02-18 02:46:29 : ./sync.py PID 191 : INFO : changed stat: /tmp/etc-copy/alternatives/write
...
2022-02-18 02:46:44 : ./sync.py PID 191 : INFO : Stop syncronization /etc --X--> /tmp/etc-copy
```
