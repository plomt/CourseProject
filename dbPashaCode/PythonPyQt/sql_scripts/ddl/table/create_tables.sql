CREATE TABLE IF NOT EXISTS project_pyqt.seance (
    id_seance SERIAL UNIQUE,
    name_user   VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS project_pyqt.message (
    command                  text,
    answer_to_command        text,
    flag                     BOOLEAN,
    date_time                VARCHAR(255),
    id_seance                VARCHAR(255)
);