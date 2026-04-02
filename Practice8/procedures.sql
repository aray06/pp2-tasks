
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE name = p_name) THEN
        UPDATE contacts SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO contacts(name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_identity VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE name = p_identity OR phone = p_identity;
END;
$$;

-- 3. Процедура массовой вставки с валидацией
CREATE OR REPLACE PROCEDURE bulk_insert_contacts(p_names VARCHAR[], p_phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_upper(p_names, 1) LOOP
        -- Простая проверка: номер должен содержать только цифры/знаки
        IF p_phones[i] ~ '^[\+0-9\-\s]+$' THEN
            IF EXISTS (SELECT 1 FROM contacts WHERE name = p_names[i]) THEN
                UPDATE contacts SET phone = p_phones[i] WHERE name = p_names[i];
            ELSE
                INSERT INTO contacts(name, phone) VALUES(p_names[i], p_phones[i]);
            END IF;
        ELSE
            RAISE NOTICE 'NOT correct number: %', p_names[i];
        END IF;
    END LOOP;
END;
$$;