-- Script creates a TRIGGER that decreases the quantity OF an item after adding a new ORDER

CREATE TRIGGER decrease_order AFTER INSERT ON `orders`
FOR EACH ROW UPDATE `items`
SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;
