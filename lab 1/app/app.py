from flask import Flask, render_template
from faker import Faker

app = Flask(__name__)
application = app 

fake = Faker()

images_id = [
    '2d2ab7df-cdbc-48a8-a936-35bba702def5',
    '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
    '7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
    'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
    'cab5b7f2-774e-4884-a200-0c0180fa777f'
]

def generate_post(index):
    return { 
            'title': 'post title',
            'img_id' : images_id[index],
            'text' : fake.paragraph(nb_sentences = 100),
            'author': fake.name(),
            'date': fake.date_time_between(start_date = '-2y', end_date = 'now'),
            }   
 
    
posts_list = [generate_post(i) for i in range(5)] 
   


@app.route('/')
def index():
    # 1/0
    text = 'Hello world!'
    return render_template('index.html', msg = text)

@app.route('/posts')
def posts():
    return render_template('posts.html', title = 'Posts', posts_list = posts_list)

@app.route('/posts/<int:post_id>')
def post(post_id):
    return render_template('posts.html', post = posts_list[post_id], title = 'Read more')

@app.route('/about')
def about():
    return render_template('about.html', title = 'About')


