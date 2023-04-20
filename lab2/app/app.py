from flask import *


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

@app.route('/form')
def form(): 
    return render_template('form.html')