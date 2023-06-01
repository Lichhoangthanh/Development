from flask import *
from flask_login import *

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You must be logged in to access this page.'
login_manager.login_message_category = 'warning'

class User(UserMixin):
    def __init__(self, user_id, user_login):
        self.id = user_id
        self.login = user_login

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        remember = request.form.get('remember_me') == 'on'
        for user in get_user():
            if user['login'] == login and user['password'] == password:
                login_user(User(user['id'], user['login']), remember = remember)
                flash('You have successfully passed authentication!', 'success')
                param_url = request.args.get('next')
                return redirect(param_url or url_for('index'))
        flash('Wrong username or password entered.', 'danger')
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    for user in get_user():
        if user['id'] == int(user_id):
            return User(user['id'], user['login'])
    return None

def get_user() :
    users = [
        {
        "id": 1,
        "login": "user",
        "password": "qwerty"
        },
        {
        "id": 2,
        "login": "l",
        "password": "l"
        }
    ]
    return users
