CREATE TABLE trr(
    trr_id TEXT,
    trr_time TIMESTAMPTZ,
    nsv_id INT,
    PRIMARY KEY(trr_id, trr_time)
);