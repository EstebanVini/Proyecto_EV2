CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    release DATE, -- Cambiar a DATE si es una fecha válida
    type TEXT,
    genre TEXT,
    imageurl TEXT,
    user1 TEXT,
    user2 TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,  -- Cambiado a SERIAL para autoincrementar
    username TEXT,
    email TEXT,
    password TEXT,
    salt TEXT,
    relatedto TEXT,
    admin BOOLEAN
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,  -- SERIAL reemplaza AUTOINCREMENT
    userID INTEGER,
    sender TEXT,
    receiver TEXT,
    message TEXT,
    date TIMESTAMP,  -- Cambiado a TIMESTAMP si quieres almacenar fecha y hora
    FOREIGN KEY (userID) REFERENCES users(id)  -- Ajustada la clave foránea para referenciar el campo id de la tabla users
);
