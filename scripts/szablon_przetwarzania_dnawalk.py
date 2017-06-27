#moze komuś się przyda - gotowy skrypt do przechodzenia po sygnałach transpozonów, coś można z tym tu zrobić

import pg
import re
db = pg.DB(dbname="postgres", host="localhost", port=5432, user="postgres", passwd="twoje_haslo")
from pgdb import connect
con = connect(database='postgres', host='localhost:5432', user='postgres', password='twoje_haslo')

cursor = con.cursor()

#transpozony przetłumaczone na sygnały dna walk (tutaj jest limit 1 dla przykładu)
cursor.execute("select distinct transposon_id from bio.dna_walk limit 1")

transposon_row = cursor.fetchone()

while transposon_row is not None:
	
	#wybranie sekwencji
	sequence = con.cursor().execute("select num,x,y from bio.dna_walk where transposon_id = "+str(transposon_row.transposon_id)+" order by num asc").fetchall()
	#sequence to lista czegoś co zachowuje się jak tuple, mozna z tym cos ciekawego zrobic w tym miejscu:
    print(sequence[3])
	#atrybuty num, x i y
	
	transposon_row = cursor.fetchone()