
import io
from flask import *
from app import db
from math import ceil
from flask_login import *
from auth import bp as auth_bp
PER_PAGE = 10

bp = Blueprint('visits', __name__, url_prefix='/visits')

def generate_report_file(records, fields):
    csv_content = '№,' + ','.join(fields) + '\n'
    for i, record in enumerate(records):
        values = [str(getattr(record, f, '')) for f in fields]
        csv_content += f'{i+1},' + ','.join(values) + '\n'
    f = io.BytesIO()
    f.write(csv_content.encode('utf-8'))
    f.seek(0)
    return f

@bp.route('/')
@login_required
def logging():
    if current_user.is_admin():
        page = request.args.get('page', 1, type = int)
        query = ('SELECT visit_logs.*, users.login '
                'FROM users RIGHT JOIN visit_logs ON visit_logs.user_id = users.id '
                'ORDER BY created_at DESC LIMIT %s OFFSET %s')
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query, (PER_PAGE, (page-1)*PER_PAGE))
            logs = cursor.fetchall()
    else:
        user_id = getattr(current_user, 'id', None)
        page = request.args.get('page', 1, type = int)
        query = ('SELECT visit_logs.*, users.login '
                'FROM users RIGHT JOIN visit_logs ON visit_logs.user_id = users.id '
                'WHERE user_id = %s '
                'ORDER BY created_at DESC LIMIT %s OFFSET %s')
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query, (user_id,PER_PAGE, (page-1)*PER_PAGE))
            logs = cursor.fetchall()
            
    query = 'SELECT COUNT(*) AS count FROM visit_logs'
    with db.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(query)
        count = cursor.fetchone().count
    
    last_page = ceil(count/PER_PAGE)

    return render_template('visits/logs.html', logs = logs, last_page = last_page, current_page = page)


@bp.route('/stat/pages')
@login_required
def pages_stat():
    if current_user.is_admin():
        page = request.args.get('page', 1, type = int)
        query = 'SELECT path, COUNT(*) as count FROM visit_logs GROUP BY path ORDER BY count DESC LIMIT %s OFFSET %s;'
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query, (PER_PAGE, (page-1)*PER_PAGE))
            records = cursor.fetchall()
        
        query = 'SELECT COUNT(*) AS count FROM (SELECT path, COUNT(*) as count FROM visit_logs GROUP BY path ORDER BY `count` DESC) as result'
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query)
            count = cursor.fetchone().count
    
        last_page = ceil(count/PER_PAGE)
        
        if request.args.get('download_csv'):
            f = generate_report_file(records, ['path', 'count'])
            return send_file(f, mimetype='text/csv', as_attachment=True, download_name='pages_stat.csv')
        return render_template('visits/pages_stat.html', records=records,last_page = last_page, current_page = page)
    else:
        flash('Недостаточно прав', 'warning')
        return redirect(url_for('visits.logging'))
    
    
@bp.route('/stat/log')
@login_required
def log_stat():
    if current_user.is_admin():
        page = request.args.get('page', 1, type = int)
        query = ('SELECT users.login, COUNT(*) as count ' 
                'FROM visit_logs ' 
                'JOIN users ON visit_logs.user_id = users.id '
                'GROUP BY visit_logs.user_id '
                'ORDER BY count DESC;')
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            
        query = 'SELECT COUNT(*) AS count FROM (SELECT users.login, COUNT(*) as count FROM visit_logs JOIN users ON visit_logs.user_id = users.id GROUP BY visit_logs.user_id ORDER BY count DESC) as result'
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query)
            count = cursor.fetchone().count
    
        last_page = ceil(count/PER_PAGE)
        
        if request.args.get('download_csv'):
            f = generate_report_file(records, ['path', 'count'])
            return send_file(f, mimetype='text/csv', as_attachment=True, download_name='pages_stat.csv')
        return render_template('visits/log_stat.html', records=records,last_page = 1, current_page = page)
    else:
        flash('Недостаточно прав', 'warning')
        return redirect(url_for('visits.logging'))

