# -*- coding: utf-8 -*-
"""
Задание 4.2

Преобразовать строку в переменной mac из формата XXXX:XXXX:XXXX
в формат XXXX.XXXX.XXXX
Полученную новую строку вывести на стандартный поток вывода (stdout) с помощью print.

Ограничение: Все задания надо выполнять используя только пройденные темы.

Предупреждение: в разделе 4 тесты можно легко "обмануть" сделав нужный вывод,
без получения результатов из исходных данных с помощью Python.
Это не значит, что задание сделано правильно, просто на данном этапе сложно иначе
проверять результат.

Chuyển đổi chuỗi trong biến mac từ định dạng XXXX:XXXX:XXXX
sang định dạng XXXX.XXXX.XXXX
In dòng mới kết quả thành đầu ra tiêu chuẩn (thiết bị xuất chuẩn) bằng cách sử dụng print.

Hạn chế: Tất cả các nhiệm vụ phải được hoàn thành chỉ sử dụng các chủ đề được đề cập.

Cảnh báo: trong Phần 4, các bài kiểm tra có thể dễ dàng bị "gian lận" để tạo ra kết quả mong muốn,
mà không nhận được kết quả từ dữ liệu gốc với Python.
Điều này không có nghĩa là nhiệm vụ được thực hiện chính xác, chỉ ở giai đoạn này thì khó ở giai đoạn khác.
kiểm tra kết quả.
"""

mac = "AAAA:BBBB:CCCC"

mac_new = mac.replace(":",".")

print(mac_new)


