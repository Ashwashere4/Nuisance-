CREATE TABLE songs(
    id  SERIAL PRIMARY KEY NOT NULL,
    songName TEXT NOT NULL,
    link TEXT NOT NULL
);

CREATE TABLE songSuggestees(
    id SERIAL PRIMARY KEY NOT NULL,
    songName TEXT NOT NULL,
    suggestees TEXT NOT NULL
);

INSERT INTO songs(songName, link) VALUES
('song1', 'test1');

INSERT INTO songSuggestees(songName, suggestees) VALUES
('song1', 'discord title');