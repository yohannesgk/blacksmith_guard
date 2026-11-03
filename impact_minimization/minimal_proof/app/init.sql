DROP TABLE IF EXISTS items;

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    owner TEXT NOT NULL,
    status TEXT NOT NULL
);

INSERT INTO items (id, name, owner, status) VALUES
    (1, 'Blue Nile Logistics Renewal', 'marta.oren', 'active'),
    (2, 'Meron Trading Group Invoice', 'dawit.tesfaye', 'active'),
    (3, 'Highland Telecom Service Order', 'selam.abebe', 'active');
