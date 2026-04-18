create table trr (
    id int primary key,
    name varchar(255) not null,
    description text,
    created_at timestamp default current_timestamp
);


INSERT INTO trr (id, name, description) VALUES (1, 'Jose', 'This is a test TRR entry.');


SELECT * 
FROM trr
WHERE name > 'Jose';


CREATE TABLE futbolistas (
    id INT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    edad INT,
    posicion VARCHAR(100),
    equipo VARCHAR(255)
);

INSERT INTO futbolistas (id, nombre, edad, posicion, equipo) VALUES (1, 'Lionel Messi', 36, 'Delantero', 'Inter Miami');
INSERT INTO futbolistas (id, nombre, edad, posicion, equipo) VALUES (2, 'Cristiano Ronaldo', 38, 'Delantero', 'Al Nassr');
INSERT INTO futbolistas (id, nombre, edad, posicion, equipo) VALUES (3, 'Kylian Mbappé', 24, 'Delantero', 'Paris Saint-Germain');
INSERT INTO futbolistas (id, nombre, edad, posicion, equipo) VALUES (4, 'Neymar Jr.', 31, 'Delantero', 'Al Hilal');
INSERT INTO futbolistas (id, nombre, edad, posicion, equipo) VALUES (5, 'Sergio Ramos', 37, 'Defensor', 'Sevilla');
INSERT INTO futbolistas (id, nombre, edad, posicion, equipo) VALUES (6, 'Kevin De Bruyne', 32, 'Centrocampista', 'Manchester City');
INSERT INTO futbolistas (id, nombre, edad, posicion, equipo) VALUES (7, 'Luka Modrić', 37, 'Centrocampista', 'Real Madrid');
INSERT INTO futbolistas (id, nombre, edad, posicion, equipo) VALUES (8, 'Virgil van Dijk', 32, 'Defensor', 'Liverpool');
INSERT INTO futbolistas (id, nombre, edad, posicion, equipo) VALUES (9, 'Mohamed Salah', 31, 'Delantero', 'Liverpool');
INSERT INTO futbolistas (id, nombre, edad, posicion, equipo) VALUES (10, 'Erling Haaland', 23, 'Delantero', 'Manchester City');

SELECT * FROM futbolistas WHERE nombre = 'Neymar Jr.';










