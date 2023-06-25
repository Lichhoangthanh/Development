from flask import *
from flask_login import *
from auth import check_rights
from app import db
from math import ceil
from werkzeug.utils import secure_filename
# from books_tool import *
import mysql.connector
import os
from bs4 import BeautifulSoup

PER_PAGE = 3
PERMITTED_PARAMS = ["title", "description", "year", "publisher", "author","page_count"]
EDIT_PARAMS = ["id","title", "description", "year", "publisher", "author","page_count"]
COVER_PARAMS = ["filename","mime","type"]
EDIT_GENRES = ["book_id","genre"]


bp = Blueprint('books', __name__, url_prefix='/books')


@bp.route('/')
def all():
    page = request.args.get('page', 1, type = int)
    query = ('SELECT * FROM books JOIN covers ON books.cover_id = covers.id_covers LIMIT %s OFFSET %s')
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query,(PER_PAGE, (page-1)*PER_PAGE))
        books_list = cursor.fetchall()
    
    query = 'SELECT COUNT(*) AS count FROM (SELECT * FROM books JOIN covers ON books.cover_id = covers.id_covers) as result'
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query)
        count = cursor.fetchone().count
    
    last_page = ceil(count/PER_PAGE)
    
    query = "SELECT users.*, roles.name as role_name FROM users LEFT JOIN roles ON users.role_id=roles.id WHERE users.id = %s;"
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (current_user.id,))

        db_user = cursor.fetchone()
    
    return render_template('books/books.html', user = db_user, books_list=books_list, last_page = last_page, current_page = page,bgs = load_book_genres(), genres = load_genres())

def load_genres():
    query = "SELECT * FROM genres;"
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query)
        db_genres = cursor.fetchall()
    return db_genres

def load_book_genres():
    query = "SELECT * FROM book_genre;"
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query)
        db_bg = cursor.fetchall()
    return db_bg

@bp.route('/<int:book_id>')
def show_book(book_id):
    query = ('SELECT * FROM (SELECT * FROM books JOIN covers ON books.cover_id = covers.id_covers) as result WHERE id = %s')
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (book_id,))
        book = cursor.fetchone()
    
    if book is None:
        flash("Пользователь не найден", "danger")
        return redirect(url_for("books.all"))
    
    return render_template('books/book.html', book=book)

@bp.route('/books/<int:book_id>/edit', methods=['GET'])
@login_required
@check_rights("edit")
def edit_book(book_id):
    edit_select = "SELECT * FROM books WHERE id = %s;"
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(edit_select, (book_id,))
        book = cursor.fetchone()
        if book is None:
            flash("Пользователь не найден", "warning")
            return redirect(url_for("books.all"))
        
    return render_template("books/edit_books.html", book=book,bgs = load_book_genres(), genres = load_genres())

def params(names_list):
    result = {}
    for name in names_list:
        result[name] = request.form.get(name) or None
    return result

@bp.route('/books/<int:book_id>/update', methods=['POST'])
@login_required
@check_rights("edit")
def update_book(book_id):
    cur_params = params(EDIT_PARAMS)
    fields = ", ".join([f"{key} = %({key})s" for key in cur_params.keys()])
    update_query = f"UPDATE books SET {fields} WHERE id = %(id)s;"
    cur_params["id"] = book_id
    try:
        with db.connection.cursor(named_tuple = True) as cursor:
            cursor.execute(update_query, cur_params)
            db.connection.commit()
            flash("Пользователь успешно обновлен", "success")
    except mysql.connector.errors.DatabaseError:
        flash("При изменении возникла ошибка", "danger")
        db.connection.rollback()
        return render_template('books/edit_books.html', book=cur_params,bgs=load_book_genres(),genres = load_genres())
    
      
    return redirect(url_for("books.all"))

@bp.route('/new')
@login_required
@check_rights("create")
def new_book():
    return render_template('books/new.html', bgs=load_book_genres(),genres = load_genres(),books={})
        
