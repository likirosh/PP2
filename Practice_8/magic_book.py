from connect import conn, cur


def add_spell(spell_name, spell_power):
    cur.execute("CALL upsert_spell(%s, %s)", (spell_name, spell_power))
    conn.commit()

def update_spell_name(old_name, new_name):
    cur.execute("UPDATE magic_book SET spell_name = %s WHERE spell_name = %s", (new_name, old_name))
    conn.commit()

def update_spell_power(spell_name, new_power):
    cur.execute("UPDATE magic_book SET spell_power = %s WHERE spell_name = %s", (new_power, spell_name))
    conn.commit()

def delete_spell(value):
    cur.execute("CALL delete_spell(%s)", (value,))
    conn.commit()

def search_spell(pattern):
    cur.execute("SELECT * FROM get_spells_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()
    return rows

def show_spells(limit, offset):
    cur.execute("SELECT * FROM get_spells_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    return rows

def insert_many():
    names  = ["Fireball", "Ice Lance", "Time Stop"]
    powers = ["Common", "Rare", "Legendary"]
    cur.execute("CALL insert_m(%s, %s)", (names, powers))
    conn.commit()

def print_rows(rows):
    if not rows:
        print("No spells found.")
        return
    for i, row in enumerate(rows, start=1):
        id_, spell_name, spell_power = row
        print(f"{i}. ID: {id_} | Spell: {spell_name} | Power: {spell_power}")

        while True:
            print("\n1) Add/Update spell")
            print("2) Show spells")
            print("3) Search spell")
            print("4) Delete spell")
            print("5) Insert many")
            print("6) Update spell name")
            print("7) Update spell power")
            print("8) Exit")

    n = input("Choose: ")

    if n == "1":
        name  = input("Spell name: ")
        power = input("Spell power: ")
        functions.add_spell(name, power)
        print("Done.")

    elif n == "2":
        limit  = int(input("Limit: "))
        offset = int(input("Offset: "))
        rows = functions.show_spells(limit, offset)
        functions.print_rows(rows)

    elif n == "3":
        pattern = input("Enter pattern: ").strip()
        rows = functions.search_spell(pattern)
        functions.print_rows(rows)

    elif n == "4":
        value = input("Enter spell name or power: ")
        functions.delete_spell(value)
        print("Done.")

    elif n == "5":
        functions.insert_many()
        print("Done.")

    elif n == "6":
        old_name = input("Current spell name: ")
        new_name = input("New spell name: ")
        functions.update_spell_name(old_name, new_name)
        print("Done.")

    elif n == "7":
        spell_name = input("Spell name: ")
        new_power  = input("New spell power: ")
        functions.update_spell_power(spell_name, new_power)
        print("Done.")

    elif n == "8":
        break