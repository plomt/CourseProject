CREATE TABLE IF NOT EXISTS project_pyqt.message (
    sentence    text,
    flag        varchar(255),
    date_time   timestamp
);

CREATE TABLE IF NOT EXISTS project_pyqt.seance (
    name_seance varchar(255),
    name_user   varchar(255)
);