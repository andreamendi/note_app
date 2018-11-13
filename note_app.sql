CREATE DATABASE note_app;
DROP DATABASE note_app;

USE note_app;


CREATE TABLE users(
	id int NOT NULL auto_increment,
    name VARCHAR(45) NOT NULL,
    username VARCHAR(45) NOT NULL UNIQUE,
    password varchar(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE notes(
	id INT NOT NULL auto_increment,
	title VARCHAR (45),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);


SELECT * FROM notes;
SELECT * FROM users;