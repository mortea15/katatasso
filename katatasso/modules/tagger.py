import os
import sqlite3
import sys

import emailyzer
from flask import Flask, redirect, render_template, request

from katatasso.helpers.const import CATEGORIES, DBFILE, CLF_TRAININGDATA_PATH
from katatasso.helpers.extraction import get_file_paths

DATAPATH = CLF_TRAININGDATA_PATH

app = Flask(__name__, template_folder='../../../../../tagserver/templates')

phishing_dir = DATAPATH + 'phishing/'
spam_dir = DATAPATH + 'spam/'
legit_dir = DATAPATH + 'legitimate/'
emails = []

def load_emails():
    """
    Load emails from the specified directory.
        Untagged emails in root dir
        Subdirs for `phishing`, `spam`, and `legitimate`
    """
    legit = [ (legit_dir + fname, 0) for fname in os.listdir(legit_dir) ]
    spam = [ (spam_dir + fname, 1) for fname in os.listdir(spam_dir) ]
    phish = [ (phishing_dir + fname, 2) for fname in os.listdir(phishing_dir) ]
    untagged = [ (fname, -1) for fname in os.listdir(DATAPATH)]

    emails = legit + spam + phish + untagged

    print(f'''Loaded {len(emails)} emails
    => Legit:       {len(legit)}
    => Spam:        {len(spam)}
    => Phishing:    {len(phish)}
    ''')

    return emails

def create_conn():
    """
    Connect to the database file
    """
    return sqlite3.connect(DBFILE)

def init_db():
    """
    Inititalize database
    """
    conn = create_conn()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY AUTOINCREMENT, filepath TEXT NOT NULL, tag INTEGER)')
    conn.commit()
    conn.close()

def tag():
    """
    Add the tags to the DB
    """
    conn = create_conn()
    c = conn.cursor()
    tags = load_emails()
    c.executemany('INSERT INTO tags (filepath, tag) VALUES (?,?)', tags)
    conn.commit()
    conn.close()

def load_tags():
    conn = create_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM tags')
    res = c.fetchall()
    conn.close()
    return res

def load_tag(filepath):
    conn = create_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM tags WHERE filename=?', (filepath,))
    res = c.fetchone()
    conn.close()
    return res

def save_tag(filepath, tag):
    conn = create_conn()
    c = conn.cursor()
    c.execute('UPDATE tags SET tag=? WHERE filename=?', (tag, filepath))
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
    tags = load_tags()
    tagstats = {}
    for tag, cat in CATEGORIES.items():
        tagstats[tag] = { 'count': 0, 'category': cat }
    for tag in tags:
        tagstats[tag[2]]['count'] += 1
    return render_template(
        'index.html',
        appname = 'katatasso tagger',
        tags = tags,
        tagstats = tagstats,
        total = len(tags)
    )

@app.route('/show', methods=['GET'])
def show():
    filepath = request.form.get('filepath')
    try:
        if filepath:
            tag = load_tag(filepath)
            cat = CATEGORIES.get(tag[2])
            email = emailyzer.from_file(filepath)
            return render_template('email.html', email=email, tag=tag, cat=cat)
    except Exception as e:
        print(e)
        return '500 an error occurred'

@app.route('/tag', methods=['POST'])
def receive_tag():
    filepath = request.form.get('filepath')
    cat = request.form.get('cat')
    save_tag(filepath, cat)
    next_tag = get_next(filepath)
    if next_tag:
        return redirect(f'/show/{next_tag[1]}')
    else:
        return '201 donkey needs a nap'

def run_server():
    init_db()
    tag()

    app.run(debug=True)

if __name__ == '__main__':
    run_server()
