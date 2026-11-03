CREATE TABLE IF NOT EXIST contactos(
    id_contacto bigint INT AUTOINCREMENT PRIMARY KEY,
    nombre VARCHAR (100) NOT NULL,
    email VARCHAR (100) NOT NULL,
    telefono VARCHAR (13) NOT NULL
);

INSERT INTO contactos(nombre,email,telefono)
VALUES
("Cintia Rubí", "sosa@gmail.com","7752324788");
("Victor Borbolla", "hugo@gmail.com","7752324788");

