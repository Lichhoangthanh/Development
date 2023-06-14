SECRET_KEY = 'cd99f6eb39b78d27742089f72bb2102587c30f7c22c4c97850ded91dda7e58cd'

MYSQL_USER = 'std_2082_lab4'
MYSQL_PASSWORD = '12345678'
MYSQL_HOST = 'std-mysql.ist.mospolytech.ru'
MYSQL_DATABASE = 'std_2082_lab4'

TYPES_ERRORS = {
        "empty_login": "Логин не должен быть пустым",
        "empty_passwd": "Пароль не должен быть пустым",
        "empty_last_name": "Фамилия не должна быть пустой",
        "empty_first_name": "Имя не должно быть пустым",
        "login_incorrect_size": "Логин должен быть не меньше 5 символов",
        "login_incorrect_chars": "Логин должен состоять только из латинских букв и цифр",
        "password_small_length": "Пароль должен быть не меньше 8 символов",
        "password_big_length": "Пароль должен быть не более 128 символов",
        "password_has_spaces": "Пароль не должен содержать пробелов",
        "password_incorrect_chars": '''Пароль должен состоять из латинских или кириллических букв, содержать только арабские цифры и допустимые символы: ~!?@#$%^&*_-+()[]{}></\|"'.,:;''',
        "password_hasnt_big_alpha": "Пароль должен содержать как минимум одну заглавную букву",
        "password_hasnt_small_alpha": "Пароль должен содержать как минимум одну строчную букву",
        "password_hasnt_digit": "Пароль должен содержать как минимум одну цифру",
        "incorrect_password": "Неверный пароль",
        "incorrect_checked_password": "Пароль должен быть таким же"
    }