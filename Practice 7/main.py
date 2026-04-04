import psycopg2
from psycopg2.extras import RealDictCursor, execute_batch
import sql
import csv

def csv_converter(file):
    spells = []
    with open(file) as f:
        reader = csv.reader(f)
        header = next(reader)
        
        for row in reader:
            if row:
                spells.append(tuple(row))
    return spells


conn_param = {
    "database": "pp2_db",     
    "user": "dayrengay",      
    "password": "123456",   
    "host": "127.0.0.1",            
    "port": "5432"
}

try:
    with psycopg2.connect(**conn_param) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # cur.execute(sql.create_table)
            
            #cur.execute(sql.insert_data, ("Zoltraak", "Common"))
            
            # spells = csv_converter("spells.csv")
            # execute_batch(cur, sql.insert_data, spells)
            
            # choice_insert=input("Insert by console? (y/n): ").lower()
            # if choice_insert == 'y':
            #     spell_name = input()
            #     spell_power = input()
            #     if spell_name and spell_power:
            #         cur.execute(sql.insert_data, (spell_name, spell_power))

            # update_choice = input("Wanna change? [y/n]").lower()
            # if update_choice == 'y':
            #     choice_of_update = input("What you wanna update?(name/power)").strip().lower()
            #     if choice_of_update == 'name':
            #         changer_id = input("Choose the id to update a spell").strip()
            #         upd_name = input(" Write new spell name").strip()
            #         cur.execute(sql.update_spell_name, (upd_name, changer_id))
            #     if choice_of_update == 'power':
            #         changer_name = input("Choose the name to update a power").strip()
            #         upd_power = input(" Write new spell power").strip()
            #         cur.execute(sql.update_spell_power, (upd_power, changer_name))   

            # order_question = input("Query by name or power or all?").strip().lower()
            # if order_question == 'name':
            #     cur.execute(sql.get_all_spells)
            # elif order_question == 'power':
            #     cur.execute(sql.get_all_power)
            # elif order_question == 'all':
            #     cur.execute(sql.get_all_data)

            # all_data =  cur.fetchall()
            # for row in all_data:
            #     print(f"id - {row['id']}, name - {row['spell_name']}, power - {row['spell_power']}")

            # delete_question = input("Wanna delete? [y/n]").strip().lower()
            # if delete_question == "y":
            #     choice_of_delete = input("What you wanna delete by?(name/power/id)").strip().lower()
            #     detail_of_delete = input("write the name/power/id you wanna delete").strip()
            #     if choice_of_delete == 'name':
            #         cur.execute(sql.delete_name, (detail_of_delete,))
            #     elif choice_of_delete == 'power':
            #         cur.execute(sql.delete_power,(detail_of_delete,))
            #     elif choice_of_delete  == 'id':
            #         cur.execute (sql.delete_by_id, (detail_of_delete,))
            print("\nDONE, STATEMENT")
             
except Exception as e:
    print(f"Error: {e}")

