import os
import requests
import json
import datetime


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_list_of_movies_from_radarr(instance, api_key):
    headers = {'Content-Type': 'application/json', "X-Api-Key": api_key}
    api_address = instance + "api/movie"
    response = requests.get(api_address, headers=headers)
    data = response.json()

    list_of_ids = []

    for x in range(0, len(data)):
        buffer = data[x]["tmdbId"]
        list_of_ids.append(buffer)

    return list_of_ids


def get_movie_details_from_tmdb(movie_id, api_key):
    api_address = "https://api.themoviedb.org/3/movie/"
    api_call = api_address + movie_id + "?api_key=" + api_key
    response = requests.get(api_call)
    data = response.json()
    return data


def get_collection_details_from_tmdb(collection_id, api_key):
    api_address = "https://api.themoviedb.org/3/collection/"
    api_call = api_address + collection_id + "?api_key=" + api_key
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


def check_name_of_collection(movie_id, tmdb_api_key):
    movie_details = get_movie_details_from_tmdb(movie_id, tmdb_api_key)
    if movie_details['belongs_to_collection'] is None:
        return 0
    else:
        collection_name = movie_details['belongs_to_collection']['name']
        return collection_name


def check_id_of_collection(movie_id, tmdb_api_key):
    movie_details = get_movie_details_from_tmdb(movie_id, tmdb_api_key)
    if movie_details['belongs_to_collection'] is None:
        return 0
    else:
        collection_id = movie_details['belongs_to_collection']['id']
        return collection_id


def make_a_list_of_owned_collections(data, tmdb_api_key):
    list_of_collections = []
    counter = 0
    number_of_movies = len(data)

    for x in data:
        # wrong ID for a in TMDB movie - needs to be adjusted here
        if x == 690882:
            collection_id = check_id_of_collection("664847",
                                                   tmdb_api_key)
        else:
            collection_id = check_id_of_collection(str(x),
                                                   tmdb_api_key)
        counter += 1

        if collection_id == 0:
            pass
        else:
            if collection_id not in list_of_collections:
                list_of_collections.append(collection_id)
                print("Movies: " + str(counter) + "/" + str(number_of_movies))
                print("Found " + str(len(list_of_collections)) +
                      " collections")
    return list_of_collections


def get_movies_id_in_a_collection(collection, api_key):
    collection_details = get_collection_details_from_tmdb(collection, api_key)
    collection_details_parts = collection_details["parts"]
    movies_ids_in_collection = []

    for x in range(0, len(collection_details_parts)):
        collection_details_parts_titles = collection_details_parts[x]["id"]
        movies_ids_in_collection.append(collection_details_parts_titles)
    return movies_ids_in_collection


def check_if_movie_exists_in_library(movies, movies_in_collection, api_key):
    for x in movies_in_collection:
        if x in movies:
            pass
        else:
            movie_details = get_movie_details_from_tmdb(str(x), api_key)

            release_date = movie_details["release_date"]
            movie_title = movie_details["title"]
            release_date = release_date.split("-")

            if release_date == [""]:
                result = movie_title + " ( )"
                pass
            else:
                d1 = datetime.datetime(int(release_date[0]),
                                       int(release_date[1]),
                                       int(release_date[2])).date()
                d1_year = d1.year
                d2 = datetime.datetime.now().date()
                if d1 < d2:
                    result = movie_title + " (" + str(d1_year) + ")"
                    print(result)
                    store_results_in_txt(result, 'output/missing-movies.txt')
                else:
                    pass


def store_results_in_txt(result, filename):
    f = open(filename, "a")
    f.write(result + "\n")
    f.close()


def set_radarr_instance():
    protocol = os.environ.get('RADARR_PROTOCOL')
    ip = os.environ.get('radarr_ip')
    port = os.environ.get('radarr_port')

    url = protocol + "://" + ip + ":" + port + "/"
    return url


def set_radarr_api_key():
    key = os.environ.get('radarr_api_key')
    return key


def set_tmdb_api_key():
    key = os.environ.get('tmdb_api_key')
    return key


if __name__ == '__main__':
    radarr_instance = set_radarr_instance()
    radarr_api_key = set_radarr_api_key()
    tmdb_api_key = set_tmdb_api_key()

    open('output/missing-movies.txt', 'w').close()

    movies = get_list_of_movies_from_radarr(radarr_instance, radarr_api_key)

    collections = make_a_list_of_owned_collections(movies, tmdb_api_key)

    for x in collections:
        movies_in_coll = get_movies_id_in_a_collection(str(x), tmdb_api_key)
        check_if_movie_exists_in_library(movies, movies_in_coll, tmdb_api_key)
    print("Wrote list of missing movies to output/missing-movies.txt.")
