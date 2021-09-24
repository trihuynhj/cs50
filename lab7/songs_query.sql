-- Query to output names of all the songs in the database --
SELECT name FROM songs;

-- Query to output names of all the songs in increasing order of tempo --
SELECT name FROM songs ORDER BY tempo ASC;

-- Query to output the names of 5 longest songs in descending order --
SELECT name FROM songs ORDER BY duration_ms DESC LIMIT 5;

-- Query to output names of any songs with danceability, energy and valence greater than 0.75 --
SELECT name FROM songs WHERE danceability > 0.75 AND energy > 0.75 AND valence > 0.75;

-- Query to output the average energy of all the songs --
SELECT AVG(energy) FROM songs;

-- Query to output the names of all the songs by Post Malone --
SELECT songs.name FROM songs
JOIN artists ON songs.artist_id = artists.id
WHERE artists.name = "Post Malone";

-- Query to output the average energy of songs by Drake --
SELECT AVG(songs.energy) FROM songs
JOIN artists ON songs.artist_id = artists.id
WHERE artists.name = "Drake";

-- Query to output names of all the songs that feature other artists --
SELECT name FROM songs WHERE name LIKE "%feat.%";