-- Script creates a TRIGGER that resets the attribute valid_email only WHEN the email has been changed

DROP TRIGGER IF EXISTS is_email;
DELIMETER $$
CREATE TRIGGER is_email BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email != NEW.email THEN
        SET NEW.valid_email = 0;
    ELSE
        SET NEW.valid_email = NEW.valid_email;
    END IF;
END $$
DELIMITER;
