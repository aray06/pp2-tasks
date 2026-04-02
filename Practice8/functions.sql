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