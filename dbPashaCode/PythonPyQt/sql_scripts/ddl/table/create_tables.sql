CREATE TABLE IF NOT EXISTS project_pyqt.seance (
    id_seance SERIAL UNIQUE,
    name_user   VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS project_pyqt.message (
    command                  VARCHAR(255),
    answer_to_command        VARCHAR(255),
    flag                     VARCHAR(255),
    date_time                TIMESTAMP,
    id_seance                SERIAL REFERENCES project_pyqt.seance (id_seance)
);