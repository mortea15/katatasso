import os
import sqlite3
import sys

import emailyzer
from flask import Flask, redirect, render_template, request

from katatasso.helpers.const import CATEGORIES
from katatasso.helpers.extraction import get_file_paths

DATAPATH = os.getenv('CLF_TRAININGDATA_PATH', 'trainingdata/')

app = Flask(__name__)

def load_emails():
    files = [ fp.replace(DATAPATH, '') for fp in os.listdir(DATAPATH) ]
    return files

def create_conn():
    return sqlite3.connect('tagger.db')

def init_db():
    conn = create_conn()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL, tag INTEGER)')
    emails = load_emails()
    untagged = [(filename, 5) for filename in emails]
    c.executemany('INSERT INTO tags (filename, tag) VALUES (?,?)', untagged)
    conn.commit()
    conn.close()

def add_missing_tags():
    added = 0
    conn = create_conn()
    c = conn.cursor()
    emails = load_emails()
    untagged = [(filename, 5) for filename in emails]
    for tag in untagged:
        c.execute('SELECT * FROM tags WHERE filename=?', (tag[0],))
        res = c.fetchone()
        if not res:
            c.execute('INSERT INTO tags (filename, tag) VALUES (?,?)', tag)
            added += 1
    if added > 0:
        print(f'{added} rows inserted')
        conn.commit()
    conn.close()

def load_tags():
    conn = create_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM tags')
    res = c.fetchall()
    conn.close()
    return res

def load_tag(filename):
    conn = create_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM tags WHERE filename=?', (filename,))
    res = c.fetchone()
    conn.close()
    return res

def save_tag(filename, tag):
    conn = create_conn()
    c = conn.cursor()
    c.execute('UPDATE tags SET tag=? WHERE filename=?', (tag, filename))
    conn.commit()
    conn.close()

def get_next(filename):
    conn = create_conn()
    c = conn.cursor()
    c.execute('SELECT id FROM tags WHERE filename=?', (filename,))
    cid = c.fetchone()[0]
    c.execute('SELECT * FROM tags WHERE id=?', (cid + 1,))
    return c.fetchone()

@app.route('/', methods=['GET'])
def index():
    return render_template(
        'index.html',
        appname = 'katatasso tagger',
        tags = load_tags()
    )

@app.route('/show/<filename>', methods=['GET'])
def show(filename):
    try:
        if filename:
            tag = load_tag(filename)
            cat = CATEGORIES.get(tag[2])
            email = emailyzer.from_file(DATAPATH + filename)
            return render_template('email.html', email=email, tag=tag, cat=cat)
    except Exception as e:
        print(e)
        return '404 donkey is sad'

@app.route('/tag', methods=['POST'])
def receive_tag():
    filename = request.form.get('filename')
    cat = request.form.get('cat')
    save_tag(filename, cat)
    next_tag = get_next(filename)
    if next_tag:
        return redirect(f'/show/{next_tag[1]}')
    else:
        return '201 donkey needs a nap'

def run_server():
    if not os.path.isfile('tagger.db'):
        print('DB not present. Creating..')
        init_db()
    else:
        add_missing_tags()

    app.run()

if __name__ == '__main__':
    run_server()
