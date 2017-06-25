from os import listdir
from os.path import join
import pg
import getpass
from sys import stdin

path = '../data/'
files = listdir(path)

hostname_default = 'localhost'
username_default = 'postgres'
database_default = 'postgres'
port_default = 5432

header = None
sequence = None
added = 0


def insert_transposon(db):
    global header
    global sequence
    global added
    part = header.partition(' ')
    db.insert('bio.transposon', name=part[0][1:], comment=part[2], sequence=sequence, source_file=filename)
    header = None
    sequence = None
    added += 1


def read_or_default(prompt, default):
    print((prompt + " [{}]: ").format(default))
    r = stdin.readline().rstrip('\n')
    return default if r == "" else r

hostname = read_or_default("Server", hostname_default)
database = read_or_default("Database", database_default)
port = int(read_or_default("Port", port_default))
username = read_or_default("Username", username_default)
password = getpass.getpass("Password for {}: ".format(username))
print("Connecting to database {} on {}:{} as {}...".format(database, hostname, port, username))

try:
    with pg.DB(dbname=database, host=hostname,
               port=port, user=username, passwd=password) as db:
        print("Connected.")
        for filename in files:
            print("Inserting {}...".format(filename))
            with open(join(path, filename), 'r') as f:
                for line in f:
                    if len(line) == 0:
                        continue
                    if line[0] == '>':
                        if not (header is None or sequence is None):
                            insert_transposon(db)
                        header = line
                    elif sequence is None:
                        sequence = line
                    else:
                        sequence += line
                if not (header is None or sequence is None):
                    insert_transposon(db)
        print("Added {} records, closing connection.".format(added))
except pg.InternalError as err:
    print("Error: {}".format(err))