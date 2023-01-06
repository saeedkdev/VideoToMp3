CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';

CREATE DATABASE auth_db;

GRANT ALL PRIVILEGES ON auth_db.* TO 'auth_user'@'localhost';

USE auth_db;

CREATE TABLE users (
	id INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(50) NOT NULL UNIQUE,
	password VARCHAR(255) NOT NULL,
	PRIMARY KEY (id)
);

INSERT INTO users (email, password) VALUES ('saeedsektor@gmail.com', '$2a$04$jDtlyB6s1dBzmTi6/yoH2uKfmGoyK14z58phGg7e4SSpWIaQGrvhm');
