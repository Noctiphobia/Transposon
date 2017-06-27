CREATE TABLE bio.dna_walk(
  num integer, --numer w sekwencji, by można było łatwo przechodzić przez nią
  x integer, --współrzędna pozioma sygnału
  y integer, --współrzędna pionowa sygnału
  transposon_id integer references bio.transposon(id) --który transpozon? klucz obcy
);

CREATE INDEX IX_dna_num ON bio.dna_walk (transposon_id, num);