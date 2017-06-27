#odpalane po stworzeniu tabeli dna_walk, sktypt wypełniający ją danymi

import pg
import re
db = pg.DB(dbname="postgres", host="localhost", port=5432, user="postgres", passwd="twoje_haslo")
from pgdb import connect
con = connect(database='postgres', host='localhost:5432', user='postgres', password='twoje_haslo')

cursor = con.cursor()

#limit 1000 - to i tak ogrom danych (~4.5 KK rekordów)
cursor.execute("select id, sequence from bio.transposon limit 1000")

row = cursor.fetchone()
while row is not None:
	#normalizacja sekwencji
	sequence = re.sub("\s+","",row.sequence).upper()
	transposon_id = row.id
	num = 0
	x = 0
	y = 0
	bulk = []
	for s in sequence:
		if (s=="N"):
			continue
			
		if s not in ["A","G","T","C"]:
			raise Exception("Bad FASTA format - transposon_id: "+str(transposon_id)+", nucleotide \""+s+"\"")
			
		#wzięte z PDF-a
		x = x+1 if s=="A" else x if (s=="G" or s=="T") else x-1
		y = y+1 if s=="G" else y if (s=="A" or s=="C") else y-1
		bulk.append((num,x,y,transposon_id))
		num=num+1
	
	#bulk insert by było szybciej
	db.inserttable("bio.dna_walk",bulk)
	row = cursor.fetchone()