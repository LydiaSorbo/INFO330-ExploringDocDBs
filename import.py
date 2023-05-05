import sqlite3
import sys
from pymongo import MongoClient

mongoClient = MongoClient("mongodb://localhost/pokemon")
pokemonDB = mongoClient['pokemondb']
pokemonColl = pokemonDB['pokemon_data']

try:
    conn = sqlite3.connect('pokemon.sqlite')

    cur = conn.cursor()
    
    generalquery = "SELECT name, pokedex_number, hp, attack, defense, speed, sp_attack, sp_defense FROM pokemon ORDER BY pokedex_number"
    typesquery = "SELECT type1, type2 FROM pokemon_types_view WHERE name = ?"
    abilityquery = "SELECT name FROM ability WHERE id IN (SELECT ability_id FROM pokemon_abilities WHERE " \
               "pokemon_id = ?)"

    rows = cur.execute(generalquery).fetchall()
    for row in rows:

        name, pokedex_number, hp, attack, defense, speed, sp_attack, sp_defense = row

        types_results = cur.execute(typesquery, (name,)).fetchall()
        types = []
        for t in types_results:
            types.append(t[0])
            if t[1]:
                types.append(t[1])

        ability_results = cur.execute(abilityquery, (pokedex_number,)).fetchall()
        abilities = [a[0] for a in ability_results]

        pokemon = {
            "name": name,
            "pokedex_number": pokedex_number,
            "types": types,
            "hp": hp,
            "attack": attack,
            "defense": defense,
            "speed": speed,
            "sp_attack": sp_attack,
            "sp_defense": sp_defense,
            "abilities": abilities
        }

        pokemonColl.insert_one(pokemon)

    for doc in pokemonColl.find():
        print(doc)

except sqlite3.Error as e:
    print("SQLite error occurred:", e)
except Exception as e:
    print("An error occurred:", e)


conn.close()
