-- Script creates a TRIGGER that resets the attribute valid_email only WHEN the email has been changed

DELIMETER
//
CREATE TRIGGER email_validate_trigger BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END;
//
