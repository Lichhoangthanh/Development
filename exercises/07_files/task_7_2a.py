# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]



with open("exercises\\07_files\\config_sw1.txt", "r") as f:
    for line in f:
        words = line.split()
        words_intersect = set(words) & set(ignore) # so sánh từng dòng với từ bị cấm
        # print(words_intersect)   nếu có chữ cái bị trùng words_intersect trả về true
        if not line.startswith("!") and not words_intersect:
            print(line.rstrip())
