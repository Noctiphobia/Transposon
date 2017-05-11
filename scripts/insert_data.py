from os import listdir
from os.path import join
import pg

files = listdir(path)
path = '../data/'

hostname = 'localhost'
username = 'postgres'
password = 'qwerty'
database = 'postgres'
port = 5432

header = None
sequence = None
added = 0

def insert_transposon(db):
	part = header.partition(' ')
	db.insert('bio.transposon', name = part[0], comment = part[2], sequence = sequence, source_file = filename)
	header = None
	sequence = None
	added += 1


with pg.DB(dbname = database, host = hostname, 
port = port, user = username, passwd = password) as db:

	for filename in files:
		with open(join(path, filename) ,'r') as f:
			for line in f:
				if len(line) == 0:
					continue
				if line[0] == '>':
					if !(header is None or sequence is None):
						insert_transposon(db)
					header = line
				elif sequence is None:
					sequence = line
				else:
					sequence += line
			if !(header is None or sequence is None):
				insert_transposon(db)






