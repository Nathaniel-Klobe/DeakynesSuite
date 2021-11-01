DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS ticket;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS specialorder;
DROP TABLE IF EXISTS rental;
DROP TABLE IF EXISTS rentalitem;
DROP TABLE IF EXISTS repairservice;
DROP TABLE IF EXISTS tickettype;


CREATE TABLE customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    street_address TEXT NOT NULL,
    phone TEXT NOT NULL
);

CREATE TABLE ticket(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    ticket_type TEXT NOT NULL,
    ticket_description TEXT NOT NULL,
    reference TEXT,
    ticketstatus TEXT NOT NULL,
    created DATE NOT NULL,
    promised DATE,
    sentoutlocation TEXT,
    sentoutdate DATE,
    sentoutnotes TEXT,
    labor DECIMAL(4,2),
    parts DECIMAL(4,2),
    other DECIMAL(4,2),
    total DECIMAL(4,2),
    notes TEXT,
    completed DATE,
    called DATE,
    pickedup DATE,
    FOREIGN KEY (customer_id) REFERENCES customer(id)
);

CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE specialorder(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_type TEXT NOT NULL,
    order_description TEXT NOT NULL,
    order_from TEXT NOT NULL,
    created DATE NOT NULL,
    promised DATE,
    FOREIGN KEY (customer_id) REFERENCES customer(id)
);

CREATE TABLE rentalitem(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    sku TEXT NOT NULL,
    item_description TEXT NOT NULL
);

CREATE TABLE rental(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    rentalitem INTEGER NOT NULL,
    rental_period TEXT NOT NULL,
    created DATE NOT NULL,
    promised DATE NOT NULL,
    cost DECIMAL NOT NULL,
    paid BOOLEAN NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer(id),
    FOREIGN KEY (rentalitem) REFERENCES rentalitem(id)
);

CREATE TABLE repairservice(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    street_address TEXT NOT NULL,
    phone TEXT NOT NULL
);

CREATE TABLE tickettype(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
