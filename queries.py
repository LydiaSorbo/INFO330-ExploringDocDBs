from pymongo import MongoClient

mongoClient = MongoClient("mongodb://localhost/pokemon")
pokemonDB = mongoClient['pokemondb']
pokemonColl = pokemonDB['pokemon_data']

pikachu = pokemonColl.find({'name': 'Pikachu'})

for pokemon in pikachu:
    print(pokemon)

attackPokemon = pokemonColl.find({"attack": {"$gt": 150}})

for pokemon in attackPokemon:
    print(pokemon)

overgrowPokemon = pokemonColl.find({"abilities": 'Overgrow'})

for pokemon in overgrowPokemon:
    print(pokemon)