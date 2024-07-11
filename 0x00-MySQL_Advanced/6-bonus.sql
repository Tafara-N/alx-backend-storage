-- Script creates a STORED PROCEDURE `AddBonus` that adds a new correction FOR a student

DELIMETER |
CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score FLOAT
)

BEGIN
    INSERT INTO projects(name)
    SELECT project_name FROM DUAL
    WHERE NOT EXISTS (
        SELECT * FROM projects WHERE name = project_name
    );

    INSERT INTO corrections(user_id, project_id, score)
    VALUES(
        user_id,
        (SELECT id FROM projects WHERE name = project_name),
        score
        );
END;
|