CREATE DATABASE articles;

USE articles;

CREATE TABLE article (
    id int NOT NULL auto_increment,
    url VARCHAR(1000) NOT NULL,
    title VARCHAR(1000),
    year int,
    journal VARCHAR(1000),
    science_field VARCHAR(1000),
    abstract VARCHAR(1000),
    likes int,
    dislikes int,
    seen int,
    downloaded int,
    link_gost VARCHAR(1000),
    PRIMARY KEY (id));

CREATE TABLE request (
    id int NOT NULL auto_increment,
    text VARCHAR(1000),
    date DATETIME,
    results_found int,
    PRIMARY KEY (id)
);

CREATE TABLE keywords(
    article_id int,
    word VARCHAR(1000),
    FOREIGN KEY (article_id) REFERENCES article(id) ON DELETE CASCADE
);

CREATE TABLE authors(
    article_id int,
    author VARCHAR(1000),
    FOREIGN KEY (article_id) REFERENCES article(id) ON DELETE CASCADE
);

CREATE TABLE article_request(
    article_id int,
    request_id int,
    FOREIGN KEY (article_id) REFERENCES article(id) ON DELETE CASCADE,
    FOREIGN KEY (request_id) REFERENCES request(id) ON DELETE CASCADE
);