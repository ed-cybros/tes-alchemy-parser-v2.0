import json
import sqlite3

# Connect with database:
conn = sqlite3.connect('data/03_alchemy_dataset.sqlite')
cur = conn.cursor()

# Load .json with final data:
with open("data/02_alchemy_transformed.json", "r") as file:
    dic = json.load(file)


# Insert data into Reagents table:
for key in dic:
    description = dic[key].get("description")
    if description:
        cur.execute('''
        INSERT INTO Reagents (name, description) VALUES (?, ?)''', (key, description))
    else:
        cur.execute('''
        INSERT INTO Reagents (name) VALUES (?)''', (key,))

conn.commit()
    

# Insert data into Effects table and Junction table:
for key in dic:
    effects = dic[key].get("effects")
    
    if effects:
        for polarity, effect_list in effects.items():

            for effect in effect_list:
                
                cur.execute('''
                INSERT OR IGNORE INTO Effects (name, polarity) VALUES (?, ?)''', (effect, polarity))
                
                cur.execute('''
                SELECT id FROM Reagents WHERE name = ? ''', (key,))
                reagent_id = cur.fetchone()[0]
                
                cur.execute('''
                SELECT id FROM Effects WHERE name = ? ''', (effect,))
                effect_id = cur.fetchone()[0]
                
                cur.execute('''
                INSERT OR IGNORE INTO Reagent_Effects (reagent_id, effect_id) VALUES (?, ?)''', (reagent_id, effect_id))

                cur.execute('''
                SELECT * FROM Reagent_Effects WHERE reagent_id = ? AND effect_id = ? ''', (reagent_id, effect_id))
                debug_result = cur.fetchall()

conn.commit()