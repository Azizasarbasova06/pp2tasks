CREATE OR REPLACE FUNCTION search_by_pattern(p_pattern TEXT)
RETURNS TABLE(
    p_id INT,
    p_name VARCHAR,
    p_surname VARCHAR,
    p_phone VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, surname, phone
    FROM phonebook
    WHERE name ILIKE '%' || p_pattern || '%'
       OR surname ILIKE '%' || p_pattern || '%'
       OR phone ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(
    p_id INT,
    p_name VARCHAR,
    p_surname VARCHAR,
    p_phone VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT id, name, surname, phone
    FROM phonebook
    ORDER BY id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;