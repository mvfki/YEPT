'''For developer use only'''
import pickle
from Bio import SeqIO
import os
import sqlite3

this_dir, this_filename = os.path.split(__file__)

def importAnn(src = 'contig'):
    ann = os.path.join(this_dir, src+'.ann.pkl')
    with open(ann, 'rb') as f:
        table = pickle.load(f)
    f.close()
    return table

def importGenome(species):
    dataPath = os.path.join(this_dir, 'data', species, 'seq.pkl')
    with open(dataPath, 'rb') as f:
        fasta = pickle.load(f)
    f.close()
    return fasta

def search(species, keyword):
    '''
    Search the preprepared SQLite3 database for the given keywords, and return 
    the matched result.
    Arguments:
    ----------
    species - str. 
              Choose from {'P', 'C', 'J', 'O'}.
    keyword - str.
              Can be either GenBank accession ID, gene symbol, or systematic 
              ID (PomBase) for S. pombe. 
    Return:
    ----------
    result - list.
             elements are tuples with 9 fields each, where the 3rd is the 
             chromosome identifier, the 4th for the start, the 5th for the end, 
             the 6th for the strand. 
    '''
    sp = {'P': 'S_pombe'}
    dbPath = os.path.join(this_dir, 'data', sp[species], 'ANNOTATION.db')
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    cmd = '''SELECT * 
    FROM ANNOTATION
    WHERE GenBank LIKE "%{0}%" 
    OR PomBase LIKE "%{0}%" 
    OR Symbol LIKE "%{0}%";'''.format(keyword)
    return c.execute(cmd).fetchall()

    
