CREATE OR REPLACE FUNCTION get_spells_by_pattern(p text)
RETURNS TABLE(id INT, spell_name VARCHAR, spell_power VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT mb.id, mb.spell_name, mb.spell_power
    FROM magic_book mb
    WHERE mb.spell_name ILIKE '%' || p || '%'
       OR mb.spell_power ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_spells_paginated(lim INT, off INT)
RETURNS TABLE(id INT, spell_name VARCHAR, spell_power VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT mb.id, mb.spell_name, mb.spell_power
    FROM magic_book mb
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;