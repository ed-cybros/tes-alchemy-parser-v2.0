# Initiate tables:
import sqlite3

conn = sqlite3.connect('data/03_alchemy_dataset.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Reagents')
cur.execute('DROP TABLE IF EXISTS Effects')
cur.execute('DROP TABLE IF EXISTS Reagent_Effects')

cur.execute('''
CREATE TABLE Reagents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    description TEXT
)
''')

cur.execute('''
CREATE TABLE Effects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    polarity TEXT
)
''')

cur.execute('''
CREATE TABLE Reagent_Effects (
    reagent_id INTEGER,
    effect_id INTEGER,
    PRIMARY KEY (reagent_id, effect_id),
            
    FOREIGN KEY (reagent_id)
    REFERENCES Reagents(id),

    FOREIGN KEY (effect_id)
    REFERENCES Effects(id)
)
''')

conn.commit()