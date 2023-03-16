# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]

with open("exercises\\07_files\\config_sw1.txt") as src ,open("exercises\\07_files\\result.txt", 'w') as dst:
    for line in src:
        words = line.split()
        words_intersect = set(words) & set(ignore) 
        if not line.startswith("!") and not words_intersect:
            dst.write(line)
