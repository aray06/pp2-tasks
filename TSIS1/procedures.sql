-- 1. Добавление телефона
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE first_name = p_contact_name OR last_name = p_contact_name LIMIT 1;
    IF v_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
    ELSE
        RAISE NOTICE 'Contact % not found', p_contact_name;
    END IF;
END;
$$;

-- 2. Смена группы
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    UPDATE contacts SET group_id = v_group_id 
    WHERE first_name = p_contact_name OR last_name = p_contact_name;
END;
$$;

-- 3. Расширенный поиск (Функция)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INTEGER, full_name TEXT, email VARCHAR, birthday DATE, group_name VARCHAR, phone_list TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        c.id, 
        (c.first_name || ' ' || COALESCE(c.last_name, ''))::TEXT as full_name, 
        c.email, 
        c.birthday, 
        g.name as group_name,
        string_agg(p.phone || ' (' || p.type || ')', ', ') as phone_list
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.last_name  ILIKE '%' || p_query || '%'
       OR c.email      ILIKE '%' || p_query || '%'
       OR p.phone      ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END;
$$ LANGUAGE plpgsql;