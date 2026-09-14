DROP TABLE IF EXISTS items;

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    owner TEXT NOT NULL,
    status TEXT NOT NULL
);

INSERT INTO items (id, name, owner, status) VALUES
    (1, 'Synthetic Account Alpha', 'test-user-01', 'active'),
    (2, 'Synthetic Account Beta', 'test-user-02', 'active'),
    (3, 'Synthetic Account Gamma', 'test-user-03', 'active');