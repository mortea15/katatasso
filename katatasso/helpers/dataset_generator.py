import os
import sqlite3
import sys

from katatasso.helpers.const import CATEGORIES, DBFILE, CLF_TRAININGDATA_PATH
from katatasso.helpers.extraction import get_file_paths, warn_failed
from katatasso.helpers.utils import progress_bar
import juicer
import emailyzer

DATAPATH = CLF_TRAININGDATA_PATH
phishing_dir = DATAPATH + 'phishing/'
spam_dir = DATAPATH + 'spam/'
legit_dir = DATAPATH + 'legitimate/'
mal_dir = DATAPATH + 'malware/'
fraud_dir = DATAPATH + 'fraud/'
emails = []

DBFILE = 'tagger.db'

def load_emails():
    legit = [ (legit_dir + fname, 0) for fname in os.listdir(legit_dir) ]
    spam = [ (spam_dir + fname, 1) for fname in os.listdir(spam_dir) ]
    phish = [ (phishing_dir + fname, 2) for fname in os.listdir(phishing_dir) ]
    malware = [ (mal_dir + fname, 3) for fname in os.listdir(mal_dir) ]
    fraud = [ (fraud_dir + fname, 4) for fname in os.listdir(fraud_dir) ]

    emails = legit + spam + phish + malware + fraud

    print(f'''Loaded {len(emails)} emails
    => Legit:       {len(legit)}
    => Spam:        {len(spam)}
    => Phishing:    {len(phish)}
    => Malware:     {len(malware)}
    => Fraud:       {len(fraud)}
    ''')

    return emails


def parse_emails(tags):
    failed = []
    parsed = []
    tagger = juicer.initStanfordNERTagger()
    for tag in progress_bar(tags):
        try:
            filepath = tag[0]
            email = emailyzer.from_file(filepath)
            content = email.html_as_text
            # Preprocess, extract entities
            words = juicer.extract_stanford(content, named_only=False, stemming=False, tagger=tagger)
            hosts = '|'.join(email.hosts)
            tagged = (filepath, tag[1], words, hosts)
            parsed.append(tagged)
        except:
            failed.append(filepath.replace(CLF_TRAININGDATA_PATH, ''))
            pass

    if failed:
        warn_failed(failed)

    return parsed 


def create_conn():
    return sqlite3.connect(DBFILE)

def init_db():
    conn = create_conn()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY AUTOINCREMENT, filepath TEXT NOT NULL, tag INTEGER, text TEXT, hosts TEXT)')
    conn.commit()
    conn.close()

def tag():
    conn = create_conn()
    c = conn.cursor()
    tags = load_emails()
    tags = parse_emails(tags)
    c.executemany('INSERT INTO tags (filepath, tag, text, hosts) VALUES (?,?,?,?)', tags)
    conn.commit()
    conn.close()

def count():
    conn = create_conn()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM tags')
    total = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM tags WHERE tag=?', (0,))
    legit = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM tags WHERE tag=?', (1,))
    spam = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM tags WHERE tag=?', (2,))
    phish = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM tags WHERE tag=?', (3,))
    malware = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM tags WHERE tag=?', (4,))
    fraud = c.fetchone()[0]
    
    print(f'''DB: {total} emails
    => Legit:       {legit}
    => Spam:        {spam}
    => Phishing:    {phish}
    => Malware:     {malware}
    => Fraud:       {fraud}
    ''')


def main():
    if not os.path.isfile(DBFILE):
        print('DB not present. Creating..')
        init_db()
    tag()
    count()

if __name__ == '__main__':
    main()
