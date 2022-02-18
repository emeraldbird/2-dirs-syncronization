# Задача 2 (Linux version)
Junior Developer in QA test task №2

## Задание
Написать программу, которая будет синхронизировать два каталога: каталог-источник и каталог-реплику.
Задача программы – приводить содержимое каталога-реплики в соответствие содержимому каталога-источника.
Требования:
- Сихронизация должна быть односторонней: после завершения процесса синхронизации содержимое каталога-реплики должно в точности соответствовать содержимому каталогу-источника;
- Синхронизация должна производиться периодически;
- Операции создания/копирования/удаления объектов должны логироваться в файле и выводиться в консоль;
- Пути к каталогам, интервал синхронизации и путь к файлу логирования должны задаваться параметрами командной строки при запуске программы.

## Описание программы
Программа реагирует на:
- удаление
- создание
- модификацию содержимого
- изменение мета-данных

## Использование

Запуск синхронизации
```bash
$ sudo ./task2.py [--interval INTERVAL] [--log-file LOG_FILE] master slave
```

Остановка синхронизации
`Ctrl`+`C`


#### Пример
```bash
sm1rn0vn@ubuntu:~/task_2$ sudo ./task2.py -i 1.5 --log-file sync.log /etc/ /tmp/etc-copy/
```
Фрагменты лога:
```bash
2022-02-18 02:46:25 : ./task2.py PID 191 : INFO : Start syncronization /etc ----> /tmp/etc-copy
2022-02-18 02:46:25 : ./task2.py PID 191 : INFO : copied: dir /tmp/etc-copy/alternatives
...
2022-02-18 02:46:26 : ./task2.py PID 191 : INFO : copied: dir /tmp/etc-copy/xdg
...
2022-02-18 02:46:26 : ./task2.py PID 191 : INFO : copied: file /tmp/etc-copy/zsh_command_not_found
...
2022-02-18 02:46:28 : ./task2.py PID 191 : INFO : changed GID: /tmp/etc-copy/gshadow-
...
2022-02-18 02:46:28 : ./task2.py PID 191 : INFO : updated: /tmp/etc-copy/mtab
...
2022-02-18 02:46:29 : ./task2.py PID 191 : INFO : changed stat: /tmp/etc-copy/alternatives/write
...
2022-02-18 02:46:44 : ./task2.py PID 191 : INFO : Stop syncronization /etc --X--> /tmp/etc-copy
```
