CREATE OR REPLACE PROCEDURE upsert_spell(s_name TEXT, s_power TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM magic_book WHERE spell_name = s_name) THEN
        UPDATE magic_book SET spell_power = s_power WHERE spell_name = s_name;
    ELSE
        INSERT INTO magic_book(spell_name, spell_power) VALUES (s_name, s_power);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_spell(s text)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM magic_book WHERE spell_name=s OR spell_power=s;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_m(s_names TEXT[], s_power TEXT[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(s_names, 1) LOOP
        INSERT INTO magic_book(spell_name, spell_power)
        VALUES (s_names[i], s_power[i]);
    END LOOP;
END;
$$;