import os
import requests
import json
import config
from extract import json_extract


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_list_of_movies_from_radarr(instance, api_key):
    headers = {'Content-Type': 'application/json', "X-Api-Key": api_key}
    api_address = instance + "api/movie"
    response = requests.get(api_address, headers=headers)
    data = response.json()
    return data


def get_movie_details_from_tmdb(movie_id, api_key):
    api_address = "https://api.themoviedb.org/3/movie/"
    api_call = api_address + movie_id + "?api_key=" + api_key
    response = requests.get(api_call)
    data = response.json()
    return data


def write_to_json(content, filename):
    with open(filename, "w+") as f:
        json.dump(content, f)
        f.close()


def read_from_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data


def check_if_part_of_a_collection(movie_id, tmdb_api_key):
    movie_details = get_movie_details_from_tmdb(movie_id, tmdb_api_key)
    if movie_details['belongs_to_collection'] is None:
        return 0
    else:
        collection = movie_details['belongs_to_collection']['name']
        # title = movie_details['original_title']
        # detail = title + " belongs to collection: " + collection
        return collection


def make_a_list_of_owned_collections(data, tmdb_api_key):
    list_of_movies_ids = json_extract(data, "tmdbId")
    list_of_collections = []
    counter = 0
    number_of_movies = len(list_of_movies_ids)

    for x in list_of_movies_ids:
        print(x)

        # wrong ID for a in TMDB movie - needs to be adjusted here
        if x == 690882:
            collection_title = check_if_part_of_a_collection("664847",
                                                             tmdb_api_key)
        else:
            collection_title = check_if_part_of_a_collection(str(x),
                                                             tmdb_api_key)
        counter += 1
        # print(str(counter))
        if collection_title == 0:
            pass
        else:
            if collection_title not in list_of_collections:
                list_of_collections.append(collection_title)
                cls()
                # print(list_of_collections)
                print(str(counter) + "/" + str(number_of_movies))
                print(str(len(list_of_collections)) + " collections")
    return list_of_collections


if __name__ == '__main__':
    data = get_list_of_movies_from_radarr(config.radarr_instance,
                                          config.radarr_api_key)

    # collections are stored in collections var as a list of strings
    collections = make_a_list_of_owned_collections(data, config.tmdb_api_key)
    print(collections)