def insert_to_db(params, cover_id):
    query = """
        INSERT INTO books (title, description, year, publisher, author, page_count, cover_id) 
        VALUES (%(title)s, %(description)s, %(year)s, %(publisher)s, %(author)s, %(page_count)s, %(cover_id)s)
    """
    
    params["cover_id"] = cover_id
    
    try:
        with db.connection.cursor(named_tuple=True) as cursor:
            cursor.execute(query, params)
            db.connection.commit()
            cursor.close()
    except mysql.connector.errors.DatabaseError:
        db.connection.rollback()
        return False

    return True

def insert_f_to_db(params):
    query = """
        INSERT INTO covers (filename, mime_type, md5_hash) 
        VALUES (%(filename)s, %(mime_type)s, %(md5_hash)s)
    """
    try:
        with db.connection.cursor(named_tuple = True) as cursor:
            cursor.execute(query, params)
    except Exception:
        db.connection.rollback()
        return False

    return True

# def insert_genres_to_db(book_id,genre_id):
#     query = "INSERT INTO book_genre (book_id, genre_id) VALUES (%s,%s)"
#     try:
#         with db.connection.cursor(named_tuple=True) as cursor:
#             cursor.execute(query, (book_id,genre_id))
#             print(cursor.statement)
#     except Exception:
#         db.connection.rollback()


    

@bp.route('/create', methods=['POST'])
@login_required
@check_rights("create")
def create_book():
    if not current_user.can("create"):
        flash("Недостаточно прав для доступа к странице", "warning")
        return redirect(url_for("books"))
    
    # file
    file = request.files.get('photo')
    files = {
        "filename" : file.filename,
        "mime_type" : file.mimetype,
        "md5_hash" : "aaaaa"
    }
    inserted_cover = insert_f_to_db(files)

    # get covers id
    query = "SELECT id_covers AS id FROM covers WHERE filename = %s"
    with db.connection.cursor(named_tuple=True) as cursor:
        cursor.execute(query, (file.filename,))
        result = cursor.fetchall()
    if result:
        id_value = result[0].id
    else:
        flash("Không thể tìm thấy thông tin bìa sách", "danger")
        return redirect(url_for("books.new"))
    cur_params = params(PERMITTED_PARAMS)
    inserted = insert_to_db(cur_params,id_value)
    
    # get book id
    query = "SELECT id FROM books WHERE cover_id = %s"
    with db.connection.cursor(named_tuple=True) as cursor:
        cursor.execute(query, (id_value,))
        result = cursor.fetchall()
    if result:
        id_book = result[0].id
        print(id_book)
    else:
        flash("Không thể tìm thấy thông tin sách", "danger")
        return redirect(url_for("books.new"))
    # genre_id = request.form.get('genre_id')
    genre_id = 8
    

    # add genre
    query = "INSERT INTO book_genre (book_id, genre_id) VALUES (%s,%s)"
    try:
        with db.connection.cursor(named_tuple=True) as cursor:
            cursor.execute(query, (id_book,genre_id))
            print(cursor.statement)
    except Exception:
        db.connection.rollback()
    
    if inserted and inserted_cover:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        flash("Пользователь успешно добавлен", "success")
        return redirect(url_for("books.all"))
    else:
        flash("При сохранении возникла ошибка", "danger")
        return render_template("books/new.html",book=cur_params, bgs=load_book_genres(),genres = load_genres())

    
@bp.route("/<int:book_id>/delete", methods=['POST'])
@login_required
@check_rights("delete")
def delete_book(book_id):
    delete_query="DELETE books, covers FROM books JOIN covers ON books.cover_id = covers.id_covers WHERE books.id =  %s"
    try:
        with db.connection.cursor(named_tuple = True) as cursor:
            cursor.execute(delete_query, (book_id,))
            db.connection.commit()
            flash("Пользователь успешно удален", "success")
    except mysql.connector.errors.DatabaseError:
        flash("При удалении произошла ошибка", "danger")
        db.connection.rollback()
    return redirect(url_for("books.all"))
    