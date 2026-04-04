create_table = """
CREATE TABLE IF NOT EXISTS magic_book (
    id SERIAL PRIMARY KEY,
    spell_name TEXT NOT NULL,
    spell_power VARCHAR(20)
);
"""

insert_data = """
INSERT INTO magic_book (spell_name, spell_power)
VALUES (%s, %s)
RETURNING id;
"""

update_spell_name = """
UPDATE magic_book
SET spell_name = %s
WHERE id =%s;
"""

update_spell_power = """
UPDATE magic_book
SET spell_power = %s
WHERE spell_name = %s;
"""

get_all_data = """
SELECT * FROM magic_book ORDER BY id ASC;
"""
get_all_spells = "SELECT * FROM magic_book ORDER BY spell_name ASC;"
get_all_power = "SELECT * FROM magic_book ORDER BY spell_power ASC;"

delete_name = """
DELETE FROM magic_book WHERE spell_name =%s;
"""
delete_power = "DELETE FROM magic_book WHERE spell_power = %s"
delete_by_id = "DELETE FROM magic_book WHERE id = %s"