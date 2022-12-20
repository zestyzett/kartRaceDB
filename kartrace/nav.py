import psycopg2
import psycopg2.extras
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from kartrace.db import get_db

bp = Blueprint('index',__name__)

@bp.route('/', methods=('GET','POST'))
def index():
    conn = get_db()
    db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    db.execute("""SELECT DISTINCT year FROM weekends order by year""")
    years = db.fetchall()
    
    return render_template('index/index.html', years = years)

