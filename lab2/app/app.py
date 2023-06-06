from flask import *
import re


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/headers')
def headers(): 
    return render_template('headers.html')

@app.route('/args')
def args(): 
    return render_template('args.html')

@app.route('/cookies')
def cookies(): 
    resp = make_response(render_template('cookies.html'))
    if "name" in request.cookies :
        resp.delete_cookie("name")
    else :
        resp.set_cookie("name","value")
    return resp

@app.route('/form', methods=['GET', 'POST'])
def form(): 
    return render_template('form.html')

def transformation_text(kind, nums_phone_number):
    result = ''
    if kind == '+7':
        result = f'8-{nums_phone_number[1:4]}-{nums_phone_number[4:7]}-{nums_phone_number[7:9]}-{nums_phone_number[9:]}'
    elif kind == '8':
        result = f'8-{nums_phone_number[1:4]}-{nums_phone_number[4:7]}-{nums_phone_number[7:9]}-{nums_phone_number[9:]}'
    elif kind == '10':
        result = f'8-{nums_phone_number[0:3]}-{nums_phone_number[3:6]}-{nums_phone_number[6:8]}-{nums_phone_number[8:]}'
    return result

@app.route('/phone_checker', methods = ['GET', 'POST'])
def phone_checker():
    types_of_error = [
        'Недопустимый ввод. Неверное количество цифр.', 
        'Недопустимый ввод. В номере телефона встречаются недопустимые символы.',
    ]
    allows_chars = [' ', '(', ')', '-', '.', '+', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    phone_number = None
    error_msg = None
    isnt_valid = False
    
    if request.method == 'POST':
        length_of_nums_in_phone = 0
        nums_phone_number = ''
        phone_number = request.form.get('phone_number')
        for num in phone_number:
            if num not in allows_chars:
                error_msg = types_of_error[1]
                isnt_valid = True
                break
            if num.isdigit():
                length_of_nums_in_phone += 1
                nums_phone_number += str(num)
        if len(nums_phone_number) < 10:
            return render_template('phone_checker.html', phone_number=phone_number, isnt_valid=True, error_msg=types_of_error[0])
        if isnt_valid == False and phone_number[0] == '+' and phone_number[1] == '7' and len(nums_phone_number) == 11:
            phone_number = transformation_text('+7', nums_phone_number)
        elif isnt_valid == False and phone_number[0] == '8' and len(nums_phone_number) == 11:
            phone_number = transformation_text('8', nums_phone_number)
        elif isnt_valid == False and len(nums_phone_number) == 10:
            phone_number = transformation_text('10', nums_phone_number)
        elif isnt_valid == False and len(nums_phone_number) > 10:
            error_msg = types_of_error[0]
            isnt_valid = True

    return render_template('phone_checker.html', phone_number=phone_number, isnt_valid=isnt_valid, error_msg=error_msg)


@app.route('/calc', methods=['GET', 'POST'])
def calc():
    answer=''
    error_text=''
    if request.method=='POST':
        try:
            first_num = int(request.form['first_num'])
            second_num = int(request.form['second_num'])
        except ValueError:
            error_text='The text has been sent. Please enter a number.'
            return render_template('calc.html', answer=answer, error_text=error_text)
        operation = request.form['operation']
        if operation == '+':
            answer = first_num + second_num
        elif operation == '-':
            answer = first_num - second_num
        elif operation == '*':
            answer = first_num * second_num
        elif operation == '/':
            try:
                answer = first_num / second_num
            except ZeroDivisionError:
                error_text = "Can't divide by zero"
    return render_template('calc.html', answer=answer, error_text=error_text)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404