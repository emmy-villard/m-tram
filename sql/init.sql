CREATE TABLE trr(
    trr_id TEXT,
    trr_time TIMESTAMP,
    trr_nsv_id INT,
    PRIMARY KEY(trr_id, trr_time)
);

CREATE TABLE ligne(
    ligne_id TEXT,
    ligne_time TIMESTAMP,
    ligne_nsv_id INT,
    PRIMARY KEY(ligne_id, ligne_time)
);