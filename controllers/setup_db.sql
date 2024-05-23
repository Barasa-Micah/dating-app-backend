CREATE DATABASE datingApp;

USE datingApp;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    county VARCHAR(100),
    constituency VARCHAR(100),
    height VARCHAR(50),
    complexion VARCHAR(50),
    body_shape VARCHAR(50),
    hairstyle VARCHAR(50),
    beards BOOLEAN,
    phone_number VARCHAR(15),
    connections JSON,
    connection_requests JSON
);
