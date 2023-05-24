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

@app.route('/Telephone', methods=['GET',"POST"])
def tel():
    msg = ''
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        digits = [char for char in phone_number if char.isdigit()]
        if digits[0]  != '8' and phone_number[0] != '+' and phone_number[1] != '7':
            msg += 'Invalid input. Invalid number of digits. Your phone number need to start with 8 or +7 '
            return render_template('tel.html', phone_number=phone_number, msg = msg)
        elif   len(digits) != 11:
            msg += 'Invalid input. Invalid number, you need to enter 11 numbers.'
            return render_template('tel.html', phone_number=phone_number, msg = msg)
        elif not all(char.isdigit() or char in [' ','+', '(', ')', '-', '.'] for char in phone_number):
            msg += 'Invalid input. There are invalid characters in the phone number.'
            return render_template('tel.html', phone_number=phone_number, msg = msg)
        else:
            formatted_number = '8-'
            for i in range(1, len(digits)):
                if i in [4,7,9]:
                    formatted_number += '-' + ''.join(digits[i])
                else:
                    formatted_number += ''.join(digits[i])
            msg = 'Accepted! Phone number entered: '
            return render_template('tel.html', msg = msg, num = formatted_number)
    else:
        return render_template('tel.html')

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