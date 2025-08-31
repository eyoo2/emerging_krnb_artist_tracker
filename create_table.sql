CREATE TABLE krnb_artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    SID VARCHAR(22) NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    followers INT,
    popularity INT,
    image_url VARCHAR,
    artist_url VARCHAR
);