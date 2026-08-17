PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS flowers;
DROP TABLE IF EXISTS colours;
DROP TABLE IF EXISTS categories;

CREATE TABLE colours (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE categories (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE flowers (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    latin       TEXT,
    season      TEXT NOT NULL,
    sunlight    TEXT NOT NULL,
    watering    TEXT NOT NULL,
    difficulty  TEXT NOT NULL,
    colour_id   INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (colour_id) REFERENCES colours(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
