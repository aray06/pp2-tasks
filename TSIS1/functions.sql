-- 1. Функция поиска по шаблону
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE(contact_name VARCHAR, contact_phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT name, phone 
    FROM contacts 
    WHERE name ILIKE '%' || p_pattern || '%'
       OR phone ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Функция для пагинации
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(contact_name VARCHAR, contact_phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT name, phone 
    FROM contacts 
    ORDER BY name ASC 
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION GET_NAMES_CNT(PNAME TEXT)
RETURNS INT AS $$
DECLARE
    counter INT;
BEGIN
    SELECT COUNT(*) INTO counter FROM contacts WHERE first_name = PNAME;
    RETURN counter;
END;
$$ LANGUAGE plpgsql;



SELECT COUNT(*) FROM CONTACTS WHERE NAME = AITYM

