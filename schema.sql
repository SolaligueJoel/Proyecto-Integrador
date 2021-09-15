DROP TABLE IF EXISTS localidad;

CREATE TABLE localidad(
    [id] INTEGER PRIMARY KEY AUTOINCREMENT,
    [price_min] TEXT NOT NULL,
    [price_max] INTEGER NOT NULL,
);