-- database: database.db

PRAGMA foreign_keys = ON;

INSERT INTO colours (id,name) VALUES
    (1,'Yellow'),
    (2,'Red'),
    (3,'Purple');

INSERT INTO categories (id,name) VALUES
    (1,'Annual'),
    (2,'Perennial'),
    (3,'Shrub');

INSERT INTO flowers
    (id, name, latin, season, sunlight, watering, difficulty, colour_id, category_id)
VALUES
   (1,'Sunflower','Helianthus annuus','Summer','Full Sun','Medium','Easy',1,1),
   (2, 'Rose','Rosa','Spring-Autumn','Full Sun','Medium','Hard',2,3),
   (3,'Lavender','lavare', 'Summer','Full Sun','Low','Easy',3,2);