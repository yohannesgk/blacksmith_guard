DROP TABLE IF EXISTS items;

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    owner TEXT NOT NULL,
    status TEXT NOT NULL
);

INSERT INTO items (id, name, owner, status) VALUES
    (1, 'Alpha', 'user-01', 'active'),
    (2, 'Beta', 'user-02', 'active'),
    (3, 'Gamma', 'user-03', 'inactive');
