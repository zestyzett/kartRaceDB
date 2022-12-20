import psycopg2
import psycopg2.extras
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from kartrace.db import get_db

bp = Blueprint('year',__name__)

@bp.route('/<year>', methods=('GET','POST'))
def year(year):
    conn = get_db()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    db.execute("""SELECT id, weekend_name FROM weekends WHERE year = 'year' """)
    weekends = db.fetchall()
    
    return render_template('year/year.html', weekends = weekends)