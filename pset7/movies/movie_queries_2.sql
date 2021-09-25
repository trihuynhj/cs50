-- Query to output names of all people that starred in Toy Story --
SELECT people.name FROM stars
JOIN movies ON movies.id = stars.movie_id
JOIN people ON people.id = stars.person_id
WHERE movies.title = "Toy Story";

-- Query to output names of all people who starred in a movie released in 2004, ordered by birth year --
SELECT DISTINCT people.name FROM stars
JOIN movies ON movies.id = stars.movie_id
JOIN people ON people.id = stars.person_id
WHERE movies.year = 2004 ORDER BY birth;

-- Query to output names of all the people who directed a movie with a rating of at least 9.0 --
SELECT DISTINCT people.name FROM directors
INNER JOIN movies ON movies.id = directors.movie_id
INNER JOIN people ON people.id = directors.person_id
INNER JOIN ratings ON movies.id = ratings.movie_id
WHERE ratings.rating >= 9.0 ORDER BY people.name ASC;

-- Query to output titles of 5 highest rated movies (in order) that --
-- Chadwick Boseman starred in, starting with the highest rated --
SELECT movies.title FROM stars
INNER JOIN movies ON movies.id = stars.movie_id
INNER JOIN people ON people.id = stars.person_id
INNER JOIN ratings ON movies.id = ratings.movie_id
WHERE people.name = "Chadwick Boseman"
ORDER BY ratings.rating DESC
LIMIT 5;

-- Query to output titles of movies in which --
-- Johnny Depp and Helena Bonham Carter starred --
SELECT movies.title FROM stars
INNER JOIN movies ON movies.id = stars.movie_id
INNER JOIN people ON people.id = stars.person_id
WHERE people.name = "Johnny Depp" OR people.name = "Helena Bonham Carter"

-- These two commands go together to get the titles that has 2 people names (stars)
GROUP BY movies.title
HAVING COUNT(DISTINCT people.name) = 2;

-- Query to output names of all people who starred in movies --
-- in which Kevin Bacon also starred --

SELECT DISTINCT people.name FROM stars
INNER JOIN movies ON movies.id = stars.movie_id
INNER JOIN people ON people.id = stars.person_id
WHERE (people.name != "Kevin Bacon" AND movies.title IN (
    SELECT movies.title FROM stars
    INNER JOIN movies ON movies.id = stars.movie_id
    INNER JOIN people on people.id = stars.person_id
    WHERE people.name = "Kevin Bacon" ORDER BY movies.title
));