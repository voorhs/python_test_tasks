# Тестовое задание на ревью кода

## Описание

Сервис запускается внутри докер контейнера, вычитывает числа из файла data.csv (который хранится в архиве data.tgz), суммирует все числа, проверяет, что сумма равна `10`.
 
В общем сервис работает и выполняет свою задачу, но при разработке разработчики допустили много ошибок/недочетов, необходимо их найти, все исправления должны быть с комментариями, которые описываю причину исправления.
 
 
## Запуск сервиса
Требования:
- docker
 
Запус сервиса:
```bash
make test
```
 
## Критерии оценки работы
- оптимизация кода
- код стайл
- читаемость кода
- следования устоявшимся практикам для задач такого рода
- повышение стабильности/безопасности работы кода

    
## Решение

Формат входных данных: датафрейм любого размера с любыми значениями. Извлекаются только числовые значения. Примеры:

```
1,2,3,4

1,2
3,4

1,-
4,5

1,-,2
3,4
```

Для тестирования работы сервиса
- поместить архив `data.tgz` с файлом `data.csv` в текущую рабочую директорию
- запустить `make test`

Как я предлагаю пользователю обращаться к сервису
- запуллить образ
- открыть в терминале папку с архивом `data.tgz`, в котором лежит файл `data.csv`
- запустить в тихом режиме: `docker run --rm -v .:/data code_review`, на выходе будет просто `True` или `False`
- запустить в нетихом режиме: `docker run --rm -e CSV_VERBOSE=1 -v .:/data code_review`, на выходе будет подобное:
```
===== SIGMA BASED CSV CHECKER =====
    Do values sum to 10: True
===================================
```

Сервис сворачивается и выводит сообщения об ошибке при
- отсутствии `data.tgz`
- ошибке чтения `data.csv`
    