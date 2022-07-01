
## Описание программы
Программа реагирует на:
- удаление
- создание
- модификацию содержимого
- изменение мета-данных

## Использование

Запуск синхронизации
```bash
$ sudo ./sync.py [--interval INTERVAL] [--log-file LOG_FILE] master slave
```

Остановка синхронизации
`Ctrl`+`C`


#### Пример
```bash
user@ubuntu:~/sync$ sudo ./sync.py -i 1.5 --log-file sync.log /etc/ /tmp/etc-copy/
```
Фрагменты лога:
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
