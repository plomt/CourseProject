CREATE TABLE IF NOT EXISTS project_pyqt.message (
    command                  VARCHAR(255),
    answer_to_command        VARCHAR(255),
    flag                     VARCHAR(255),
    date_time                TIMESTAMP,
    name_seance              SERIAL REFERENCES seance (name_seance)
);

CREATE TABLE IF NOT EXISTS project_pyqt.seance (
    name_seance SERIAL,
    name_user   VARCHAR(255)
);