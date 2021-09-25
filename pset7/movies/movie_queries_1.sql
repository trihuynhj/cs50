-- Query to output titles of all movies release in 2008 --
SELECT title FROM movies WHERE year = 2008;

-- Query to output the birth year of artress Emma Stone --
SELECT birth FROM people WHERE name = "Emma Stone";

-- Query to output titles of all movies released on or after 2018, in alphabetical order --
SELECT title FROM movies WHERE year >= 2018 ORDER BY title ASC;

-- Query to output the number of movies with an IMDb rating of 10.0 --
SELECT COUNT(ratings.rating) FROM movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE ratings.rating = 10.0;

-- Query to output all titles and release years of Harry Potter movies, in chronological order --
SELECT title, year FROM movies WHERE title LIKE "Harry Potter%" ORDER BY year ASC;

-- Query to output the average rating of all movies released in 2012 --
SELECT AVG(ratings.rating) FROM movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE movies.year = 2012;

-- Query to output titles and ratings of all movies released in 2010 --
-- in descending order by rating, for movies with same ratings, order them alphabetically by title --
SELECT movies.title, ratings.rating FROM movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE movies.year = 2010
ORDER BY ratings.rating DESC, movies.title ASC;