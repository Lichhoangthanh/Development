# -*- coding: utf-8 -*-
"""
Задание 4.1

Используя подготовленную строку nat, получить новую строку, в которой в имени
интерфейса вместо FastEthernet написано GigabitEthernet.
Полученную новую строку вывести на стандартный поток вывода (stdout) с помощью print.

Ограничение: Все задания надо выполнять используя только пройденные темы.

Предупреждение: в разделе 4 тесты можно легко "обмануть" сделав нужный вывод,
без получения результатов из исходных данных с помощью Python.
Это не значит, что задание сделано правильно, просто на данном этапе сложно иначе
проверять результат.

Sử dụng chuỗi nat đã chuẩn bị, lấy một chuỗi mới có tên
giao diện thay vì FastEthernet được viết GigabitEthernet.
In dòng mới kết quả thành đầu ra tiêu chuẩn (thiết bị xuất chuẩn) bằng cách sử dụng print.

Hạn chế: Tất cả các nhiệm vụ phải được hoàn thành chỉ sử dụng các chủ đề được đề cập.

Cảnh báo: trong Phần 4, các bài kiểm tra có thể dễ dàng bị "gian lận" để tạo ra kết quả mong muốn,
mà không nhận được kết quả từ dữ liệu gốc với Python.
Điều này không có nghĩa là nhiệm vụ được thực hiện chính xác, chỉ ở giai đoạn này thì khó ở giai đoạn khác.
kiểm tra kết quả.

"""

nat = "ip nat inside source list ACL interface FastEthernet0/1 overload"

nat_gig = nat.replace("Fast","Gigabite")

print(nat_gig)
