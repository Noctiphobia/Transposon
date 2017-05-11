CREATE TABLE bio.transposon(
  id serial PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  comment VARCHAR(255),
  sequence text NOT NULL,
  source_file VARCHAR(50)
);

CREATE INDEX IX_transposon_name ON bio.transposon (name);